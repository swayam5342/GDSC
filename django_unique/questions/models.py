from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class QuestionnaireResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question_1 = models.CharField(max_length=255)
    question_2 = models.CharField(max_length=255)
    # Add more fields for other questions
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.user.username if self.user else 'Anonymous'}"
