from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book, BookLog

@receiver(post_save, sender=Book)
def log_book_created(sender, instance, created, **kwargs):
    if created:
        BookLog.objects.create(
            book_title=instance.title,
            book_author=instance.author.name,
            action="create"
        )

@receiver(post_delete, sender=Book)
def log_book_delted(sender, instance, **kwargs):
        BookLog.objects.create(
            book_title=instance.title,
            book_author=instance.author.name,
            action="delete"
        )