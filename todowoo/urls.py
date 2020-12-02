from django.contrib import admin
from django.urls import path

from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('current/', views.currenttodos, name='currenttodos')
]
