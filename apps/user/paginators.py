from apps.core.paginators import StandardResultsSetPagination


class UserAnimeListPaginator(StandardResultsSetPagination):
    page_query_param = 'page'
    page_size = 12
    page_size_query_param = 'page_size'
