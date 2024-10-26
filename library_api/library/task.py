from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Book

@shared_task
def archive_old_books():
    ten_years = timezone.now().date() - timedelta(days=365 * 10)
    book_to_archive = Book.objects.filter(published_date__lt=ten_years, is_archived=False)
    book_to_archive.update(is_archived=True)