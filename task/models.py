from django.db import models
from account.models import BaseModel

class Task(BaseModel):
    status_choices = [
        ("started", "Started"),
        ("progress", "progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    priority_choices = [
        (0, "Low"),
        (1, "Medium"),
        (2, "High"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=status_choices, default="started")
    priority = models.IntegerField(choices=priority_choices, default=0)  # Fixed default value
    due_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    repeat = models.BooleanField(default=False)
    repeat_interval = models.IntegerField(default=0)  # Interval in days
    sub_task = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="sub_tasks"
    )

    def __str__(self):
        return self.title

class Files(BaseModel):
    file = models.FileField(upload_to='tasks/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.file.name

class Notification(BaseModel):
    notification_types = [
        ("info", "Info"),
        ("warning", "warning"),
        ("error", "Error")
    ]
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    message = models.TextField()

    notification_type = models.CharField(max_length=20, choices=notification_types)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"

class Remainder(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.reminder_date}"
