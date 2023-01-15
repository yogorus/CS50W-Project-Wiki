from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry>', views.wiki, name='wiki'),
    path('wiki/<str:entry>/edit', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('create', views.create, name="create")
]
