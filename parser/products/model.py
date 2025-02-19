from pydantic import BaseModel, model_serializer

class Product(BaseModel):
    name: str
    short_description: str | None
    description: str | None
    images: list[str] | None
    attributes: dict

    @model_serializer
    def serialize_model(self):
        return {
            'Name': self.name,
            'Short description': self.short_description if self.short_description else "",
            'Description': self.description if self.description else "",
            'Images': ", ".join(self.images) if self.images else "",
            'attributes': self.attributes
        }