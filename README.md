# Alerts

Alerts is a django based web application that scrarpes your notifications from sites like Youtube, Linkedin, Medium and Reddit.
![Alerts home page](https://github.com/robinttt333/Alerts/blob/master/Screenshot%20from%202020-08-18%2017-47-34.png)

## Getting Started
To get a local copy up and running follow these simple example steps.

### Prerequisites
Ensure that you have these installed on your system
* python
* pip

### Installation
1. Clone the repository by typing 
``` 
git clone https://github.com/robinttt333/Alerts 
```
in your terminal. Next **cd** into **Alerts** directory and type in 
```
pip install requirements.txt
```
2. Once the dependencies have been installed, you need to create a **config file** with the name ***config.yml*** . This should be present in the base directory of the project ie where the file ***manage.py*** is situated.
The structure of the file should be as follows:
```yaml
chromeDriver:
        path: path to the chromedriver
geckoDriver:
        path: path to the geckodriver
medium:
        url: https://medium.com/
        email: your **gmail** id for medium
        password: your **gmail** password

reddit:
        clientSecret: your clientSecret
        clientId: your clientId
        userAgent: test

linkedIn:
        url: https://linkedIn.com/
        email: your linkedIn email id
        password: your linkedIn password

youtube:
        url: https://youtube.com/
        email: your **gmail** account for stackoverflow
        password: your **gmail** account password for stackoverflow
        alternateUrl: https://stackoverflow.com/
```
3. Most of the things mentioned here are pretty self explanatory except for the **reddit** section. You will need to visit [here](https://ssl.reddit.com/prefs/apps/) and create a reddit app. You will then get the details.
4. ***Another important thing to note is that youtube and stackoverflow gmail accounts must be same.*** This is because if we try to login directly with selenium google does not allow it due to security reasons.
5. Ensure that you ***RabbitMQ*** is running on port ***5672***.
6. Open a terminal instance and run the django server by typing 
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
7. Open up another terminal instance and start the celery worker by typing in
```sh
celery -A Alerts worker -l info
```
You should see something like this
![celery worker](https://github.com/robinttt333/Alerts/blob/master/Screenshot%20from%202020-08-18%2018-31-29.png)
8. Lastly open up a third terminal instance and type in
```sh
celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
![celery beat](https://github.com/robinttt333/Alerts/blob/master/Screenshot%20from%202020-08-18%2018-33-00.png)

9.In **settings.py** you will have 
```python 
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULE = {
    
    'reddit':{
        'task' : 'reddit.tasks.getHot',
        'schedule' : timedelta(hours=3) 
    },
    'medium':{
        'task' : 'medium.tasks.getUserNotifications',
        'schedule' : timedelta(hours=5) 
    },
    'youtube':{
        'task' : 'youtube.tasks.getUserNotifications',
        'schedule' : timedelta(hours=3) 
    },
    'linkedIn':{
        'task' : 'linkedIn.tasks.getUserNotifications',
        'schedule' : timedelta(hours=3) 
    },
}
```
Change these according to your preferences, however running the script in very short intervals may enable the server to block you or pop up a captcha to verify that you are a human.


