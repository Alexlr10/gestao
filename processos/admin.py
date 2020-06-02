from django.contrib import admin
from .models import Cliente, Ata
from .forms import *

admin.site.register(Cliente)
admin.site.register(Ata)
