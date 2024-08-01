from django.urls import path
from .views import register, submit_paper, view_papers, profile, delete_paper, contact, leaderboard_papers, leaderboard_views, increment_view, get_paper_details, rate_paper
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('submit/', submit_paper, name='submit_paper'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('delete-paper/<int:pk>/', delete_paper, name='delete_paper'),
    path('contact/', contact, name='contact'),
    path('analytics/papers/', leaderboard_papers, name='leaderboard_papers'),
    path('analytics/views/', leaderboard_views, name='leaderboard_views'),
    path('increment-view/<int:pk>/', increment_view, name='increment_view'),
    path('get-paper-details/<int:pk>/', get_paper_details, name='get_paper_details'),
    path('rate-paper/<int:pk>/', rate_paper, name='rate_paper'),
    path('', view_papers, name='view_papers'),
]