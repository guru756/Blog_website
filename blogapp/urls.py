from . import views
from django.urls import path
urlpatterns = [
    path("show/",views.show,name='show')
]