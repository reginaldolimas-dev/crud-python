# CRUD de Produtos - Python + Flask

API REST para gerenciamento de produtos utilizando Flask e SQLite.

## 📋 Estrutura do Projeto

```
crud-python/
├── app.py                 # Aplicação principal e endpoints
├── requirements.txt       # Dependências do projeto
├── logs/                  # Diretório de logs
├── models/
│   └── ProductModel.py    # Modelo de dados do produto
├── services/
│   └── ProductService.py  # Lógica de negócio
└── storage/
    └── ProductStorage.py  # Acesso ao banco de dados
```

## 🚀 Como Iniciar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 📡 Endpoints da API

### 1. Criar Produto

**POST** `/produtos`

```bash
curl -X POST http://localhost:5000/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Notebook",
    "price": 2500.00,
    "quantity": 10
  }'
```

**Resposta:**
```json
{
  "message": "Produto inserido com sucesso",
  "timestamp": "2026-01-16T10:30:00.000000",
  "data": {
    "id": 1,
    "name": "Notebook",
    "price": 2500.00,
    "quantity": 10
  }
}
```

### 2. Listar Todos os Produtos

**GET** `/produtos`

```bash
curl http://localhost:5000/produtos
```

**Resposta:**
```json
{
  "message": "Todos os Produtos",
  "timestamp": "2026-01-16T10:30:00.000000",
  "total": 2,
  "data": [
    {
      "id": 1,
      "name": "Notebook",
      "price": 2500.00,
      "quantity": 10
    },
    {
      "id": 2,
      "name": "Mouse",
      "price": 50.00,
      "quantity": 25
    }
  ]
}
```

### 3. Buscar Produto por ID

**GET** `/produtos/<id>`

```bash
curl http://localhost:5000/produtos/1
```

**Resposta:**
```json
{
  "message": "Produto encontrado",
  "timestamp": "2026-01-16T10:30:00.000000",
  "data": {
    "id": 1,
    "name": "Notebook",
    "price": 2500.00,
    "quantity": 10
  }
}
```

### 4. Atualizar Produto (Parcial)

**PUT** `/produtos/<id>`

Permite atualizar campos específicos sem enviar todos os dados:

```bash
# Atualizar apenas o preço
curl -X PUT http://localhost:5000/produtos/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 2300.00}'

# Atualizar múltiplos campos
curl -X PUT http://localhost:5000/produtos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Notebook Gamer",
    "price": 3500.00,
    "quantity": 5
  }'
```

**Resposta:**
```json
{
  "message": "Produto atualizado com sucesso",
  "timestamp": "2026-01-16T10:30:00.000000",
  "data": {
    "id": 1,
    "name": "Notebook Gamer",
    "price": 3500.00,
    "quantity": 5
  }
}
```

### 5. Deletar Produto

**DELETE** `/produtos/<id>`

```bash
curl -X DELETE http://localhost:5000/produtos/1
```

**Resposta:**
```json
{
  "message": "Produto excluído com sucesso",
  "timestamp": "2026-01-16T10:30:00.000000"
}
```

## 📊 Banco de Dados

O projeto utiliza **SQLite** com o arquivo `products-database.sqlite` criado automaticamente na primeira execução.

### Estrutura da Tabela `produtos`

| Campo    | Tipo    | Descrição                    |
|----------|---------|------------------------------|
| id       | INTEGER | Chave primária (auto)        |
| name     | TEXT    | Nome do produto (obrigatório)|
| price    | REAL    | Preço (> 0)                  |
| quantity | INTEGER | Quantidade (≥ 0)             |

## 📝 Logs

Os logs da aplicação são salvos em `logs/products-service.log` com informações de:
- Requisições recebidas
- Operações realizadas (insert, update, delete)
- Erros e exceções

## ⚙️ Validações

O sistema realiza as seguintes validações:

- **Nome**: obrigatório e não pode ser vazio
- **Preço**: deve ser maior que zero
- **Quantidade**: não pode ser negativa

## 🛠️ Tecnologias

- **Python 3.12**
- **Flask 3.0.0** - Framework web
- **SQLite** - Banco de dados
- **Arquitetura em camadas**: Models, Services, Storage

## 📦 Dependências

```
flask==3.0.0
```

## 🔍 Códigos de Status HTTP

| Código | Descrição                          |
|--------|------------------------------------|
| 200    | OK - Requisição bem-sucedida       |
| 201    | Created - Produto criado           |
| 400    | Bad Request - Dados inválidos      |
| 404    | Not Found - Produto não encontrado |
| 500    | Internal Server Error - Erro       |

## 📄 Licença

Projeto desenvolvido para fins educacionais.
