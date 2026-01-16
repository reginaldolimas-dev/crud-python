#!/bin/env python3

import logging
import os
from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime
import json 

from models.ProductModel import ProductModel
from services.ProductService import ProductService

print("Starting...")

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/products-service.log",
    filemode='a',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.info("=== Aplicação iniciando ===")

app = Flask(__name__)
service = ProductService()

print("Aplicação iniciando...")

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

@app.route("/produtos/<id>", methods = ['GET'])
def buscarPorId(id):
    try:
        produto = service.buscarPorId(id)
        if produto is None:
            return makeResponse(f"Produto com ID {id} não encontrado"), HTTPStatus.NOT_FOUND
        return makeResponse(f"Produto encontrado", { "data": produto.toDict() }), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR    

@app.route("/produtos/<id>", methods = ['PUT'])
def atualizar(id):
    try:
        if not request.is_json:
            return makeResponse(
                "Requisição inválida: corpo JSON necessário"
            ), HTTPStatus.BAD_REQUEST
        
        dados = request.get_json()
        logging.debug(f"[PRODUCT-API] Update request data: {dados}")
        
        produto_atualizado = service.atualizar(int(id), dados)
        
        if produto_atualizado is None:
            return makeResponse(f"Produto com ID {id} não encontrado"), HTTPStatus.NOT_FOUND
        
        return makeResponse(
            f"Produto atualizado com sucesso",
            {"data": produto_atualizado.toDict()}), HTTPStatus.OK
    except ValueError as error:
        errorMsg = f"Dados inválidos para atualizar produto id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.BAD_REQUEST
    except Exception as error: 
        errorMsg = f"Error to try update product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR    

@app.route("/produtos/<id>", methods = ['DELETE'])
def deletar(id):
    try:
        apagou = service.deletar(int(id))
        if not apagou:
            return makeResponse(f"Produto com ID {id} não encontrado"), HTTPStatus.NOT_FOUND
        return makeResponse(f"Produto excluído com sucesso"), HTTPStatus.OK
    except Exception as error:
        errorMsg = f"Error to try delete product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 