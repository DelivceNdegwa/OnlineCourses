from typing import Optional


def get_model_field_names(model_cls, exclude: Optional[list]=None) -> list:
    fields = model_cls._meta.get_fields()
    if exclude:
        return [field.name for field in fields if field.name not in exclude]
    return [field.name for field in fields]