import pandas as pd
import random
from datetime import datetime
import os

# NOVO: Adicionado import para ExcelWriter
from pandas import ExcelWriter

# Configurações de pastas (MODIFICADO: removida variável CSV)
PASTA_PLANILHAS = "planilhas_de_servico"
NOME_ARQUIVO = f"balanco_diario_{datetime.now().strftime('%d%m%Y')}.xlsx"  # MODIFICADO: .xlsx em vez de .csv
CAMINHO_ARQUIVO = os.path.join(PASTA_PLANILHAS, NOME_ARQUIVO)

# Listas de dados (mantidas as mesmas)
NOMES = [
    "João", "Maria", "Pedro", "Ana", "Lucas", "Carla", "Marcos", "Juliana", 
    "Fernando", "Patrícia", "Rafael", "Amanda", "Daniel", "Tatiane", "Gustavo",
    "Bruna", "Rodrigo", "Camila", "Felipe", "Aline", "André", "Vanessa", "Roberto", 
    "Isabela", "Ricardo", "Laura", "Thiago", "Larissa", "Eduardo", "Mariana"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
    "Pereira", "Gomes", "Costa", "Martins", "Ribeiro", "Carvalho", "Lima", "Monteiro",
    "Almeida", "Nascimento", "Mendes", "Barbosa", "Rocha", "Cunha", "Moreira",
    "Cardoso", "Teixeira", "Dias", "Freitas", "Correia", "Moraes", "Castro", "Araújo"
]

SERVICOS_PREDEFINIDOS = {
    'corte_masculino': 35,
    'barba': 25,
    'acabamento_pezinho': 10,
    'pigmentacao': 35,
    'sobrancelhas': 10,
    'barboterapia': 35,
    'depilacao_nariz_orelha': 20,
    'selagem': 80,
    'limpeza_pele': 50,
    'hidratacao': 15,
    'reflexo': 50,
    'platinado': 100,
    'camuflagem_cabelo': 20,
    'camuflagem_barba': 10
}

def gerar_dados_ficticios(num_registros=50):
    """Gera um arquivo Excel com dados fictícios."""
    dados = []
    servicos_disponiveis = list(SERVICOS_PREDEFINIDOS.keys())
    data_atual = datetime.now().strftime("%d/%m/%Y")  # MODIFICADO: Data única para todos
    
    for _ in range(num_registros):
        nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"
        idade = random.randint(10, 60)
        servicos = random.sample(servicos_disponiveis, k=random.randint(1, 3))
        
        for servico in servicos:
            dados.append({
                "Cliente": nome,
                "Idade": idade,
                "Servico": servico,
                "Preco": SERVICOS_PREDEFINIDOS[servico],
                "Quantidade": random.randint(1, 2),
                "Data": data_atual  # MODIFICADO: Usa a data atual fixa
            })
    
    df = pd.DataFrame(dados)
    
    # Garante a ordem das colunas
    colunas = ["Cliente", "Idade", "Servico", "Preco", "Quantidade", "Data"]
    df = df[colunas]
    
    # NOVO: Geração direta de arquivo Excel
    try:
        os.makedirs(PASTA_PLANILHAS, exist_ok=True)
        with ExcelWriter(CAMINHO_ARQUIVO, engine='openpyxl', datetime_format='DD/MM/YYYY') as writer:
            df.to_excel(writer, index=False, sheet_name='Servicos')
        
        print(f"✅ Arquivo Excel gerado com sucesso: {CAMINHO_ARQUIVO}")
        print("\n🔍 Amostra dos dados:")
        print(df.head())
        
    except Exception as e:
        print(f"❌ Erro ao gerar arquivo: {e}")

if __name__ == "__main__":
    gerar_dados_ficticios(num_registros=50)