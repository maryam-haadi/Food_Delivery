from rest_framework import filters


class RestaurantCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category')

        if category:
            return queryset.filter(restaurant__category=category)

        return queryset


class DescendingOrderingFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, *args, **kwargs):
        # Get the default ordering
        ordering = super().get_ordering(request, queryset, *args, **kwargs)

        # Filter out ascending orders
        if ordering:
            ordering = [o for o in ordering if not o.startswith('-')]

        return ordering