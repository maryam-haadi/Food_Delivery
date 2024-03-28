from rest_framework import filters


class RestaurantCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category')

        if category:
            return queryset.filter(restaurant__category=category)

        return queryset