For running the celery task, use below line of code


celery -A app.celery worker --pool=solo -l INFO
