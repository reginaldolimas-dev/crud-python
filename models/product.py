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
    def fromDict(cls, data: dict):
        return cls(
            name=data["name"],
            price=float(data["price"]),
            quantity=int(data["quantity"])
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
