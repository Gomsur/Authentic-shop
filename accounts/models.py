from django.db import models

# To create a Custom User Model and Admin Panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy


# To automatically create Profile or one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

''' A Custom Manager to deal with emails as unique identifier '''
class MyUserManager(BaseUserManager): # BaseUserManager will handle the users which we create. It will inherit BaseUserManager
        
    ''' Creates and saves a user with a given email and password '''
    def _create_user(self, email, password, **extra_fields): # This function will create a normal user.

        if not email:
            raise ValueError("The Email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # This function is to create a Superuser.
    def create_superuser(self, email, password, **extra_fields):
        ''' When the superuser will create then they will be True by default '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)


''' User class or model where we will save our users '''
class User(AbstractBaseUser, PermissionsMixin): # It will inherit AbstractBaseUser and PermissionsMixin.
    email = models.EmailField(unique=True, null=False)

    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False, # By default no user/ normal user will get the permission to be a staff. If he is a superuser then he will get.
        help_text=gettext_lazy('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True, # Every user should be active.
        help_text=gettext_lazy('Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'  # Now Email will be in the place of username.
    objects = MyUserManager() # An object of MyUserManager will be created. Our Custom User Manager.

    def __str__(self):
        return self.email 

    def get_full_name(self):
        return self.email 

    def get_short_name(self):
        return self.email 


''' To create more fields. If we want then we can add more fields in User model. But we will do it here '''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile"

    '''
        This function is to Check that all fields have been filled-up or not.
        And, We will see it's work when we make the payment.

        This is not a built in function. So, we can name it as we want.
    '''
    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()] # All the fields inside the model will come inside fields_names
        
        ''' 
            It will check that Whether any field is empty or not.
            
            Even if a field is empty, it will return False. It will check by Continuing the loop.
            If nothing is empty then it will be out of the loop and will return True.
        '''
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True
    

''' 
    When a new user is created, the profile will be created automatically. Profile will be linked with the user.

    When the receiver receives a signal that an User model has been created, the create_profile function will be the figure. 
    This create_profile function will receive User model means sender, instance, created. 
    If created is True, means the User Model is actually created, then an object of the profile will be created automatically.
'''
@receiver(post_save, sender=User) # If User model send any signal that i(User model) saved then create_profile function will be called.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # profile is the related_name of user field in Profile model.