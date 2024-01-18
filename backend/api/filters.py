from rest_framework.filters import SearchFilter


class OrganizationTitleFilter(SearchFilter):
    """Фильтр для поиска организаций по названию."""

    search_param = 'title'
