from django.shortcuts import render
from django.views.generic import View
from birds.models import Bird


class BirdList(View):

    def get(self, request):
        headers = Bird._meta.get_all_field_names()
        body = Bird.objects.values_list(*headers)

        data = {
            'header': headers,
            'body': body,
        }
        return render(request, 'birds/birds.html', data)
