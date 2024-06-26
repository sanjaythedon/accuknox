
# Social Media App

This project provides APIs to manage users and the relationship between them which replicates how facebook works.


## Installation

1. Clone the project

```bash
  https://github.com/sanjaythedon/accuknox.git
```
2. Open your command line and go to the project directory.

3. Create a virtual environment
```bash
python -m venv venv
venv/Scripts/activate
```
4. Install all dependencies
```bash
pip install -r requirements.txt
```
5. Migrate all models
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Run the web server
```bash
python manage.py runserver
```
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
