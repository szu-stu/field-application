import logging

from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS

from field_application.campus_field.forms import ExhibitApplicationForm
from field_application.campus_field.forms import PublicityApplicationForm
from field_application.campus_field.models import ExhibitApplication
from field_application.campus_field.models import PublicityApplication


class ApplyExhibitView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'campus_field/apply-exhibit.html', 
                      {'form': ExhibitApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = ExhibitApplicationForm(request.POST,
                                      request.FILES)
        if not form.is_valid():
            return render(request, 'campus_field/apply-exhibit.html', 
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


class ApplyPublicityView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'campus_field/apply-publicity.html', 
                      {'form': PublicityApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = PublicityApplicationForm(request.POST,
                                        request.FILES)
        if not form.is_valid():
            return render(request, 'campus_field/apply-publicity.html', 
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = ExhibitApplication.generate_table(offset=week)
    return render(request, 'campus_field/table.html',
            {'table': table, 'curr_week': week})


def display_listing(request):
    listing = ExhibitApplication.objects.all()
    return render(request, 'campus_field/listing.html',
                  {'listing': listing})
