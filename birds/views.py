from django.shortcuts import render


def get_birds(request):
    data = {}
    return render('birds.html', data=data)
