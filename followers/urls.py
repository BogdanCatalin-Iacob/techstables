from django.urls import path
from followers import views

urlpatterns = [
    path('likes/', views.FollowerList.as_view()),
    path('likes/<int:pk>', views.FollowerDetail.as_view()),
]
