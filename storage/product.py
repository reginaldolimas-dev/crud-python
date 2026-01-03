import logging
import sqlite3
from models.product import ProductModel

class ProductStorage:
    def __init__(self):
        self.conn = sqlite3.connect("products-database.sqlite", check_same_thread=False)
        self.__createDataBase()

    def __createDataBase(self):
        if self.conn is None:
            logging.error(f"[PRODUCT-STORAGE] Connection error!")
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
            logging.debug(f"[PRODUCT-STORAGE] Creating Products table...")
        except Exception as error: 
            logging.error(f"[PRODUCT-STORAGE] Fail to create table: {error}")      
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
            logging.debug(f"[PRODUCT-STORAGE] Product inserted with ID {id}")
            return id
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Fail to insert product: {error}")
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
            logging.debug(f"[PRODUCT-STORAGE] Retrieved {len(rows)} products")
            return produtos
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Fail to get products: {error}")
            raise error
    
    def getById(self, id: int) -> ProductModel:
        ret = {}
        try:
            # TODO Retrieve product by ID from database

            logging.debug(f"[PRODUCT-STORAGE] Retrieved Product ID:{id}")
            return ret
        except Exception as error:
            logging.error(f"[PRODUCT-STORAGE] Fail to get product by ID: {error}")
            raise error
        
    # TODO UPDATE
    # TODO DELETE