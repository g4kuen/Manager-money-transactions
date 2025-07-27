from django.shortcuts import render
from .models import Record

def record_list(request):
    records = Record.objects.all()
    return render(request, 'transactions/records_list.html', {'records': records})


