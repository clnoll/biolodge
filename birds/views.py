from django.shortcuts import render


def get_birds(request):
    data = {}
    return render(request, 'birds/birds.html', data)
