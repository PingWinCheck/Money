# Money
catalog money site on FastAPI framework


1. Установка зависимостей:
    
    ```
    poetry install
    ```
2. Создать файл .env с необходимыми переменными окружения

    ```
    Данные от postgres db
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    DB_NAME=
   
    TEST_DB_USER=
    TEST_DB_PASSWORD=
    TEST_DB_HOST=
    TEST_DB_PORT=
    TEST_DB_NAME=
   
    PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
    rsa приватный ключ для jwt
    -----END PRIVATE KEY-----"
    PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
    rsa публичный ключ для jwt
    -----END PUBLIC KEY-----"
   
    Данные от SMTP
    SMTP_PASS=
    SMTP_LOGIN=
    SMTP_SERVER=
    SMTP_PORT=
   
    Данные от RabbitMQ
    RMQ_USER=
    RMQ_PASS=
    RMQ_HOST=
    RMQ_PORT=
    RMQ_QUEUE=
   
    Данные от Redis
    REDIS_HOST=
    REDIS_PORT=
    ```
3. Поднять весь проект в docker-compose:
    
    ```
    docker-compose up
    ```
