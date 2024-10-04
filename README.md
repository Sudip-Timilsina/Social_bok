# Social Book

## Project Overview
This repository contains a full-stack Django project aimed at building a simple and functional social media application. The application includes core features such as user profiles, posts, comments, and interactions, providing a platform for users to share content and engage with each other.

## Features
- **User Registration and Authentication**
  - User sign-up, login, and logout functionality.
  - User profile management and profile picture uploads.
- **Create, Read, Update, and Delete (CRUD) for Posts**
  - Users can create, and view posts.
  - 
- **Like/Unlike Posts**
  - Users can like or unlike posts, with like counts displayed.
- **User Profiles**
  - Display user details and their specific posts.
- **Follow System**
  - Users can follow or unfollow other users, with follower and following counts.

## Tech Stack
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript (for dynamic interactions)
- **Database**: SQLite (default), or any other supported by Django (e.g., PostgreSQL)
- **Version Control**: Git and GitHub

## Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Virtual Environment (e.g., `venv` or `pipenv`)
- Git

### Steps

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/repo-name.git
    cd repo-name
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```bash
    python manage.py runserver
    ```

7. **Access the application**
    - Open your browser and navigate to `http://127.0.0.1:8000/`


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For any inquiries, please reach out to:  
**Email**: timilsinasudip980@example.com  
**GitHub**: [Sudip-Timilsina](https://github.com/Sudip-Timilsina)


