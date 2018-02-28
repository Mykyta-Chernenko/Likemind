import django_filters

from users.models import Person


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'birthday': [
                'exact', 'gte', 'lte',
                'year__exact', 'year__lte', 'year__gte',
                'month__exact', 'month__lte', 'month__gte',
                'day__exact', 'day__lte', 'day__gte'
            ],
            'first_name': [
                'iexact', 'icontains'
            ],
            'last_name': [
                'iexact', 'icontains'
            ],
            'username': [
                'iexact', 'icontains'
            ]
        }
