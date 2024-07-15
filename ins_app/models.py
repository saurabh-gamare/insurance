from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    ]
    dob = models.DateField()
    gender = models.CharField(max_length=1, 
                              choices=gender_choices
                            )
    mobile = models.CharField(max_length=15, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class PolicyDetail(models.Model):
    premium_frequency_choices = [
        ('y', 'Yearly'),
        ('hy', 'Half-Yearly'),
        ('m', 'Monthly'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sum_assured = models.IntegerField()
    premium = models.IntegerField()
    premium_frequency = models.CharField(
                            max_length=2    , 
                            choices=premium_frequency_choices, 
                            default='yearly'
                        )
    pt = models.IntegerField()
    ptt = models.IntegerField()
    policy_type = models.CharField(max_length=20, null=True, blank=True)
    policy_information = models.TextField(null=True, blank=True)
    riders = models.CharField(max_length=20, null=True, blank=True)
    premium_options = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.profile.user.username
