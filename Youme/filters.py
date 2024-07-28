import django_filters

from .forms import *


class UserFilter(django_filters.FilterSet):
    body_type = django_filters.MultipleChoiceFilter(
        choices=Profile.BodyTypeChoices.choices,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Profile
        fields = {
            'age': ['lt', 'gt'],
            'sex': ['exact'],
            'orientation': ['exact'],
            # 'body_type':['exact'],  
            'location': ['icontains'],
            'hobbies': ['icontains'],
        }
