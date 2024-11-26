from django import forms
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'status', 'author']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'correct_answer']


class QuizFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус")

    def __init__(self, *args, **kwargs):
        super(QuizFilterForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-control"})