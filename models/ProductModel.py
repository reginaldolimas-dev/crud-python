import json
from typing import Optional

class ProductModel:
    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        id: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    @classmethod
    def fromDict(cls, data: dict, existente: Optional['ProductModel'] = None):
        if existente:
            return cls(
                id=existente.id,
                name=data.get("name", existente.name),
                price=float(data.get("price", existente.price)),
                quantity=int(data.get("quantity", existente.quantity))
            )
        else:
            return cls(
                name=data["name"],
                price=float(data["price"]),
                quantity=int(data["quantity"]),
                id=data.get("id")
            )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    def toJson(self) -> str:
        return json.dumps(self.toDict())
