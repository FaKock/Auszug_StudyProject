from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
import datetime
from .forms import TaskForm
from .models import Task
from django.urls import reverse_lazy

class Landing(TemplateView):
    template_name = 'Arbeitsprobe/landing.html'  # for highlighting current page

    def get_context_data(self, **kwargs):
        context = super(Landing, self).get_context_data(**kwargs)
        context['task_list'] = Task.objects.all().order_by('deadline_date', 'deadline_time')
        context['done_tasks'] = context['task_list'].filter(complete=True)[:5]
        context['open_tasks'] = context['task_list'].filter(complete=False)
        context['high_prio_task_count'] = context['open_tasks'].filter(priority=3).count()
        context['medium_prio_task_count'] = context['open_tasks'].filter(priority=2).count()
        context['low_prio_task_count'] = context['open_tasks'].filter(priority=1).count()
        return context


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm

    def get_initial(self):
        # deadline init time is the next full hour
        time = datetime.datetime.now() + datetime.timedelta(hours=1)
        minutes = time.minute
        deadline_time = (time - datetime.timedelta(minutes=minutes)).time()
        initial = {
            'deadline_date': datetime.date.today(),
            'deadline_time': deadline_time,
            'duration': datetime.time(0, 30),
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['task_list'] = Task.objects.order_by('deadline_date', 'deadline_time')
        context['done_tasks'] = context['task_list'].filter(complete=True)[:10]
        context['open_tasks'] = context['task_list'].filter(complete=False)
        context['high_prio_task_count'] = context['open_tasks'].filter(priority=3).count()
        context['medium_prio_task_count'] = context['open_tasks'].filter(priority=2).count()
        context['low_prio_task_count'] = context['open_tasks'].filter(priority=1).count()
        return context

    # combines the post data for category and task form
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # adds the user as author of a model instance
    # form is automatically saved afterwards by a predefined method
    def form_valid(self, form):

        # create a task
        form.save()

        messages.success(self.request, 'Task was successfully created!')

        return redirect('landing')

    def form_invalid(self, form, **kwargs):

        context = self.get_context_data(**kwargs)
        form.data = form.data.copy()

        # access the validation error from the forms.py class
        if form.has_error('deadline_date', 'invalid'):
            form.data['deadline_date'] = datetime.date.today()

        elif form.has_error('deadline_time', 'invalid'):
            form.data['deadline_time'] = (datetime.datetime.now() + datetime.timedelta(minutes=1)).time()

        elif form.has_error('duration', 'invalid'):
            form.data['duration'] = datetime.time(0, 5)

        context['form'] = form

        return self.render_to_response(context)


def completeTask(request, **kwargs):
    task = Task.objects.get(pk=kwargs['pk'])
    if not task.complete:
        task.complete = True
    else:
        task.complete = False
    task.save()

    return redirect('landing')
