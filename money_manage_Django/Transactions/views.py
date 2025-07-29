from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from .models import Record, Subcategory, Status, Type, Category
from .filters import RecordFilter
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db.models import ProtectedError

MODEL_MAP = {
    'statuses': {'model': Status, 'form': StatusForm},
    'types': {'model': Type, 'form': TypeForm},
    'categories': {'model': Category, 'form': CategoryForm},
    'subcategories': {'model': Subcategory, 'form': SubcategoryForm},
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

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('model') not in MODEL_MAP:
            raise Http404("Справочник не найден")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        model_data = MODEL_MAP.get(self.kwargs['model'])
        if not model_data:
            raise Http404("Модель не найдена")
        return model_data['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_data = MODEL_MAP.get(self.kwargs['model'])
        context.update({
            'model_name': self.kwargs['model'],
            'model_verbose_name': model_data['model']._meta.verbose_name,
            'model_verbose_name_plural': model_data['model']._meta.verbose_name_plural,
            'show_type_column': model_data['model'].__name__ == 'Category',
            'show_category_column': model_data['model'].__name__ == 'Subcategory',
        })
        return context


class DictionaryCreateView(CreateView):
    template_name = 'transactions/generic_form.html'

    def get_form_class(self):
        return MODEL_MAP[self.kwargs['model']]['form']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_data = MODEL_MAP[self.kwargs['model']]
        context.update({
            'model_name': self.kwargs['model'],
            'model_verbose_name': model_data['model']._meta.verbose_name,
            'model_verbose_name_plural': model_data['model']._meta.verbose_name_plural,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})


class DictionaryUpdateView(UpdateView):
    template_name = 'transactions/generic_form.html'

    def get_queryset(self):
        return MODEL_MAP[self.kwargs['model']]['model'].objects.all()

    def get_form_class(self):
        return MODEL_MAP[self.kwargs['model']]['form']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_data = MODEL_MAP[self.kwargs['model']]
        context.update({
            'model_name': self.kwargs['model'],
            'model_verbose_name': model_data['model']._meta.verbose_name,
            'model_verbose_name_plural': model_data['model']._meta.verbose_name_plural,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})


class DictionaryDeleteView(DeleteView):
    template_name = 'transactions/generic_confirm_delete.html'

    def get_queryset(self):
        return MODEL_MAP[self.kwargs['model']]['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_data = MODEL_MAP[self.kwargs['model']]


        obj = self.get_object()
        related_records = []
        if hasattr(obj, 'record_set'):
            related_records = list(obj.record_set.all())

        context.update({
            'model_name': self.kwargs['model'],
            'model_verbose_name': model_data['model']._meta.verbose_name,
            'model_verbose_name_plural': model_data['model']._meta.verbose_name_plural,
            'protected_objects': related_records,
            'has_protected_objects': bool(related_records),
        })
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        if hasattr(self.object, 'record_set') and self.object.record_set.exists():
            messages.error(
                request,
                f"Невозможно удалить '{self.object}', так как существуют связанные записи. "
                "Сначала удалите или измените эти записи."
            )
            return redirect(success_url)

        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            protected_objects = list(e.protected_objects)
            messages.error(
                request,
                f"Невозможно удалить '{self.object}'. "
                f"Найдено связанных записей: {len(protected_objects)}. "
                "Сначала удалите или измените эти записи."
            )
            return redirect(success_url)

    def get_success_url(self):
        return reverse_lazy('dictionary_list', kwargs={'model': self.kwargs['model']})