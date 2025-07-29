from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RecordForm, DictionaryForm
from .models import Record, Subcategory, Status, Type, Category
from .filters import RecordFilter
from django.http import JsonResponse


MODELS = {
    'statuses': Status,
    'types': Type,
    'categories': Category,
    'subcategories': Subcategory,
}

def create_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm()
    return render(request, 'transactions/record_form.html', {'form': form})

def edit_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'transactions/record_form.html', {'form': form})

def delete_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'transactions/record_confirm_delete.html', {'record': record})

def record_list(request):
    records = Record.objects.all().order_by('-date')
    record_filter = RecordFilter(request.GET, queryset=records)
    return render(request, 'transactions/record_list.html', {
        'filter': record_filter,
        'records': record_filter.qs
    })

def get_subcategories(request, category_id):
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def get_categories(request, type_id):
    categories = Category.objects.filter(type_id=type_id).values('id', 'name','type')
    return JsonResponse(list(categories), safe=False)


class DictionaryListView(ListView):
    template_name = 'transactions/generic_list.html'

    def get_queryset(self):
        model = MODELS.get(self.kwargs['model'])
        return model.objects.all() if model else model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model']
        return context


class DictionaryCreateView(CreateView):
    template_name = 'transactions/generic_form.html'
    form_class = DictionaryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['model'] = MODELS.get(self.kwargs['model'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})


class DictionaryUpdateView(UpdateView):
    template_name = 'transactions/generic_form.html'
    form_class = DictionaryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['model'] = MODELS.get(self.kwargs['model'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})


class DictionaryDeleteView(DeleteView):
    template_name = 'transactions/generic_confirm_delete.html'

    def get_queryset(self):
        model = MODELS.get(self.kwargs['model'])
        return model.objects.all() if model else model.objects.none()

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})