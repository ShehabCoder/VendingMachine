# Vending Machine API 🍬

Welcome to the Vending Machine API documentation! This API allows users with different roles to interact with a vending machine system. Users with
a "seller" role can manage products, while users with a "buyer" role can deposit coins, purchase products, and reset their deposits.

## Prerequisites 🛠️

Before getting started, make sure you have completed the following steps:

1. Activate your virtual environment:
 \myenv\Scripts\activate

2. Install required dependencies:
  pip install -r requirements.txt

3. Download and install PostgreSQL.

4. Install Postman and join the workspace invited to your email (knassef90@gmail.com).

5. Sign up using the `/signUp` endpoint with the following parameters: "username,"password",role.

6. Obtain the authentication token from the response in Postman.

7. For each endpoint, pass the token under the Authorization tab in Postman, selecting Bearer Token as the token type.

8. Enjoy exploring the Vending Machine API! 🎉

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Users](#users)
4. [Products](#products)
5. [Deposits](#deposits)
6. [Purchases](#purchases)
7. [Reset](#reset)
8.. [Error Handling](#error-handling)
9. [Edge Cases](#edge-cases)

## Authentication

Authentication is required for certain endpoints. Users with the "seller" role have elevated privileges compared to users with the "buyer" role.

## Endpoints

### Users

- `GET /users`: Retrieve information about all users.
- `GET /users/{user_id}`: Retrieve information about a specific user.
- `POST /users`: Create a new user. Authentication not required.
- `PUT /users/{user_id}`: Update user information.
- `DELETE /users/{user_id}`: Delete a user.

### Products

- `GET /products`: Retrieve information about all products. Accessible to all users.
- `GET /products/{product_id}`: Retrieve information about a specific product. Accessible to all users.
- `POST /products`: Create a new product. Requires authentication as a "seller".
- `PUT /products/{product_id}`: Update product information. Requires authentication as a "seller".
- `DELETE /products/{product_id}`: Delete a product. Requires authentication as a "seller".

### Deposits

- `POST /deposit`: Deposit coins into the vending machine account. Accessible to users with a "buyer" role.

### Purchases

- `POST /buy`: Purchase products using deposited coins. Accessible to users with a "buyer" role.

### Reset

- `POST /reset`: Reset deposit amount for users with a "buyer" role.

## Error Handling

The API will return appropriate HTTP status codes and error messages for invalid requests, unauthorized access, or server errors.

## Edge Cases

- Ensure that only users with the "seller" role can perform CRUD operations on products.
- Validate the deposit amount to accept only 5, 10, 20, 50, and 100 cent coins.
- Handle scenarios where users attempt to purchase products with insufficient funds.
- Implement safeguards against race conditions and concurrent access to the vending machine resources.

Thank you for using the Vending Machine API! If you have any questions  please contact me to support.



