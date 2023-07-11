from flask import Flask
from celery import Celery
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

# Create Celery instance
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Create Celery beat scheduler
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'app.send_email',
        'schedule': timedelta(seconds=30),
        'args': ('hariom@simprosys.com', 'Hello', 'This is a test email.'),
    },
}

# Update Celery configuration with the schedule
celery.conf.beat_schedule = CELERYBEAT_SCHEDULE 

@celery.task
def send_email(recipient, subject, message):
    # Add your email sending logic using SMTP here
    # Example code:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender=os.environ.get("sender")
    password=os.environ.get("password")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

@app.route('/send')
def schedule_email_task():
    recipient = os.environ.get("sender")
    subject = 'Hello'
    message = 'This is a test email.'

    # Schedule the task to be executed asynchronously by Celery
    send_email.delay(recipient, subject, message)

    return 'Email scheduled for sending.'

if __name__ == '__main__':
    app.run(debug=True)
