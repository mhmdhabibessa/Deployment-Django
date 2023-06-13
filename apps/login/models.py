from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData, pageType):
        errors = {}

        if pageType == 'registration':  #Registration Page Checks-
            pattern = re.compile("^[A-Za-z]+$")
            
            if len(postData['reg-fname']) < 1:
                errors['reg-fname'] = "First Name is a required field"
            elif len(postData['reg-fname']) < 3:
                errors['reg-fname'] = "First Name must be at least 3 characters"
            elif not pattern.match(postData['reg-fname']):
                errors['reg-fname'] = "First Name must only contain letters"
            
            if len(postData['reg-lname']) < 1:
                errors['reg-lname'] = "Last Name is a required field"
            elif len(postData['reg-lname']) < 2:
                errors['reg-lname'] = "Last Name must be at least 2 characters"
            elif not pattern.match(postData['reg-lname']):
                errors['reg-lname'] = "Last Name must only contain letters"
            
            pattern = re.compile("^[^\s@]+@[^\s@]+\.[^\s@]+$")

            if len(postData['reg-email']) < 1:
                errors['reg-email'] = "Email is a required field"
            elif not pattern.match(postData['reg-email']):
                errors['reg-email'] = "Please enter a valid email address! \n Example: joe.smith@email.com"
            
            checkEmail = User.objects.filter(email=postData['reg-email'])
            if checkEmail:
                errors['reg-email'] = "A user with this email is already registered. Please enter a different email."
            
            if len(postData['reg-pword']) < 1:
                errors['reg-pword'] = "Password is a required field"
            elif len(postData['reg-pword']) < 8:
                errors['reg-pword'] = "Password must be at least 8 characters"
            elif postData['reg-pword'] != postData['reg-confpw']:
                errors['reg-pword'] = "Passwords DO NOT match!"

        elif pageType == 'update': #Update Page Checks
            pattern = re.compile("^[A-Za-z]+$")

            if len(postData['fname']) < 1:
                errors['fname'] = "First Name is a required field"
            elif len(postData['fname']) < 2:
                errors['fname'] = "First Name must be at least 2 characters"
            elif not pattern.match(postData['fname']):
                errors['fname'] = "First Name must only contain letters"
            
            if len(postData['lname']) < 1:
                errors['lname'] = "Last Name is a required field"
            elif len(postData['lname']) < 2:
                errors['lname'] = "Last Name must be at least 2 characters"
            elif not pattern.match(postData['lname']):
                errors['lname'] = "Last Name must only contain letters"

            if len(postData['pword']) > 0:
                if len(postData['pword']) < 8:
                    errors['pword'] = "Password must be at least 8 characters"
                elif postData['pword'] != postData['conf_pw']:
                    errors['pword'] = "Passwords DO NOT match!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    

class Pie(models.Model):
    name=models.CharField(max_length=255)
    user = models.ForeignKey(User,related_name="pies",on_delete=models.CASCADE)
    filling=models.CharField(max_length=255)
    crust=models.CharField(max_length=255)
    vote = models.ManyToManyField(User, related_name="voted_pies",default=0)

    