from pydantic import BaseModel, model_serializer

class Product(BaseModel):
    name: str
    categories: str | None
    car_name: str | None
    short_description: str | None
    description: str | None
    images: list[str] | None
    attributes: dict

    @model_serializer
    def serialize_model(self):
        base_json = {
            'Name': self.name,
            'Categories': self.categories,
            'Short description': self.short_description if self.short_description else "",
            'Description': self.description if self.description else "",
            'Images': ", ".join(self.images) if self.images else "",
            'meta:car_name': self.car_name,
        }
        attributes_json = {}
        i = 1
        for key, value in self.attributes.items():
            if len(key) > 22:
                continue
            attributes_json.update({f"Attribute {i + 1} name": key, f"Attribute {i + 1} value(s)": value, f"Attribute {i + 1} visible": 1, f"Attribute {i + 1} global": 1})
            i += 1
        return {**base_json, **attributes_json}