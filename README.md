# Django Core CRUD API

## Overview

This project is a backend application built using Django that provides a simple API for managing user data. It includes CRUD (Create, Read, Update, Delete) operations and is designed for integration with other applications or services.

## Features

- **User Registration**: Register a new user.
- **User Login**: Authenticate existing users.
- **List Users**: Retrieve a list of registered users.
- **Update User**: Modify user details.
- **Delete User**: Remove a user from the system.

## API Endpoints

The following endpoints are available:

| HTTP Method | Endpoint           | Description                    |
|-------------|--------------------|--------------------------------|
| POST        | `/register-user`    | Register a new user.          |
| POST        | `/login-user`       | Log in an existing user.      |
| GET         | `/list-user`        | Retrieve a list of users.     |
| PUT         | `/update-user`      | Update details of a user.     |
| DELETE      | `/delete-user`      | Delete a user.                |
