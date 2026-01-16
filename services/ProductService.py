import logging
import traceback
import uuid

from storage.ProductStorage import ProductStorage
from models.ProductModel import ProductModel

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

    def inserir(self, dados: dict) -> int:
        try:
            if not dados:
                raise ValueError("Dados do produto são obrigatórios")
            produto = ProductModel.fromDict(dados)
            self._validacao(produto)
            logging.debug(f"[PRODUCT-SERVICE] Insert Product: {produto.toJson()}")
            produto.id = str(uuid.uuid4())
            self.storage.insert(produto)
            return produto
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")

        return id
            
    def buscar(self) -> list:
        try:
            ret = self.storage.get()
            logging.debug(f"[PRODUCT-SERVICE] Get all Products: {len(ret)} found")
        
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
        
        return ret

    def buscarPorId(self, id:int) -> ProductModel:
        try:
            produto = self.storage.getById(id)
            if produto is None:
                logging.debug(f"[PRODUCT-SERVICE] Produto com ID {id} não encontrado")
                raise ValueError(f"Produto com ID {id} não encontrado")
            logging.debug(f"[PRODUCT-SERVICE] Get Product by ID: {id}")
            return produto
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
            return None

        return ret
    
    def atualizar(self, id: int, dados: dict) -> ProductModel:
        try:
            existente = self.storage.getById(id)
            if existente is None:
                logging.debug(f"[PRODUCT-SERVICE] Produto {id} não encontrado para atualização")
                return None

            produto_atualizado = ProductModel.fromDict(dados, existente=existente)

            self._validacao(produto_atualizado)
            logging.debug(f"[PRODUCT-SERVICE] Atualizando Produto ID {id}: {produto_atualizado.toJson()}")

            atualizado = self.storage.update(id, produto_atualizado)
            if not atualizado:
                return None

            return produto_atualizado
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
            raise

    def deletar(self, id: int) -> bool:
        try:
            apagou = self.storage.delete(id)
            if not apagou:
                logging.debug(f"[PRODUCT-SERVICE] Produto {id} não encontrado para exclusão")
            else:
                logging.debug(f"[PRODUCT-SERVICE] Produto {id} excluído com sucesso")
            return apagou
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
            raise