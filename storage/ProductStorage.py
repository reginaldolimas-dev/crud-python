import logging
import sqlite3
from models.ProductModel import ProductModel

class ProductStorage:
    def __init__(self):
        self.conn = sqlite3.connect("products-database.sqlite", check_same_thread=False)
        self.__createDataBase()

    def __createDataBase(self):
        if self.conn is None:
            logging.error(f"[PRODUCT-STORAGE] Erro de conexão!")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
            self.conn.commit()
            logging.debug(f"[PRODUCT-STORAGE] Criando tabela Produtos...")
        except Exception as error: 
            logging.error(f"[PRODUCT-STORAGE] Falha ao criar tabela: {error}")      
            raise error     

    def insert(self, produto: ProductModel) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (name, price, quantity) 
                VALUES (?, ?, ?)
            """, (produto.name, produto.price, produto.quantity))
            id = cursor.lastrowid
            self.conn.commit()
            logging.debug(f"[PRODUCT-STORAGE] Produto inserido com ID {id}")
            return id
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Falha ao inserir produto: {error}")
            raise error
    
    def get(self) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, price, quantity FROM produtos")
            rows = cursor.fetchall()

            produtos = [
            ProductModel(
                id=row[0],
                name=row[1],
                price=row[2],
                quantity=row[3]
            )
            for row in rows
        ]
            logging.debug(f"[PRODUCT-STORAGE] Recuperados {len(rows)} produtos")
            return produtos
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Falha ao recuperar produtos: {error}")
            raise error
    
    def getById(self, id: int) -> ProductModel:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, price, quantity FROM produtos WHERE id = ?", (id,))
            row = cursor.fetchone()
            
            if row is None:
                logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} não encontrado.")
                return None
            
            produto = ProductModel(
                id=row[0],
                name=row[1],
                price=row[2],
                quantity=row[3]
            )
            logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} recuperado.")
            return produto
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Falha ao recuperar produto por ID: {error}")
            raise error
        
    def update(self, id: int, produto: ProductModel) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE produtos 
                SET name = ?, price = ?, quantity = ? 
                WHERE id = ?
            """, (produto.name, produto.price, produto.quantity, id))
            self.conn.commit()
            
            if cursor.rowcount == 0:
                logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} não encontrado para atualização.")
                return False
            
            logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} atualizado com sucesso.")
            return True
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Falha ao atualizar produto: {error}")
            raise error

    def delete(self, id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
            self.conn.commit()

            if cursor.rowcount == 0:
                logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} não encontrado para exclusão.")
                return False

            logging.debug(f"[PRODUCT-STORAGE] Produto de ID {id} excluído com sucesso.")
            return True
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Falha ao excluir produto: {error}")
            raise error