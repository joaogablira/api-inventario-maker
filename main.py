from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 1. Instanciação da API
app = FastAPI(title="API de Inventário Maker")

# 2. Modelo Pydantic (A + Criação e Validação)
class ComponenteSchema(BaseModel):
    nome: str = Field(..., description="Nome do componente")
    quantidade: int = Field(..., ge=0, description="Quantidade em estoque (deve ser maior ou igual a zero)")
    categoria: str = Field(..., description="Categoria do item (ex: Atuadores, Microcontroladores)")
    estado_conservacao: str = Field(..., description="estado da conversão  ")

# 3. Nosso "Banco de Dados" temporário em memória
estoque_laboratorio = [
    {"id": 1, "nome": "Arduino Sensor Shield", "quantidade": 15, "categoria": "Placas de Expansão"},
    {"id": 2, "nome": "Micro Servo Motor SG90", "quantidade": 14, "categoria": "Atuadores"},
    {"id": 3, "nome": "Solução em Acrílico", "quantidade": 2, "categoria": "Mecânica"}
]

# Rota Raiz
@app.get("/")
def raiz():
    return {
        "mensagem": "API do Laboratório Maker operante. Acesse /docs para ver a documentação."
    }

# CRUD - READ (listar todos)
@app.get("/componentes")
def listar_componentes():
    return estoque_laboratorio

# CRUD - CREATE (Cadastrar novo item)
@app.post("/componentes", status_code=201)
def adicionar_componente(componente: ComponenteSchema):
    if estoque_laboratorio:
        novo_id = max(item["id"] for item in estoque_laboratorio) + 1
    else:
        novo_id = 1

    # Converte o objeto Pydantic para dicionário e insere o ID
    componente_dict = componente.model_dump()
    componente_dict["id"] = novo_id

    estoque_laboratorio.append(componente_dict)

    return {
        "mensagem": "Componente adicionado com sucesso!",
        "componente": componente_dict
    }

# CRUD - UPDATE (Atualizar quantidade ou dados)
@app.put("/componentes/{componente_id}")
def atualizar_componente(componente_id: int, dados_atualizados: ComponenteSchema):
    for item in estoque_laboratorio:
        if item["id"] == componente_id:
            item["nome"] = dados_atualizados.nome
            item["quantidade"] = dados_atualizados.quantidade
            item["categoria"] = dados_atualizados.categoria
            item["estado_conservacao"] = dados_atualizados.estado_conservacao

            return {
                "mensagem": "Componente atualizado com sucesso!",
                "componente": item
            }

    raise HTTPException(
        status_code=404,
        detail="Componente não encontrado no laboratório."
    )

# CRUD - DELETE (Remover item do inventário)
@app.delete("/componentes/{componente_id}")
def remover_componente(componente_id: int):
    for idx, item in enumerate(estoque_laboratorio):
        if item["id"] == componente_id:
            estoque_laboratorio.pop(idx)

            return {
                "mensagem": f"Componente com ID {componente_id} foi removido do estoque."
            }

    raise HTTPException(
        status_code=404,
        detail="Componente não encontrado no laboratório."
    )