from django.core.validators import MinValueValidator
from django.db import models

from account.models import User

class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_daily_record")
    date = models.DateField()
    exercise_mins = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Exercise Time (Minutes)')
    sleeping_mins = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Sleeping Time (Minutes)')
    meditation_mins = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Meditation Time (Minutes)')
    social_interaction_mins = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Social Interaction Time (Minutes)')
    family_bonding_mins = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Family Bonding Time (Minutes)')
    water_intake = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)], verbose_name='Water Intake (Litre)')

    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Record"
        verbose_name_plural = "Daily Records"

    def __str__(self):
        return f'ID: {self.id}'