from typing import Type, Optional, Dict, Union
from django.db.models import Model, QuerySet
from base import selectors
from base.exceptions import CustomException

def model_update(
    model_cls: Type[Model],
    item_id: int,
    allowed_fields: list,
    update_params: Optional[Dict[str, Union[str, int]]] = None,
) -> QuerySet[Model]:
    try:
        instance = selectors.get_specific_object(model_cls, item_id)

    except model_cls.DoesNotExist as exc:
        raise CustomException(exc)

    if update_params:
        for field_name, new_value in update_params.items():
            if getattr(instance, field_name) == new_value:
                continue

            if field_name not in allowed_fields:
                continue

            setattr(instance, field_name, new_value)
        instance.full_clean()
        instance.save()
    return instance
