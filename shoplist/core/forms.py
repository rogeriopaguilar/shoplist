# -*- coding: utf-8 -*-
import string
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import (ShopList, ListItem, Product)
from shoplist.utils.form_fields import RealCurrencyField

class CurrencyField(forms.DecimalField):
    localize=True


class ShopListForm(forms.ModelForm):

    class Meta:
        model = ShopList
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _(u'Digite o nome da lista…')}),
        }
        exclude = ('created_at',)

    def clean(self):
        super(ShopListForm, self).clean()

        if not self.cleaned_data.get('name'):
            raise forms.ValidationError(
                _(u'Informe o nome da lista de compras.'))

        return self.cleaned_data


class ListItemForm(forms.ModelForm):
    product = forms.CharField(label=_(u"Produto"),
                            widget=forms.TextInput(attrs={'class': 'input-large', 'placeholder': _(u'Produto')}))
    price = RealCurrencyField(label=_(u"Preço"), required=False)

    class Meta:
        model = ListItem
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'quantity input-mini', 'placeholder': _(u'Qtde')}),
        }
        exclude = ('product', 'price')

    def save(self, commit=True):
        item = super(ListItemForm, self).save(commit=False)

        # Get or create Product
        p, product_created = Product.objects.get_or_create(name=string.capwords(self.cleaned_data.get('product')))

        item.product = p
        item.price = self.cleaned_data.get('price')

        if commit:
            item.save()
        return item

