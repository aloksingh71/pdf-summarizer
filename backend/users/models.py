from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class Summary(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    summary_type = models.CharField(max_length=20, choices=[('bullet', 'Bullet'), ('paragraph', 'Paragraph')])
    num_points = models.IntegerField(null=True, blank=True)
    paragraph_length = models.IntegerField(null=True, blank=True)
    summary_text = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.summary_type} summary for {self.uploaded_file.file_name}"