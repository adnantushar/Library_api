from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.CharField(max_length=100)
    published_date = models.DateField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class BookLog(models.Model):
    book_title = models.CharField(max_length=250)
    book_author = models.CharField(max_length=200)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_title + "log_" + self.action 
    

    