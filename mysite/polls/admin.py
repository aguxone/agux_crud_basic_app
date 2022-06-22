from django.contrib import admin

# Register your models here.

# WE HAVE TO TELL that Django that some OBJECTS can be accesed
# via admin interface! Like te question column in polls app!

from .models import Question

admin.site.register(Question)