"""Base model for all models in API server."""

from __future__ import annotations

import time
import typing
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import UUID

import pydantic
# from jsf import JSF # TODO: JSF
from pydantic import UUID4

Model = TypeVar("Model", bound="BaseModel")
_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    def to_json_dict(self, exclude: set = None, **kwargs) -> dict[str, Any]:
        return self.model_dump(
            mode='json',
            exclude=exclude,
            **kwargs
        )

    def migrate(
        self,
        model: type[BaseModel],
        random_fill: bool = False,
        match_keys: dict[str, str] | None = None,
        extra_fields: dict[str, typing.Any] | None = None,
    ) -> Model:
        """Migrate one model to another ignoring missmatch.

        Args:
            model:
                Heir BaseModel object.
            random_fill:
                If True, then the fields that are not in the
                model will be filled with random values.
            match_keys:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the names of the fields of the current model.
                Key: name of field in self-model.
                Value: name of field in a target model.
            extra_fields:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the values of the fields of the current model.

                Key: name of field in a target model.

                Value: value of field in a target model.

        Examples:
            When migrating from model A to model B, the fields that are not
            in model B will be filled with them::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                ...     d: int
                >>> class B(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3, d=4)
                >>> a.migrate(model=B)  # B(a=1, b=2, c=3)

            But if you need to fill in the missing fields with a random value,
            then you can use the ``random_fill`` argument::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> class B(BaseModel):
                ...     a: int
                ...     aa: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, random_fill=True)  # B(a=1, aa=1011, b=2, c=3)

            If you need to migrate fields with different names, then you can use
            the ``match_keys`` argument::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> class B(BaseModel):
                ...     aa: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, match_keys={"aa": "a"})  # B(aa=1, b=2, c=3)

            If you need to add additional fields to the model, then you can use
            the ``extra_fields`` argument::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                >>> class B(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, extra_fields={"c": 3})  # B(a=1, b=2, c=3)


        Returns:
            pydantic model parsed from ``model``.
        """

        self_dict_model = self.to_dict(show_secrets=True)

        if not match_keys:
            match_keys = {}
        if not extra_fields:
            extra_fields = {}

        for key, value in match_keys.items():
            self_dict_model[key] = self_dict_model.pop(value)

        for key, value in extra_fields.items():
            self_dict_model[key] = value

        if not random_fill:
            return pydantic.parse_obj_as(model, self_dict_model)

        # TODO: JSF
        # faker = JSF(model.schema()).generate()
        # faker.update(self_dict_model)
        # return pydantic.parse_obj_as(model, faker)
        return model(**self_dict_model)

    model_config = pydantic.ConfigDict(
        # Allow creating new fields in model.
        validate_by_name=True,

        # Allow validate assignment.
        validate_assignment=True,

        # Remove trailing whitespace
        str_strip_whitespace = True,

        use_enum_values=True,
        # strict=False,
        # arbitrary_types_allowed=True,
    )
