from django.shortcuts import render


def get_birds(request):
    header = ['field', 'another', 'third']
    body = [['b1', 'b2', 'b3'],
            ['a', 'b', 'c'],
            ['afd', 'adfasdf', 'adfasdfasf']]
    data = {
        'header': header,
        'body': body,
    }
    return render(request, 'birds/birds.html', data)
