from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,Post,LikePost,FollowerCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.
@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    
    # Check if the profile exists, and if not, handle it
    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        # Create a profile if not found, or redirect to profile setup page
        user_profile = Profile.objects.create(user=user_object, id_user=user_object.id)
        user_profile.save()
        # Optionally, redirect the user to a profile setup page:
        # return redirect('setting') 
    user_following_list=[]
    feed=[]
    user_following=FollowerCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    for username in user_following:
        feed_list=Post.objects.filter(user=username)
        feed.append(feed_list)

    feed_lists=list(chain(*feed))

    #user suggestion
    all_users=User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_sugeestion_list=[x for x in list(all_users) if (x not in list(user_following_all))]
    curent_user=User.objects.filter(username=request.user.username)
    final_suggestions_list=[x for x in list(new_sugeestion_list) if (x not in list(curent_user))]

    random.shuffle(final_suggestions_list)


    username_profile=[]
    username_profile_list=[]

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestions_username_profile_list=list(chain(*username_profile_list))
    return render(request, 'index.html', {'user_profile': user_profile,'posts': feed_lists,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})
def signup(request):

    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                #Log user in and redirect to setting there profile
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                #create a Profile objects for the new user
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
        else:
            messages.info(request,"Password Not Matching")
            return redirect('signup')

      
    else:
        return render(request,'signup.html')
    

def signin(request):
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Credentials Invalid")
            return redirect("signin")
    else:
        return render(request,'signin.html')
@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Initialize the bio and location fields from the request data
        bio = request.POST.get('bio', '')  # Default to empty string if not provided
        location = request.POST.get('location', '')  # Default to empty string if not provided

        # Check if the user uploaded a new profile image
        if request.FILES.get('image') is None:
            # No new image uploaded, use the existing one
            image = user_profile.profileimg
        else:
            # New image uploaded
            image = request.FILES.get('image')

        # Update the user's profile
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('setting')

    return render(request, 'setting.html', {'user_profile': user_profile})
@login_required(login_url="signin")
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
@login_required(login_url="signin")
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)

    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()
    if like_filter==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_like=post.no_of_like+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_like=post.no_of_like-1
        post.save()
        return redirect('/')
@login_required(login_url="signin")    
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=pk)
    user_post_length=len(user_post)

    follower=request.user.username
    user=pk
    if FollowerCount.objects.filter(follower=follower,user=user).first():
        buttonText='Unfollow'
    else:
        buttonText='Follow'   
    user_followers=len(FollowerCount.objects.filter(user=pk))
    user_following=len(FollowerCount.objects.filter(follower=pk)) 


    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_length':user_post_length,
        'buttonText':buttonText,
        'user_followers':user_followers,
        'user_following':user_following,

    }
    return render(request,'profile.html',context)
@login_required(login_url="signin") 
def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']
        if FollowerCount.objects.filter(follower=follower,user=user).first():
            delete_followers=FollowerCount.objects.get(follower=follower,user=user)
            delete_followers.delete()
            return redirect('/profile/'+user)
        else:
           new_follower=FollowerCount.objects.create(follower=follower,user=user)
           new_follower.save()
           return redirect('/profile/'+user)
    else:
        return redirect('/')
@login_required(login_url="signin")    
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    if request.method == "POST":
        username=request.POST['username']
        username_objects=User.objects.filter(username__icontains=username)
        username_profile=[]
        username_profile_list=[]

        for users in username_objects:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_list=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)

        username_profile_list=list(chain(*username_profile_list))


    return render (request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})

