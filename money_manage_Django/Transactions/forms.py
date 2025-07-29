from django import forms
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
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
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


class DictionaryForm(forms.ModelForm):
    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

        if self.model:
            self.Meta.model = self.model
            if self.model.__name__ == 'Category':
                self.fields['type'].queryset = Type.objects.all()
            elif self.model.__name__ == 'Subcategory':
                self.fields['category'].queryset = Category.objects.all()