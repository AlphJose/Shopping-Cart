# Shopping Cart

A FastAPI application incorporating SQLAlchemy, JWT and Pytest. This project also includes asynchronous calls and tests. asyncio is used for tests. </br>
![image]({https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white})
![image]({https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white})
![image]({https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white})
![image]({https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen})
![image]({BadgeURLHere})

## Pre-requisites 

 [![GitHub top language](https://img.shields.io/github/languages/top/vinitshahdeo/PortScanner?logo=python&logoColor=white)](https://www.python.org/)

- **Python** `>= v3.8.9`
    - Install Python from [here](https://www.python.org/).

## How to run
From project root directory run:
```sh
dotenv run uvicorn app.main:app
```

The default value for `APP_PORT` is 8000.
It can be overridden by passing port number like this:

```sh
dotenv run uvicorn app.main:app --port 9000
```
### APIs

Available at [ShoppingCart.postman_collection.json](https://github.com/AlphJose/Shopping-Cart/blob/main/ShoppingCart.postman_collection.json). Also available at http://localhost:{port}/docs .


## How to Test
From project root directory run:

```sh
dotenv -f test.env run python3 -m pytest
```
