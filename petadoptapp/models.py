from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class pet(models.Model) :
    name = models.CharField(max_length=100)  
    age= models.IntegerField()
    gender = models.CharField(max_length=6) 
    type=models.CharField(max_length=20,default='')
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')  

class cart(models.Model):
    uid =  models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid') 
    petid = models.ForeignKey(pet,on_delete=models.CASCADE,db_column='petid')
    
class adopt(models.Model):   
    adoptid=models.CharField(max_length=50) 
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    petid=models.ForeignKey(pet,on_delete=models.CASCADE,db_column='petid') 
    adopt_date = models.DateTimeField(auto_now_add=True)  


    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True) 