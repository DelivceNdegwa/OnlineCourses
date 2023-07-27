from typing import Type, Optional, Dict, Union
from django.db.models import Model, QuerySet


def get_objects(
    model_cls: Type[Model],
    filter_params: Optional[Dict[str, Union[str, int]]] = None,
    allowed_fields: Optional[list] = None,
    additional_fields: Optional[list] = None
) -> QuerySet[Model]:
    if filter_params and allowed_fields:
        if additional_fields:
            allowed_fields += additional_fields
        allowed_params = {field: value for field, value in filter_params.items() if field in allowed_fields}
        return model_cls.objects.filter(**allowed_params)
    return model_cls.objects.all()


def get_specific_object(model_cls: Type[Model], id) -> Type[Model]:
    try:
        model = model_cls.objects.get(id=id)
        return model
    except model_cls.DoesNotExist:
        raise


def get_current(model_cls: Type[Model]) -> Type[Model]:
    return model_cls.objects.all().first()
