from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Table, Worker, AllWorkers
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TableForm, WorkerForm
from django.forms import formset_factory
from django import forms
from .utils.test import generate_graphic
import calendar


DAYS = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')


def index(request, pk=None):
    template_name = 'app/index.html'
    user = request.user
    if user.is_authenticated:
        tables = Table.objects.filter(owner=user)
        if tables.exists():
            context = {'tables': tables}
           
            if pk:
                main = tables.get(pk=pk)
                workers = main.allworkers.all()
                month = main.date.month
                year = main.date.year
                days = calendar.monthrange(year, month)[1]
                first = calendar.weekday(year, month, 1)
                w = [DAYS[(first+i)%7] for i in range(days)]
                context['main'] = main
                context['workers'] = workers
                context['days'] = w
            return render(request, template_name, context)
        return redirect('main:create')
    return redirect('login')


class CreateTable(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'app/table.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def create_worker(request):
    if request.user.is_authenticated:
        WorkerFormSet = formset_factory(WorkerForm, extra=10)
        if request.method == 'POST':
            formset = WorkerFormSet(request.POST)
            count = Worker.objects.filter(owner=request.user).count()
            if count < 6:
                formset.is_valid()
            for form in formset:
                print(2)
                form.instance.owner = request.user
                if form.has_changed():
                    form.save()
            return redirect('main:index')
        
        formset = WorkerFormSet()
        context = {'formset': formset}
        return render(request, 'app/worker.html', context)
    return redirect('login')
    


def create_graphic(request, pk):
    if request.user.is_authenticated:
        table = Table.objects.get(pk=pk)
        workers = Worker.objects.filter(owner=request.user)
        if workers.count() < 6:
            print(workers)
            return create_worker(request)
        generate_graphic(workers, table)
        return index(request, pk)
    return redirect('login')

def choise(request):
    if request.user.is_authenticated:
        template_name = 'app/choise.html'
        all = Worker.objects.filter(owner=request.user)
        context = {'all': all}
        return render(request, template_name, context)
    return redirect('login')

def delete(request, pk):
    if request.user.is_authenticated:
        Worker.objects.get(pk=pk).delete()
        return redirect('main:choise')
        
    return redirect('login')

    