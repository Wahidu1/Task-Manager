from django.urls import path
from task.views import home
app_name = 'task'

urlpatterns = [
    path("", home, name="home"),
]