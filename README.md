# Cowculator Backend

## Setup
- Ensure python is installed along with pip and/or pip3
- Ensure packages in `requirements.txt` are installed: `pip install -r requirements.txt`

### Folders structure

>
        .
        ├── ...
        ├── main.py               # Main file responsible for running the server
        ├── routers               # Handling of endpoints
        ├── models                # Definitions for all database models
        ├── config                # Access to server environment variables
        └── ...

## Starting the dev environment
- Navigate to the root of this repo and run `uvicorn main:app --reload`
- In your browser, navigate to localhost:8000/doc to see the Swagger Doc for the API
- Make sure to `Ctrl + C` out of the terminal when done development, otherwise the application may continue to run in the background (blocking your port) after closing your code editor