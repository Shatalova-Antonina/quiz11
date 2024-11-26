from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .forms import QuizForm, QuestionForm
from .mixins import UserIsOwnerMixin
from .forms import QuizForm, QuizFilterForm
from .models import Quiz, Question
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class YourView(View):
    def get(self, request):
        # Обробка GET-запиту
        return render(request, 'your_template.html', {})

    def post(self, request):
        # Обробка POST-запиту
        # Наприклад, обробка даних форми
        # Тут ви можете отримати дані з форми через request.POST
        # І виконати потрібні дії (наприклад, збереження в базу даних)
        
        # Перенаправлення або рендеринг
        return redirect('success_url')  # Наприклад, перенаправлення на сторінку успіху

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = models.Quiz
    template_name = "quizes/quiz_form.html"
    form_class = QuizForm
    success_url = reverse_lazy("quizes:quiz-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class QuizListView(ListView):
    model = models.Quiz
    context_object_name = "quizes"
    template_name = "quizes/quiz_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = QuizFilterForm(self.request.GET)
        return context

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = models.Quiz
    context_object_name = "quiz"
    template_name = 'quizes/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Додаємо порожню форму коментаря в контекст
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.quiz = self.get_object()
            comment.save()
            return redirect('quizes:quiz-detail', pk=comment.quiz.pk)
        else:
            # Тут можна обробити випадок з невалідною формою
            pass


class QuizUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Quiz
    form_class = QuizForm
    template_name = "quizes/quiz_update_form.html"
    success_url = reverse_lazy("quizes:quiz-list")


class QuizDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Quiz
    success_url = reverse_lazy("quizes:quiz-list")
    template_name = "quizes/quiz_delete_confirmation.html"


class CustomLoginView(LoginView):
    template_name = "quiz/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "quiz:login"


class RegisterView(CreateView):
    template_name = "quizes/register.html"
    form_class = UserCreationForm
 