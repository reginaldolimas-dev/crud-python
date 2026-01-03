import logging
import traceback
import uuid

from storage.product import ProductStorage
from models.product import ProductModel

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()

    def _validacao(self, produto:ProductModel):
        if not produto.name or not produto.name.strip():
            raise ValueError("Nome do produto é obrigatório")

        if produto.price <= 0:
            raise ValueError("O preço do produto deve ser maior que zero")

        if produto.quantity < 0:
            raise ValueError("A quantidade do produto não pode ser negativa")

    def inserir(self, produto:ProductModel) -> int:
        try:
            self._validacao(produto)
            logging.debug(f"[PRODUCT-SERVICE] Insert Product: {produto.toJson()}")
            produto.id = str(uuid.uuid4())
            self.storage.insert(produto)
            return produto
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")

        return id
            
    def get(self) -> list:
        ret = {}
        try:
            # TODO
            logging.debug(f"[PRODUCT-SERVICE] Get all Products: {len(ret)} found")
        
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
        
        return ret

    def getById(self, id:int) -> ProductModel:
        ret = {}
        try:
            # TODO
            logging.debug(f"[PRODUCT-SERVICE] Get Product by ID: {id}")
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")

        return ret
    
    # TODO UPDATE
    # TODO DELETE