#!/bin/env python3

import logging
from functools import wraps
from flask import jsonify
from http import HTTPStatus
from datetime import datetime

def makeResponse(msg: str, args: dict = {}):
    """Helper para criar resposta padronizada"""
    ret = {
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }
    for key in args:
        ret[key] = args[key]
    return ret

def handle_errors(f):
    """
    Decorator para capturar automaticamente exceções nos endpoints.
    
    Trata diferentes tipos de exceção e retorna respostas apropriadas:
    - ValueError: BAD_REQUEST (400)
    - KeyError: BAD_REQUEST (400) 
    - Exception genérica: INTERNAL_SERVER_ERROR (500)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as error:
            error_msg = f"Dados inválidos: {error}"
            logging.error(f"[PRODUCT-API] {error_msg}")
            return makeResponse(error_msg), HTTPStatus.BAD_REQUEST
        except KeyError as error:
            error_msg = f"Campo obrigatório ausente: {error}"
            logging.error(f"[PRODUCT-API] {error_msg}")
            return makeResponse(error_msg), HTTPStatus.BAD_REQUEST
        except Exception as error:
            error_msg = f"Erro ao processar requisição: {error}"
            logging.error(f"[PRODUCT-API] {error_msg}")
            return makeResponse(error_msg), HTTPStatus.INTERNAL_SERVER_ERROR
    
    return decorated_function
