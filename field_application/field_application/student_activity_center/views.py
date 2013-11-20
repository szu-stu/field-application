from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS

from field_application.student_activity_center.forms \
        import StudentActivityCenterApplicationForm
from field_application.student_activity_center.models \
        import StudentActivityCenterApplication


class ApplyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 
                      'student_activity_center/apply.html', 
                      {'form': StudentActivityCenterApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = StudentActivityCenterApplicationForm(request.POST,
                                                    request.FILES)
        if not form.is_valid():
            return render(request, 'student_activity_center/apply.html',
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_table(request):
    table = StudentActivityCenterApplication.generate_table()
    return render(request, 'student_activity_center/table.html',
                  {'table': table})


def display_listing(request):
    listing = StudentActivityCenterApplication.objects.all()
    return render(request, 'student_activity_center/listing.html',
                  {'listing': listing})
