# Java Gateway

This Spring Boot Maven application provides a gateway for the machine learning component, nodeJS component and performs CRUD operations on users and recommendations. The application exposes RESTful APIs for interacting with users, recommendations, and various external services. Backend is created using Java, Redis and MySQL

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [User Management](#user-management)
  - [Recommendation Management](#recommendation-management)
  - [External Services](#external-services)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Java Development Kit (JDK) 1.8 or higher
- Maven 3.6.0 or higher
- Redis Server

### Installation

1. Clone the repository:
   ```
   git clone https://gitlab.scss.tcd.ie/smart_city/back-end.git
   ```
2. Change into the project directory:
   ```
   cd back-end
   ```
3. Install the dependencies using Maven:
   ```
   mvn clean install
   ```

## Redis Setup
- Download and extract Redis-x64-3.2.100.zip (windows executable)
- Extract anywhere and run redis-server.exe
- Redis server is running when you see message "# Server started, Redis version 3.2.100"
- Port 6379 is used for Redis

## MySQL

- Download and setup MySQL and let username be 'root' and password be 'password'
- Run on port 3306
- If password is set differently:
  1. Clone project from gitlab
  2. Go to 'back-end/src/main/resources/application.properties'
  3. Change spring.datasource.username=root and spring.datasource.password=password
  4. If want to use other database change property spring.datasource.url=jdbc:mysql://localhost:3306/ase
  5. Then open the folder in command prompt and run the command 'mvn clean install'
  6. For above command you need Java JDK installed and if still not able to run install Apache Maven and add to path.
  7. Once successfully run, you can see generated JAR in Target folder and then follow below steps

- Create Database named 'ase' in MySQL using query 'create database ase;'
- https://blog.devart.com/mysql-command-line-client.html tutorial to run sql queries

## Apache Maven Setup 

- https://stackoverflow.com/a/56616547

## Running the Application

1. Start the Redis server by running the following command in your terminal:
   ```
   redis-server
   ```
2. Run the Spring Boot application with Maven:
   ```
   mvn spring-boot:run
   ```

The application will start on the default port `8080`.

## API Endpoints

### User Management

- `POST /request/saveUser`: Save a new user to the database
- `GET /request/allUsers`: Get all users from the database
- `GET /request/getOne/{id}`: Get a specific user by ID
- `PUT /request/modify/{id}`: Update an existing user by ID
- `DELETE /request/delete/{id}`: Delete a user by ID

### Recommendation Management

- **GET** `/recommendations/all`: Retrieves all the recommendations stored in the database.

  - Example: `GET http://localhost:9090/recommendations/all`

- **GET** `/recommendations/get/{id}`: Retrieves the recommendation with the specified `id`.

  - Example: `GET http://localhost:9090/recommendations/get/1`

- **POST** `/recommendations/create`: Creates a new recommendation in the database.

  - Example: `POST http://localhost:9090/recommendations/create`

  - Request Body:

    ```json
    {
      "incident": "Traffic jam",
      "location": "City center",
      "message": "Avoid city center due to traffic jam"
    }
    ```

- **PUT** `/recommendations/update/{id}`: Updates the recommendation with the specified `id`.

  - Example: `PUT http://localhost:8080/recommendations/update/1`

  - Request Body:

    ```json
    {
      "incident": "Road closure",
      "location": "City center",
      "message": "City center road closed for maintenance"
    }
    ```

- **DELETE** `/recommendations/{id}`: Deletes the recommendation with the specified `id`.

  - Example: `DELETE http://localhost:8080/recommendations/delete/1`

- **GET** `/recommendations/newrecommendations`: Fetches latest recommendations from the database that are created in the last 2 minutes.

- **GET** `/recommendations/oldrecommendations`: Fetches old recommendations from the database that are created before 2 minutes.

### External Services

- `POST /request/authenticate`: Authenticate a user and return an access token
- `GET /request/luas/stop/{stop}`: Get LUAS details for a specific stop
- `GET /request/bus/stop/{stop}`: Get bus details for a specific stop
- `GET /request/getCctv/{id}`: Get CCTV details for a specific ID
- `GET /request/getBike/{id}`: Get bike details for a specific ID
- `GET /request/getTaxi`: Get taxi details
- `POST /request/getCabCluster`: Get cab cluster data

## Sample Requests and Responses

Here are some sample requests and responses for the API endpoints provided by the application:

### User Management

#### Save a new user

Request:

```
POST /request/saveUser
Content-Type: application/json

{
    "userName": "rohitt",
    "passWord": "example"
}

```

Response:

```
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "userName": "rohitt",
  "passWord": "example"
}
```

#### Get all users

Request:

```
GET /request/allUsers
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  }
]
```

### External Services

#### Authenticate a user

Request:

```
POST /request/authenticate
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "johndoe123"
}
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "authorized": "true"
}
```

#### Get LUAS details for a specific stop

Request:

```
GET request/luas/stop/MUS
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "stop_name": "Museum",
  "stop_id": "1",
  "trams": [
    {
      "due_mins": 4,
      "destination": "Sandyford",
      "tram_id": "1"
    },
    {
      "due_mins": 7,
      "destination": "Brides Glen",
      "tram_id": "2"
    }
  ]
}
```

## Testing

To run tests for the application, execute the following command:

```
mvn test
```

## Deployment

To deploy the application, package it using the following command:

```
mvn package
```

This command will generate a JAR file in the `target` directory. You can run the application using the following command:

```
java -jar target/ase-backend-2.6.6.jar
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

- Rohit Das - [dasro](https://gitlab.scss.tcd.ie/dasro)

See also the list of [contributors](https/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- The project uses the [Spring Boot](https://spring.io/projects/spring-boot) framework for rapid development and deployment.
- [Maven](https://maven.apache.org/) is used as the build and dependency management tool.

## Troubleshooting

If you encounter any issues while running the application, please check the following:

1. Ensure that you have the correct version of Java (Java 11) installed.
2. Ensure that all dependencies are installed correctly.
3. If you encounter any issues with the database, make sure that the database server is running and the connection details are configured correctly in the `application.properties` file.
4. If you encounter any issues with the redis server, make sure that the redis server is running and the connection details are configured correctly in the `application.properties` file.
5. For any other issues, please refer to the [official Spring Boot documentation](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/) or raise an issue on the project's GitHub repository.

Feel free to reach out to the project maintainers if you need further assistance.
