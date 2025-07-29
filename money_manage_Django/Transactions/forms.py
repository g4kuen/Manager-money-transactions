from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Record, Status, Type, Category, Subcategory


class RecordForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_category'})
    )

    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'})
    )

    class Meta:
        model = Record
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': timezone.now().date().isoformat()
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001'
            }),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None:
            if amount <= 0:
                raise ValidationError("Сумма должна быть положительной")
            if amount > 1_000_000_000:
                raise ValidationError("Сумма слишком большая")
        return amount

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            if date > timezone.now().date():
                raise ValidationError("Дата не может быть в будущем")


            if date.year < 1800:
                raise ValidationError("Дата не может быть раньше 1800 года")
        return date

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = Type.objects.all()


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()