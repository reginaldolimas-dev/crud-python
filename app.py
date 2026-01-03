#!/bin/env python3

import logging
from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime
import json 

from models.product import ProductModel
from services.ProductService import ProductService

print("Starting...")

app = Flask(__name__)
service = ProductService()
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="./logs/products-service.log",
    filemode='a',
    datefmt='%H:%M:%S',
)
print("Exiting...")

def makeResponse(msg: str, args: dict = {}):
    ret = {
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }

    for key in args:
        ret[key] = args[key]

    return ret

@app.route("/produtos", methods = ['POST'])
def inserir():
    try:
        if not request.is_json:
            return makeResponse(
                "Requisição inválida: corpo JSON necessário"
            ), HTTPStatus.BAD_REQUEST
        
        dados = request.get_json()
        logging.debug(f"[PRODUCT-API] Request data: {dados}")
        
        produto = ProductModel.fromDict(dados)
        produtoSalvo = service.inserir(produto)

        return makeResponse(
            f"Produto inserido com sucesso",
            {"data": produtoSalvo.toDict()}), HTTPStatus.CREATED
    except Exception as error: 
        errorMsg = f"Error to try process request: Invalid request {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.BAD_REQUEST

@app.route("/produtos", methods = ['GET'])
def buscar():
    try:
        produtos = service.buscar()
        return makeResponse(
            "Todos os Produtos",
            { "total": len(produtos), "data": [produto.toDict() for produto in produtos] }
        ), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get all products: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR    

@app.route("/products/<id>", methods = ['GET'])
def getById(id):
    ret = {}
    try:
        return makeResponse(f"Product id {id}", { "data": ret.toDict() }), HTTPStatus.NOT_IMPLEMENTED
    except Exception as error: 
        errorMsg = f"Error to try get product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# TODO UPDATE
# TODO DELETE   

