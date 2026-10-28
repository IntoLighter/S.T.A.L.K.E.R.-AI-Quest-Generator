from pydantic import BaseModel, model_validator


class CodeDefaultOptionMixin(BaseModel):
    def code_defaults(self) -> dict[str, object]:
        return {
            name: getattr(self, name)
            for name, field in type(self).model_fields.items()
            if field.exclude
        }


class CodeDefaultSectionMixin(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def seed_code_defaults(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data

        seeded = dict(data)
        for name, field in cls.model_fields.items():
            code_defaults = getattr(field.default, "code_defaults", None)
            if not callable(code_defaults):
                continue

            payload = dict(seeded.get(name) or {})
            seeded[name] = {**payload, **code_defaults()}

        return seeded
