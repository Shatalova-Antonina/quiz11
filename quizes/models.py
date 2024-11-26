from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Quiz(models.Model):

    STATUS_CHOICES = [
        ("", "All"),
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="medium")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('quizes:quiz-detail', kwargs={'pk': self.pk})

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('image', 'Image')])
    correct_answer = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text