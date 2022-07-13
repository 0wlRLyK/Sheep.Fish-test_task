from django.urls import path, include
from . import views

app_name = "app"
urlpatterns = [
    path('', views.CardsListView.as_view(), name="cards_list"),
    path('<int:pk>/', views.CardsDetailView.as_view(), name="card"),
]