def get_query_set(model_objects, obj):
    '''Method to get basic queryset.'''
    return model_objects.prefetch_related(
        'tags'
    ).select_related('author').filter(author=obj.request.user)
