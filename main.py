from fastapi import FastAPI
# Instanciando a aplicação com um título amigável para a documentação
app = FastAPI(title="API Inova Lab - Inventário Maker")
# Nosso "Banco de Dados" em memória para esta primeira fase
estoque_laboratorio = [
 {"id": 1, "nome": "Arduino Sensor Shield", "quantidade": 15, "categoria": "Placas de Expansão"},
 {"id": 2, "nome": "Micro Servo Motor SG90", "quantidade": 42, "categoria": "Atuadores"},
 {"id": 3, "nome": "Esteira em Acrílico", "quantidade": 2, "categoria": "Mecânica"},
 {"id": 4, "nome": "Kit Braço Robótico", "quantidade": 5, "categoria": "Kits"}
]
# Rota de boas-vindas (Raiz)
@app.get("/")
def raiz():
    return {"mensagem": "API do Laboratório Maker operante. Acesse /docs para ver a documentação."}
# Nosso primeiro endpoint real
@app.get("/componentes")
def listar_componentes():
    return estoque_laboratorio