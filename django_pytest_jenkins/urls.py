"""
URL configuration for django_pytest_jenkins project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from first_app.views import do_stuff
from second_app.views import do_other_stuff

urlpatterns = [
    path('do-stuff/<int:stuff_id>', do_stuff, name='do-stuff'),
    path('do-other-stuff/<int:stuff_id>', do_other_stuff, name='do-other-stuff'),
    path('admin/', admin.site.urls),
]
