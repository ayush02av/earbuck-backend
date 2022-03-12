from utility.database_utility import *

# extend user model for extra information
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    budget = models.ForeignKey(to="database_main.Budget", on_delete=models.SET_NULL, null=True, blank=True, related_name="userBudget")

    savings = models.IntegerField(default=0)

    investmentPercent = models.FloatField(default=30.0)
    investmentAmount = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.username

    def __get_self_update_object__(self):
        return User.objects.filter(id = self.id)

    def __update_details__(self):
        pass