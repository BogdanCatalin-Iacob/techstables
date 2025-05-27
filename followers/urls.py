from django.urls import path
from followers import views

urlpatterns = [
    path('likes/', views.FollowerList.as_view())
]
