from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from datetime import datetime
from django.core.validators import MaxValueValidator , MinValueValidator
from django_currentuser.db.models import CurrentUserField
# Create your models here.

# Create Book models .

Book_Ranking = (
        ('action', 'Action and Adventure'),
        ('classics', 'Classics'),
        ('novel', 'Comic Book or Graphic Novel'),
        ('detective', 'Detective and Mystery'),
        ('fantasy', 'Fantasy'),
        ('historical', 'Historical Fiction'),
        ('horror', 'Horror'),
        ('literary', 'Literary Fiction'),
        ('cookbooks', 'Cookbooks')
    )

class Book(models.Model):
    name= models.CharField(max_length=20 ,
    verbose_name= "Name of a book")
    image = models.TextField(null= True)
    description = models.TextField(
    verbose_name= "Abstract on a book")
    book_type = models.CharField(max_length=20,
    choices=Book_Ranking, 
    null= True)
    name_auther = models.CharField(max_length=20,
    verbose_name= "Auther Name",
    null= True)
    release_date = models.DateField(null= True)

    def __str__(self):
        return self.name

# Create Comment models .
Status_type = (
        ('a', 'Apparent'),
        ('b', 'Hidden')
)

class Comment(models.Model):
    book = models.ManyToManyField(Book, related_name='comments' , null= True)
    user =  models.ForeignKey(User, related_name='comments' ,on_delete=models.CASCADE, null= True)
    name = models.CharField(max_length=20, null= True)
    comment = models.TextField(max_length=120)
    date_added = models.DateTimeField(auto_now_add=True , null = True)
    status = models.CharField(max_length=20,
    choices=Status_type, 
    null= True)

    def __str__(self):
        # return self.comment
        return '%s - %s' % (self.book , self.comment)

# Create Rating models .
class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_rating' )
    user = models.ForeignKey(User , related_name="user_rating" , on_delete=models.CASCADE)
    score = models.IntegerField(default=0, 
    validators=[
        MaxValueValidator(5),
        MinValueValidator(0),
    ])

    def __str__(self):
        return str(self.score)

# Create Profile models .
choices = (
    ('male'  , 'male'),
    ('female' , 'female')
    )
class Profile(models.Model):
    About_me =models.TextField(null= True)
    birth_date=models.DateField(null= True)
    Gender=models.CharField( max_length=255, choices=choices , null=True)
    countries = CountryField(multiple=True , default='Saudi Arabia')
    image = models.ImageField(upload_to ="img/" , null=True ) 
    name =models.TextField(null= True)
    publisher = models.BooleanField(default=False)
    user_status = models.BooleanField(default=False)
    user = models.OneToOneField(User , related_name="profile" , on_delete=models.CASCADE)
    fav_books = models.ManyToManyField(Book ,related_name='users' , null=True )
    wantToRead = models.ManyToManyField(Book ,related_name='want_to_read' , null=True )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance , id =instance.id )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()