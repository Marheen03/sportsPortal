from django.contrib import admin
from .models import *

model_list = [Team, Competition, Match]
admin.site.register(model_list)