from django.urls import path
from . import views
# from quizes import views
from .views import YourView 

urlpatterns = [
    path("", views.QuizListView.as_view(), name="quiz-list"),
    path('your-path/', YourView.as_view(), name='your_view'),  # Використання as_view()
    path("<int:pk>/", views.QuizDetailView.as_view(), name="quiz-detail"),
    path("quiz-create/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]

app_name = "quizes"