from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def checkout(request):
    if request.method == 'POST':
        print (request.POST)
    context = {}
    template = 'checkout.html'
    return render(request, template, context)
