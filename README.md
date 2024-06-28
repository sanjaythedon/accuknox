
# Social Media App

This project provides APIs to manage users and the relationship between them which replicates how facebook works.


## Installation

1. Clone the project

```bash
  https://github.com/sanjaythedon/accuknox.git
```
2. Open your command line and go to the project directory.

3. Create a Docker image
```bash
docker build -t django_docker .
```
4. Create a container of that image which would start the application
```bash
docker run -d -p 8000:8000 django_docker 
```
5. Test the APIs that are mentioned in API Endpoints documentation

## Data Model

### Modified User

| Attributes    | Type          |
| ------------- |:-------------:|
| id      | AutoField |
| first_name      | CharField      |
| last_name | CharField      |
| name | CharField      |
| email | EmailField      |
| password | CharField      |

### Friend Requests

| Attributes    | Type          |
| ------------- |:-------------:|
| id      | AutoField |
| sender_id      | ForeignKey      |
| status | CharField      |
| receiver_id | ForeignKey      |

## API Endpoints

This postman documentation contains all details about each API endpoints and its request, response formats

<https://documenter.getpostman.com/view/26708611/2sA3dsmDP8>
