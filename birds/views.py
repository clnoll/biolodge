from django.shortcuts import render
from birds.models import Subspecies


def get_birds(request):
    headers = [field.name for field in Subspecies._meta._fields()]
    body = Subspecies.objects.values_list(*headers)

    data = {
        'header': headers,
        'body': body,
    }
    return render(request, 'birds/birds.html', data)
