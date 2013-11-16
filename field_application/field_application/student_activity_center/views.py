from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from field_application.student_activity_center.forms \
        import StudentActivityCenterApplicationForm


class ApplyView(View):

    def get(self, request):
        return render(request, 
                      'student_activity_center/apply.html', 
                      StudentActivityCenterApplicationForm())

    def post(self, request):
        form = StudentActivityCenterApplicationForm(request.POST)
        if not form.is_valid():
            return render(request, 'student_activity_center/apply.html', form)
        app = form.save(commit=False)
        app.organization = request.user
        app.save()
        return HttpResponseRedirect(reverse('home'))

