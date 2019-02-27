from django.db import models
from apps.login_register.models import User
from datetime import datetime, timedelta
# Create your models here.


class tripManager(models.Manager):
    def trip_validator(self, PostData):
        errors = {}
        is_valid = True

        if len(PostData['edit_destination']) == 0:
            is_valid = False
            errors['edit_destination'] = "Destination must not be empty"
        if len(PostData['edit_destination']) != 0:
            if len(PostData['edit_destination']) < 3:
                is_valid = False
                errors['edit_destination'] = "Destination must be longer than 3 characters"

        if len(PostData['edit_plans']) == 0:
            is_valid = False
            errors['edit_plans'] = "Plans cannot be empty"
        if len(PostData['edit_plans']) != 0:
            if len(PostData['edit_plans']) < 3:
                is_valid = False
                errors['edit_plans'] = "Plan must be longer than 3 characters"

        if PostData['edit_start_date'] == "":
            is_valid = False
            errors['edit_start_date'] = "Please enter a date"
        if PostData['edit_start_date'] != "":
            now = datetime.now()
            check = datetime.strptime(PostData['edit_start_date'], '%Y-%m-%d')
            if check <= now:
                is_valid = False
                errors['edit_start_date'] = "Start Date must be in the future"

        if PostData['edit_end_date'] == "":
            is_valid = False
            errors['edit_end_date'] = "Please enter a date"
        if PostData['edit_end_date'] != "":
            now = datetime.now()
            check = datetime.strptime(PostData['edit_end_date'], '%Y-%m-%d')
            if check <= now:
                is_valid = False
                errors['edit_end_date'] = "End Date must be in the future"

        if datetime.strptime(PostData['edit_end_date'], '%Y-%m-%d') <= datetime.strptime(PostData['edit_start_date'], '%Y-%m-%d'):
            is_valid = False
            errors['end_date'] = "End date must be after the start date. "

        if is_valid == False:
            return errors

    def create_validator(self, PostData):
        errors = {}
        is_valid = True

        if len(PostData['destination']) == 0:
            is_valid = False
            errors['destination'] = "Destination must not be empty"
        if len(PostData['destination']) != 0:
            if len(PostData['destination']) < 3:
                is_valid = False
                errors['destination'] = "Destination must be longer than 3 characters"

        if len(PostData['plans']) == 0:
            is_valid = False
            errors['plans'] = "Plans cannot be empty"
        if len(PostData['plans']) != 0:
            if len(PostData['plans']) < 3:
                is_valid = False
                errors['plans'] = "Plan must be longer than 3 characters"

        if PostData['start_date'] == "":
            is_valid = False
            errors['start_date'] = "Please enter a date"
        if PostData['start_date'] != "":
            now = datetime.now()
            check = datetime.strptime(PostData['start_date'], '%Y-%m-%d')
            if check <= now:
                is_valid = False
                errors['start_date'] = "Start Date must be in the future"

        if PostData['end_date'] == "":
            is_valid = False
            errors['end_date'] = "Please enter a date"
        if PostData['end_date'] != "":
            now = datetime.now()
            check = datetime.strptime(PostData['end_date'], '%Y-%m-%d')
            if check <= now:
                is_valid = False
                errors['end_date'] = "End Date must be in the future"

        if datetime.strptime(PostData['end_date'], '%Y-%m-%d') <= datetime.strptime(PostData['start_date'], '%Y-%m-%d'):
            is_valid = False
            errors['end_date'] = "End date must be after the start date. "

        if is_valid == False:
            return errors





class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, related_name = "created_trip")
    attendes = models.ManyToManyField(User, related_name = "attending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = tripManager()
