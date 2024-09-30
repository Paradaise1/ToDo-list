def get_query_set(model_objects, obj):
    """Получить базовый набор объектов."""
    return model_objects.prefetch_related(
        'tags'
    ).select_related('author').filter(author=obj.request.user)  
