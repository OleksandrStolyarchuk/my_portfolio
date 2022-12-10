from django import forms

from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']

    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        surname = data.get('surname')
        qs = Author.objects.filter(surname__icontains=surname).filter(name__icontains=name)
        if qs.exists():
            self.add_error('name', f'Author {name} {surname} already exists. Please insert another author')

        return data
