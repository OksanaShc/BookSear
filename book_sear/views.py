from django.shortcuts import render, render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import SearchForm
from es.helper import ElasticHelper


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data['target_text']
            e_mail = form.cleaned_data['e_mail']
            es = ElasticHelper()
            message = es.make_search(text)
            send_email(to_email=e_mail, message=message, )
            return render_to_response('search_app/search_started.html', {
                'e_mail': e_mail})
        else:
            return HttpResponseBadRequest('Such fields contain errors: %s' % form.errors)
    else:
        form = SearchForm()

    return render(request, 'search_app/search.html', {
        'form': form,
    })


def send_email(to_email, message, subject='search results'):
    if to_email and message:
        try:
            send_mail(subject, message, 'search@search.com', [to_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    else:
        return HttpResponseBadRequest('Make sure all fields are entered and valid.')


def search_started(request):
    return render_to_response('search_app/search_started.html')
