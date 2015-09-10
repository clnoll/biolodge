from django.shortcuts import render
from birds.models import Subspecies


def get_birds(request):
    headers = [field.name for field in Subspecies._meta._fields()]
    vals = Subspecies.objects.values()

    body = []
    for val in vals:
        row_data = []
        for header in headers:
            row_val = val[header]
            row_data.append(row_val)
        body.append(row_data)

    data = {
        'header': headers,
        'body': body,
    }
    return render(request, 'birds/birds.html', data)
