from django.shortcuts import render
from django.views.generic import View
from birds.models import Subspecies


class BirdList(View):

    def get(self, request):
        headers = [field for field in Subspecies._meta.get_all_field_names()]
        body = Subspecies.objects.values_list(*headers)

        data = {
            'header': headers,
            'body': body,
        }
        return render(request, 'birds/birds.html', data)
