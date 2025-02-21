import datetime
from collections import defaultdict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View

from work_times.forms import ProjectForm, WorkTimeForm
from work_times.models import Project, WorkTime


# project views
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectListView(ListView):
    model = Project
    template_name = "project_list.html"
    context_object_name = "projects"


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_form.html"
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "delete_project.html"
    success_url = reverse_lazy('project_list')


# work time views
class WorkTimeListView(ListView):
    model = WorkTime
    template_name = "work_time_list.html"
    context_object_name = "work_times"

    def get_queryset(self):
        queryset = WorkTime.objects.all().order_by('-start_time')
        project_id = self.request.GET.get('project')  # Optional project filter
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()

        grouped_work_times = defaultdict(list)
        for work_time in self.get_queryset():
            start_date = work_time.start_time.date()
            grouped_work_times[start_date].append(work_time)
        context['grouped_work_times'] = dict(grouped_work_times)

        return context


class WorkTimeCreateView(CreateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'work_time_form.html'

    def get_success_url(self):
        return reverse_lazy('work_time_list')


class WorkTimeUpdateView(UpdateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'work_time_form.html'

    def get_success_url(self):
        return reverse_lazy('work_time_list')


class WorkTimeDeleteView(DeleteView):
    model = WorkTime
    template_name = 'work_time_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('work_time_list', kwargs={'pk': self.object.project.pk})


class CalculateWorkTime(View):
    template_name = 'calculate_work_time.html'

    def get(self, request, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        work_times = WorkTime.objects.filter(start_time__date=date_obj)

        try:
            results = {}

            for work_time in work_times:
                project_name = work_time.project.name
                project_hex_color = work_time.project.hex_color

                if project_name not in results:
                    results[project_name] = {
                        'hex_color': project_hex_color,
                        'minutes': 0
                    }

                results[project_name]['minutes'] += work_time.worked_minutes

        except TypeError:
            return render(request, self.template_name, {'results': None, 'date': date, 'error': True})

        return render(request, self.template_name, {
            'results': results,
            'date': date
        })