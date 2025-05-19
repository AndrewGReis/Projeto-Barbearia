import pandas as pd
import logging
from pathlib import Path
import os
from datetime import datetime

PASTA_PLANILHAS = "planilhas_de_servico"
PASTA_LOGS = "logs"
DATA_ATUAL = datetime.now().strftime("%d%m%Y")
NOME_ARQUIVO_PADRAO = f"balanco_diario{DATA_ATUAL}.csv"
CAMINHO_COMPLETO = os.path.join(PASTA_PLANILHAS, NOME_ARQUIVO_PADRAO)
ARQUIVO_LOG = os.path.join(PASTA_LOGS, "servicos_barbearia.log")

os.makedirs(PASTA_LOGS, exist_ok=True)
logging.basicConfig(
    filename=ARQUIVO_LOG,
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger()

SERVICOS_PREDEFINIDOS = {
    'corte_masculino': 35,
    'barba': 25,
    'acabamento_pezinho': 10,
    'pigmentacao': 20,
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

def selecionar_arquivo() -> str:
    """Gerencia a seleção/criação do arquivo CSV na pasta especificada"""
    os.makedirs(PASTA_PLANILHAS, exist_ok=True)
    
    arquivos_existentes = [f for f in os.listdir(PASTA_PLANILHAS) 
                         if f.startswith("balanco_diario") and f.endswith(".csv")]
    arquivos_existentes.sort(reverse=True)
    
    if arquivos_existentes:
        print("\nArquivos disponíveis na pasta 'planilhas_de_servico':")
        for i, arquivo in enumerate(arquivos_existentes[:5], 1):
            print(f"{i} - {arquivo}")
        
        resposta = input("\nDeseja usar o último arquivo criado "
                        f"({arquivos_existentes[0]}) ou criar um novo? "
                        "(antigo/novo): ").strip().lower()
        
        if resposta == 'antigo':
            return os.path.join(PASTA_PLANILHAS, arquivos_existentes[0])
    
    return CAMINHO_COMPLETO

def inicializar_base_dados() -> pd.DataFrame:
    """Inicializa o DataFrame, verificando arquivo existente ou criando novo"""
    database_path = selecionar_arquivo()
    
    if Path(database_path).exists():
        try:
            logger.info(f"Carregando servicos do arquivo {database_path}")
            df = pd.read_csv(database_path, encoding='utf-8-sig')
            df.columns = df.columns.str.strip().str.lower()
            df = df.rename(columns={
                'serviço': 'Servico',
                'preço (r$)': 'Preco',
                'quantidade': 'Quantidade'
            })
            df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce').fillna(0)
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0)
            print(f"\n✅✅ Arquivo existente carregado: {os.path.basename(database_path)}")
            return df[['Servico', 'Preco', 'Quantidade']]
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo existente: {e}")
            print(f"\n❌❌ Erro ao carregar arquivo existente. \nCriando novo...✅✅")
            return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])
    else:
        logger.info(f"Arquivo {database_path} nao encontrado. Novo sera criado.")
        print(f"\n🆕 Criando novo arquivo: {os.path.basename(database_path)}")
        return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])

def salvar_servicos(df: pd.DataFrame):
    try:
        logger.info(f"✅ Salvando servicos no arquivo {CAMINHO_COMPLETO}")
        df.to_csv(
            CAMINHO_COMPLETO,
            mode='w',
            index=False,
            columns=['Servico', 'Preco', 'Quantidade'],
            header=['Serviço', 'Preço (R$)', 'Quantidade'],
            encoding='utf-8-sig'
        )
    except Exception as e:
        logger.error(f"Falha ao salvar servicos: {e}")
        raise

def carregar_servicos() -> pd.DataFrame:
    try:
        if Path(CAMINHO_COMPLETO).exists():
            logger.info(f"Carregando servicos do arquivo {CAMINHO_COMPLETO}")
            df = pd.read_csv(CAMINHO_COMPLETO, encoding='utf-8-sig')
            df.columns = df.columns.str.strip().str.lower()
            df = df.rename(columns={
                'serviço': 'Servico',
                'preço (r$)': 'Preco',
                'quantidade': 'Quantidade'
            })
            df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce').fillna(0)
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0)
            return df[['Servico', 'Preco', 'Quantidade']]
        else:
            logger.info("Criando novo DataFrame de servicos (nenhum arquivo encontrado).")
            return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])
    except Exception as e:
        logger.error(f"Erro ao carregar servicos: {e}")
        return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])

def adicionar_servico(servico: str, df: pd.DataFrame) -> pd.DataFrame:
    try:
        servico_lower = servico.lower()
        if servico_lower not in SERVICOS_PREDEFINIDOS:
            print(f"Serviço '{servico}' não encontrado. Serviços disponíveis:")
            for serv, preco in SERVICOS_PREDEFINIDOS.items():
                print(f" - {serv}: R${preco:.2f}")
            return df

        preco = SERVICOS_PREDEFINIDOS[servico_lower]
        logger.info(f"Registrando serviço: {servico} - R${preco:.2f}")
        mask = (df['Servico'].str.lower() == servico_lower)
        if not df[mask].empty:
            idx = df[mask].index[0]
            df.at[idx, 'Quantidade'] += 1
            print(f"+1 serviço: {servico} (Total: {df.at[idx, 'Quantidade']}x)")
        else:
            novo_servico = pd.DataFrame([[servico, preco, 1]], columns=['Servico', 'Preco', 'Quantidade'])
            df = pd.concat([df, novo_servico], ignore_index=True)
            print(f"Serviço registrado: {servico} (1x)")
        return df
    except Exception as e:
        logger.error(f"Erro ao registrar servico: {e}")
        raise

def remover_ultimo_servico(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if df.empty:
            print("\nNenhum serviço registrado para remover!")
            return df
        ultimo_idx = df.index[-1]
        servico = df.at[ultimo_idx, 'Servico']
        df.drop(ultimo_idx, inplace=True)
        print(f"\nServiço '{servico}' removido com sucesso!")
        logger.info(f"Servico removido: {servico}")
        return df.reset_index(drop=True)
    except Exception as e:
        logger.error(f"Erro ao remover servico: {e}")
        print(f"\nErro ao remover serviço: {e}")
        return df

def listar_servicos(df: pd.DataFrame):
    try:
        if df.empty:
            print("\nNenhum serviço registrado hoje.")
            return
        df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce')
        df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce')
        df['Total'] = df['Preco'] * df['Quantidade']
        total_geral = df['Total'].sum()

        print("\n{:<15} {:<10} {:<10} {:<10}".format('SERVIÇO', 'PREÇO', 'QTD', 'TOTAL'))
        print("-" * 45)
        for _, row in df.iterrows():
            print("{:<15} R${:<9.2f} {:<10} R${:<9.2f}".format(
                row['Servico'], float(row['Preco']), int(row['Quantidade']),
                float(row['Preco'] * row['Quantidade'])
            ))
        print("-" * 45)
        print("{:<15} {:<10} {:<10} R${:<9.2f}".format("TOTAL GERAL", "", "", float(total_geral)))
    except Exception as e:
        logger.error(f"Erro ao listar servicos: {e}")
        raise

def resumo_diario(df: pd.DataFrame):
    try:
        if df.empty:
            print("\nNenhum serviço registrado.")
            return
        df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce')
        df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce')
        total_servicos = df['Quantidade'].sum()
        total_arrecadado = (df['Preco'] * df['Quantidade']).sum()

        print("\n═══════════════════════════════")
        print("      ✂️  RESUMO DE SERVIÇOS ATÉ O MOMENTO ✂️      ")
        print("═══════════════════════════════")
        print(f"\n📋📋 Total de serviços: {int(total_servicos)}")
        print(f"🧾🧾 Valor arrecadado: R${float(total_arrecadado):.2f}")

        print("\n📋📋 Serviços prestados:")
        for _, row in df.iterrows():
            print(f" - {row['Servico']}: {int(row['Quantidade'])}x (R${float(row['Preco']):.2f} cada)")
        print("\n═══════════════════════════════")
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        raise

def mostrar_ajuda():
    help_text = """
✂️  GERENCIADOR DE BARBEARIA - COMANDOS:✂️

add servico      Registra um serviço prestado
remover          Remove o último serviço adicionado
list             Mostra lista detalhada
resumo           Mostra resumo financeiro
help             Mostra esta ajuda
sair             Encerra o programa

SERVIÇOS PRÉ-DEFINIDOS:"""
    for servico, preco in SERVICOS_PREDEFINIDOS.items():
        help_text += f"\n - {servico}: R${preco:.2f}"
    print(help_text)

def main():
    logger.info("===  Sistema de Barbearia Iniciado   ===")
    df = inicializar_base_dados()

    print("\n=== ✂️  GERENCIADOR DE BARBEARIA ✂️  ===")
    mostrar_ajuda()

    loop_count = 0
    MAX_LOOPS = 6

    while True:
        try:
            loop_count += 1
            logger.debug(f"Loop {loop_count}/{MAX_LOOPS} - Aguardando comando...")

            if loop_count >= MAX_LOOPS:
                logger.error("Limite maximo de loops atingido! Encerrando por seguranca.")
                print("\n❌❌ Limite de operações excedido. \nReinicie o programa.🛡️ 🛡️")
                salvar_servicos(df)
                break

            user_input = input("\nDigite um comando (ou 'sair' para encerrar): ").strip().lower()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]

            if command == 'sair':
                logger.info("=== Servico encerrado pelo usuario ===")
                print("Encerrando o programa...")
                salvar_servicos(df)
                break
            elif command == 'help':
                logger.info("Mostrando lista de comandos")
                mostrar_ajuda()
                loop_count = 0
            elif command == 'add':
                if len(parts) < 2:
                    logger.warning("Formato incorreto no comando 'add'")
                    print("❌ Formato incorreto. Uso: add servico ✅")
                    continue
                servico = parts[1]
                df = adicionar_servico(servico, df)
                salvar_servicos(df)
                loop_count = 0
            elif command == 'remover':
                logger.info("Remocao de servico solicitada")
                df = remover_ultimo_servico(df)
                salvar_servicos(df)
                loop_count = 0
            elif command == 'list':
                logger.info("Listagem de serviços solicitada")
                listar_servicos(df)
                loop_count = 0
            elif command == 'resumo':
                logger.info("Resumo diario solicitado")
                resumo_diario(df)
                loop_count = 0
            else:
                logger.warning(f"Comando nao reconhecido: {command}")
                print("Comando não reconhecido. Digite 'help' para ajuda.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}\nDigite 'help' para ajuda.")
            logger.error(f"Erro durante execucao: {e}")

if __name__ == "__main__":
    main()