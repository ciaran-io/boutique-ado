from django import forms

from .models import Category, Product
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        # remove image label from form
        self.fields['image'].label = False
        # the current image label is set in widgets.py
        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():

            field.widget.attrs['class'] = 'rounded-md border border-slate-500 px-2 py-3'