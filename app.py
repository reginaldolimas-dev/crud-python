#!/bin/env python3

import logging
import os
from flask import Flask, request, jsonify
from http import HTTPStatus

from services.ProductService import ProductService
from decorators.ErrorHandler import handle_errors, makeResponse

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

@app.route("/produtos", methods = ['POST'])
@handle_errors
def inserir():
    dados = request.get_json()
    logging.debug(f"[PRODUCT-API] Request data: {dados}")
    
    produtoSalvo = service.inserir(dados)

    return jsonify(makeResponse(
        f"Produto inserido com sucesso",
        {"data": produtoSalvo.toDict()})), HTTPStatus.CREATED

@app.route("/produtos", methods = ['GET'])
@handle_errors
def buscar():
        produtos = service.buscar()
        return jsonify(makeResponse(
            "Todos os Produtos",
            { "total": len(produtos), "data": [produto.toDict() for produto in produtos] }
        )), HTTPStatus.OK

@app.route("/produtos/<id>", methods = ['GET'])
@handle_errors
def buscarPorId(id):
    produto = service.buscarPorId(id)
    return jsonify(makeResponse(f"Produto encontrado", { "data": produto.toDict() })), HTTPStatus.OK

@app.route("/produtos/<id>", methods = ['PUT'])
@handle_errors
def atualizar(id):
    dados = request.get_json()
    logging.debug(f"[PRODUCT-API] Update request data: {dados}")
    
    produto_atualizado = service.atualizar(int(id), dados)
    
    return jsonify(makeResponse(
        f"Produto atualizado com sucesso",
        {"data": produto_atualizado.toDict()})), HTTPStatus.OK
    
@app.route("/produtos/<id>", methods = ['DELETE'])
@handle_errors
def deletar(id):
    apagou = service.deletar(int(id))
    if not apagou:
        return makeResponse(f"Produto com ID {id} não encontrado"), HTTPStatus.NOT_FOUND
    return makeResponse(f"Produto excluído com sucesso"), HTTPStatus.OK

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)