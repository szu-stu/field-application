#-*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS

from field_application.south_stadium.forms import SouthStadiumApplicationForm
from field_application.south_stadium.models import SouthStadiumApplication


class ApplyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'south_stadium/apply.html', 
                      {'form': SouthStadiumApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = SouthStadiumApplicationForm(request.POST,
                                           request.FILES)
        if not form.is_valid():
            return render(request, 'south_stadium/apply.html',
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = SouthStadiumApplication.generate_table(offset=week)
    return render(request, 'south_stadium/table.html',
                  {'table': table, 'curr_week': week})


def display_message(request):
    app_id = request.POST.get('data-app-id')
    app = SouthStadiumApplication.objects.get(pk=app_id)
    return render(request, 'south_stadium/message.html', {'app', app})


def display_listing(request):
    listing = SouthStadiumApplication.objects.all()
    return render(request, 'south_stadium/listing.html',
                  {'listing': listing})

