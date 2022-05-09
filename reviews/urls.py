from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path('', views.feed, name='review-home'),
    path('posts/', views.posts, name='post-home'),
    path('reviews/new/', views.create_review, name='review-create'),
    path('tickets/new/', views.create_ticket, name='ticket-create'),
    path('reviews/<int:pk>/update/', views.update_review, name='review-update'),
    path('tickets/<int:pk>/update/', views.update_ticket, name='ticket-update'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='review-delete'),
    path('tickets/<int:pk>/delete/', views.delete_ticket, name='ticket-delete'),
    path('tickets/answer/<int:pk>/', views.answer_ticket, name='ticket-answer'),
    path('tickets/response/<int:pk>', views.response_ticket, name='ticket-response'),
]
