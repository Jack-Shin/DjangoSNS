from django.contrib import admin
from .models import *


models = [
    Post,
    Comment,
    Heart,
]

admin.site.register(models)
