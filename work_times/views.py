import datetime
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View

from work_times.forms import ProjectForm, WorkTimeForm
from work_times.models import Project, WorkTime


# project views
class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user.is_staff


class ProjectListView(ListView):
    model = Project
    template_name = "project_list.html"
    context_object_name = "projects"


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_form.html"
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user.is_staff


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "delete_project.html"
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user.is_staff

# work time views
class WorkTimeListView(LoginRequiredMixin, ListView):
    model = WorkTime
    template_name = "work_time_list.html"
    context_object_name = "work_times"

    def get_queryset(self):
        queryset = WorkTime.objects.filter(user=self.request.user).order_by('-start_time')

        # Optional project filter
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        # Optional date range filter
        start_date_str = self.request.GET.get('start')
        end_date_str = self.request.GET.get('end')

        if not start_date_str and not end_date_str:
            # Default to today if both are missing
            today = datetime.date.today()
            start_datetime = datetime.datetime.combine(today, datetime.time.min)
            end_datetime = datetime.datetime.combine(today, datetime.time.max)
            queryset = queryset.filter(start_time__range=(start_datetime, end_datetime))
        else:
            # Filter by given range, if any
            if start_date_str:
                try:
                    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
                    queryset = queryset.filter(start_time__gte=start_datetime)
                except ValueError:
                    pass

            if end_date_str:
                try:
                    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
                    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
                    queryset = queryset.filter(start_time__lte=end_datetime)
                except ValueError:
                    pass

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


class WorkTimeCreateView(LoginRequiredMixin, CreateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'work_time_form.html'

    def get_queryset(self):
        return WorkTime.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('work_time_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class WorkTimeUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'work_time_form.html'

    def get_queryset(self):
        return WorkTime.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('work_time_list')


class WorkTimeDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkTime
    template_name = 'delete_work_time.html'

    def get_queryset(self):
        return WorkTime.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('work_time_list')


class CalculateWorkTime(LoginRequiredMixin, View):
    template_name = 'calculate_work_time.html'

    def get(self, request, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        work_times = WorkTime.objects.filter(user=self.request.user, start_time__date=date_obj)

        try:
            results = {}

            for work_time in work_times:
                project_name = work_time.project.name
                project_hex_color = work_time.project.hex_color
                project_description = work_time.description

                if project_name not in results:
                    results[project_name] = {
                        'hex_color': project_hex_color,
                        'minutes': 0,
                        'description': ''
                    }

                results[project_name]['minutes'] += work_time.worked_minutes
                results[project_name]['description'] = f'{project_description} - {results[project_name]["description"]}'

        except TypeError:
            return render(request, self.template_name, {'results': None, 'date': date, 'error': True})

        return render(request, self.template_name, {
            'results': results,
            'date': date
        })