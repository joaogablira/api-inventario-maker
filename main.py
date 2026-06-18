from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 1. Instanciação da API
app = FastAPI(title="API Inova Lab - Inventário Maker")

# 2. O Modelo Pydantic (A "Catraca" de Validação)
class ComponenteSchema(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do componente maker")
    quantidade: int = Field(..., ge=0, description="Quantidade em estoque (deve ser maior ou igual a zero)")
    categoria: str = Field(..., description="Categoria do item (ex: Atuadores, Microcontroladores)")

# 3. Nosso "Banco de Dados" temporário em memória
estoque_laboratorio = [
    {"id": 1, "nome": "Arduino Sensor Shield", "quantidade": 15, "categoria": "Placas de Expansão"},
    {"id": 2, "nome": "Micro Servo Motor SG90", "quantidade": 42, "categoria": "Atuadores"},
    {"id": 3, "nome": "Esteira em Acrílico", "quantidade": 2, "categoria": "Mecânica"}
]

# Rota Raiz
@app.get("/")
def raiz():
    return {"mensagem": "API do Laboratório Maker operante. Acesse /docs para ver a documentação."}

# CRUD - READ (Listar todos)
@app.get("/componentes")
def listar_componentes():
    return estoque_laboratorio

# CRUD - CREATE (Cadastrar novo item)
@app.post("/componentes", status_code=201)
def adicionar_componente(novo_componente: ComponenteSchema):
    # Lógica de autoincremento para o ID em memória
    if estoque_laboratorio:
        maior_id = max(item["id"] for item in estoque_laboratorio)
        novo_id = maior_id + 1
    else:
        novo_id = 1

    # Converte o objeto Pydantic para dicionário e insere o ID
    componente_dict = novo_componente.model_dump()
    componente_dict["id"] = novo_id

    estoque_laboratorio.append(componente_dict)
    return {"mensagem": "Componente adicionado com sucesso!", "componente": componente_dict}

# CRUD - UPDATE (Atualizar quantidade ou dados)
@app.put("/componentes/{componente_id}")
def atualizar_componente(componente_id: int, dados_atualizados: ComponenteSchema):
    for item in estoque_laboratorio:
        if item["id"] == componente_id:
            item["nome"] = dados_atualizados.nome
            item["quantidade"] = dados_atualizados.quantidade
            item["categoria"] = dados_atualizados.categoria
            return {"mensagem": "Componente atualizado com sucesso!", "componente": item}

    raise HTTPException(status_code=404, detail="Componente não encontrado no laboratório.")

# CRUD - DELETE (Remover item do inventário)
@app.delete("/componentes/{componente_id}")
def remover_componente(componente_id: int):
    for index, item in enumerate(estoque_laboratorio):
        if item["id"] == componente_id:
            estoque_laboratorio.pop(index)
            return {"mensagem": f"Componente com ID {componente_id} foi removido do estoque."}

    raise HTTPException(status_code=404, detail="Componente não encontrado no laboratório.")