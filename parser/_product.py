from pydantic import BaseModel, model_serializer

class Product(BaseModel):
    name: str
    short_description: str | None
    images: list[str] | None

    @model_serializer
    def serialize_model(self):
        return {
            'Name': self.name,
            'Short description': self.short_description if self.short_description else "",
            'Images': ", ".join(self.images) if self.images else ""
        }