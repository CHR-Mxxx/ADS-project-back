# FastAPI Authentication App

This project is a FastAPI application that implements user registration, login, and user information expiration features. It provides a simple and secure way to manage user accounts and their associated data.

## Features

- User registration with hashed passwords
- User login with credential validation
- User information retrieval
- Expiration management for user data

## Project Structure

```
fastapi-auth-app
├── app
│   ├── main.py               # Entry point of the FastAPI application
│   ├── models
│   │   └── user.py           # User model definition
│   ├── routes
│   │   ├── auth.py           # Authentication routes
│   │   └── user.py           # User-related routes
│   ├── services
│   │   └── expiration.py      # User information expiration logic
│   └── schemas
│       └── user.py            # schemas for user data validation
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .env                       # Environment variables
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-auth-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Set up your environment variables in the `.env` file. You will need to specify your database connection string and any secret keys for authentication.

2. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

3. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.

## License

This project is licensed under the MIT License. See the LICENSE file for details.