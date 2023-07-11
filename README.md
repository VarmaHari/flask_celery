For running the celery task, use below line of code
  **celery -A app.celery worker --pool=solo -l INFO**


For running the celery beat scheduler task, use below line of code
 **celery -A app.celery beat -l info**


where app=flask app name
