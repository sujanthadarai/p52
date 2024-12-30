from django.db import models

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Momo(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.DecimalField(decimal_places=2,max_digits=8)
    image=models.ImageField(upload_to="Momo_images") #pip install pillow
