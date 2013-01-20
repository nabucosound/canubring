from django import forms

from django_select2 import *

from cities.models import Country, City, Region
from django_select2.util import JSFunctionInContext


class MyModelSelect2Field(ModelSelect2Field):
    def label_from_instance(self, obj):
        return obj.alt_names_es.get_preferred(default=obj.name)

# class CityChoices(AutoModelSelect2Field):
class CityChoices(AutoModelSelect2Field):
    # queryset = City.objects.filter(country__name__icontains='spain')
    # queryset = City.alt_names_es
    queryset = City.objects
    search_fields = ['name__icontains', ]

    def get_results(self, request, term, page, context):
        from django_select2 import NO_ERR_RESP
        res = [(1, 'caca', {}),]
        return (NO_ERR_RESP, False, res)

    # def label_from_instance(self, obj):
    #     return getattr(obj.alt_names_es.get_preferred(default=obj.name), 'name', obj.name)

class NewTrip(forms.Form):
    country = MyModelSelect2Field(queryset=Country.objects)
    caca = CityChoices(
        # label='Issue 11 Test (Employee)',
        widget=AutoHeavySelect2Widget(
            select2_options={
                'width': '32em',
                'ajax': {
                    'dataType': 'json',
                    'quietMillis': 100,
                    'data': JSFunctionInContext('my_url_param_generator'),
                    'results': JSFunctionInContext('django_select2.process_results'),
                }
                # 'placeholder': u"Search foo"
            }
        )
    )
    # caca = ModelSelect2Field(queryset=Region.objects, widget=HeavySelect2Widget())

# CityChoices() # Should already be registered
# CityChoices(auto_id="CityChoices_CustomAutoId") # Should get registered
