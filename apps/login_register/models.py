from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        is_valid = True
        #FIRST NAME VALIDATIONS
        if len(postData['first_name']) == 0:
            is_valid = False
            errors['first_name'] = "Field cannot be empty"
        if len(postData['first_name']) != 0:
            if not str.isalpha(postData['first_name']):
                is_valid = False
                errors['first_name'] = "Field can only conatin letters"
            if str.isalpha(postData['first_name']):
                if len(postData['first_name']) < 2:
                    is_valid = False
                    errors['first_name'] = "Name must be longer than 2 characters"
                if len(postData['first_name']) > 100:
                    is_valid = False
                    errors['first_name'] = "Name cannot be longer that 100 characters"

        #LAST NAME VALIDATIONS
        if len(postData['last_name']) == 0:
            is_valid = False
            errors['last_name'] = "Field cannot be empty"
        if len(postData['last_name']) != 0:
            if not str.isalpha(postData['last_name']):
                is_valid = False
                errors['last_name'] = "Field can only conatin letters"
            if str.isalpha(postData['last_name']):
                if len(postData['last_name']) < 2:
                    is_valid = False
                    errors['last_name'] = "Name must be longer than 2 characters"
                if len(postData['last_name']) > 100:
                    is_valid = False
                    errors['last_name'] = "Name cannot be longer that 100 characters"


        #EMAIL VALIDATIONS
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['email']) == 0:
            is_valid = False
            errors['email'] = "Field cannot be empty"
        if len(postData['email']) != 0:
            if not EMAIL_REGEX.match(postData['email']):
                is_valid = False
                errors['email'] = "Must be a valid email"
            if EMAIL_REGEX.match(postData['email']):
                is_email_taken = User.objects.filter(email = postData['email'])
                if len(is_email_taken) != 0:
                    is_valid = False
                    errors['email'] = "Email already taken, sorry" 

        # REGISTRATION PASSWORD VALIDATIONS
        if len(postData['password']) == 0:
            is_valid = False
            errors['password'] = "Password cannot be empty "
        if len(postData['password']) != 0:
            if len(postData['password']) < 8:
                is_valid = False
                errors['password'] = "Password must be at least 8 characters"

        # REGISTRATION CONFIRM PASSWORD VALIDATIONS
        if len(postData['confirm_pass']) == 0:
            is_valid = False
            errors['confirm_pass'] = "Password cannot be empty "
        if len(postData['confirm_pass']) != 0:
            if len(postData['confirm_pass']) < 8:
                is_valid = False
                errors['confirm_pass'] = "Password must be at least 8 characters"

        # COMPARE PASSWORDS VALIDATIONS
        if postData['password'] != postData['confirm_pass']:
            is_valid = False
            errors['password'] = "Passwords must match"
            errors['confirm_pass'] = "Passwords must match"
        
        if is_valid == False:
            return (False, errors)
        if is_valid == True:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed_password )
            return(True, new_user)

        

#########################################################################################################
#LOGIN VALIDATIONS
#########################################################################################################
        
    def login_validator(self,postData):
        errors = {}
        #LOGIN EMAIL VALIDATIONS
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        is_valid = True
        
        if len(postData['login_email']) == 0:
            is_valid = False
            errors['login_email'] = "Field cannot be empty"
        if len(postData['login_email']) != 0:
            if not EMAIL_REGEX.match(postData['login_email']):
                is_valid = False
                errors['login_email'] = "Must be a valid email"
            if EMAIL_REGEX.match(postData['login_email']):
                is_registered = User.objects.filter(email = postData['login_email'])
                if len(is_registered) == 0:
                    is_valid = False
                    errors['login_email'] = "This email is not registered"
                    print(errors)




        #LOGIN PASSWORD VALIDATIONS
        if len(postData['login_password']) == 0:
            is_valid = False
            errors['login_password'] = "Password cannot be empty "
        if len(postData['login_password']) != 0:
            if len(postData['login_password']) < 8:
                is_valid = False
                errors['login_password'] = "Password must be at least 8 characters"
            if len(postData['login_password'])>= 8:
                user = User.objects.filter(email = postData['login_email']).values()
                if len(user) == 0:
                    is_valid = False
                    errors['login_email'] = "Email field is case sensitive"
                if len(user) != 0 :
                    pw_hash = user[0]['password']
                    if not bcrypt.checkpw(postData['login_password'].encode(), pw_hash.encode()):
                        is_valid = False
                        errors['login_password'] = "Incorrect password"

        if is_valid == False:
            return errors
        if is_valid == True:
            is_registered

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"id: {self.id}, First Name: {self.first_name}, Last Name:  {self.last_name}, Email: {self.email}, Password: {self.password}"


