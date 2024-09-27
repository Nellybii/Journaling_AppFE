from django.contrib import admin

from .models import Category, JournalEntry

admin.site.register(Category)
admin.site.register(JournalEntry)


