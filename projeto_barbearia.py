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

ARQUIVO_SELECIONADO = None

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


def selecionar_arquivo() -> str:
    """Gerencia a seleção/criação do arquivo CSV na pasta especificada"""
    global ARQUIVO_SELECIONADO
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
            ARQUIVO_SELECIONADO = os.path.join(PASTA_PLANILHAS, arquivos_existentes[0])
            return ARQUIVO_SELECIONADO
    
    ARQUIVO_SELECIONADO = CAMINHO_COMPLETO
    return ARQUIVO_SELECIONADO


def salvar_servicos(df: pd.DataFrame):
    try:
        global ARQUIVO_SELECIONADO
        logger.info(f"✅ Salvando servicos no arquivo {ARQUIVO_SELECIONADO}")
        df.to_csv(
            ARQUIVO_SELECIONADO,
            mode='w',
            index=False,
            columns=['Cliente', 'Servico', 'Preco', 'Quantidade'],
            header=['Cliente', 'Serviço', 'Preço (R$)', 'Quantidade'],
            encoding='utf-8-sig'
        )
    except Exception as e:
        logger.error(f"Falha ao salvar servicos: {e}")
        raise


def inicializar_base_dados() -> pd.DataFrame:
    """Inicializa o DataFrame, verificando arquivo existente ou criando novo"""
    database_path = selecionar_arquivo()
    
    if Path(database_path).exists():
        try:
            logger.info(f"Carregando servicos do arquivo {database_path}")
            df = pd.read_csv(database_path, encoding='utf-8-sig')
            df.columns = df.columns.str.strip().str.lower()
            
            if 'cliente' in df.columns:
                df = df.rename(columns={
                    'cliente': 'Cliente',
                    'serviço': 'Servico',
                    'preço (r$)': 'Preco',
                    'quantidade': 'Quantidade'
                })
                return df[['Cliente', 'Servico', 'Preco', 'Quantidade']]
            else:
                df = df.rename(columns={
                    'serviço': 'Servico',
                    'preço (r$)': 'Preco',
                    'quantidade': 'Quantidade'
                })
                df['Cliente'] = 'Geral'
                return df[['Cliente', 'Servico', 'Preco', 'Quantidade']]
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo existente: {e}")
            print(f"\n❌❌ Erro ao carregar arquivo existente. \nCriando novo...✅✅")
            return pd.DataFrame(columns=['Cliente', 'Servico', 'Preco', 'Quantidade'])
    else:
        logger.info(f"Arquivo {database_path} nao encontrado. Novo sera criado.")
        print(f"\n🆕 Criando novo arquivo: {os.path.basename(database_path)}")
        return pd.DataFrame(columns=['Cliente', 'Servico', 'Preco', 'Quantidade'])

def adicionar_cliente_servico(cliente: str, servico: str, df: pd.DataFrame) -> pd.DataFrame:
    try:
        servico_lower = servico.lower()
        if servico_lower not in SERVICOS_PREDEFINIDOS:
            print(f"Serviço '{servico}' não encontrado. Serviços disponíveis:")
            for serv, preco in SERVICOS_PREDEFINIDOS.items():
                print(f" - {serv}: R${preco:.2f}")
            return df

        preco = SERVICOS_PREDEFINIDOS[servico_lower]
        logger.info(f"Registrando serviço: {cliente} - {servico} - R${preco:.2f}")
        
        mask = (df['Cliente'].str.lower() == cliente.lower()) & (df['Servico'].str.lower() == servico_lower)
        
        if not df[mask].empty:
            idx = df[mask].index[0]
            df.at[idx, 'Quantidade'] += 1
            print(f"+1 serviço para {cliente}: {servico} (Total: {df.at[idx, 'Quantidade']}x)")
        else:
            novo_servico = pd.DataFrame([[cliente, servico, preco, 1]], 
                                      columns=['Cliente', 'Servico', 'Preco', 'Quantidade'])
            df = pd.concat([df, novo_servico], ignore_index=True)
            print(f"Serviço registrado para {cliente}: {servico} (1x)")
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
        cliente = df.at[ultimo_idx, 'Cliente']
        servico = df.at[ultimo_idx, 'Servico']
        df.drop(ultimo_idx, inplace=True)
        print(f"\nServiço '{servico}' do cliente '{cliente}' removido com sucesso!")
        logger.info(f"Servico removido: {cliente} - {servico}")
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
        
        clientes = df['Cliente'].unique()
        
        for cliente in clientes:
            cliente_df = df[df['Cliente'] == cliente]
            total_cliente = cliente_df['Total'].sum()
            
            print(f"\nCliente: {cliente}")
            print("{:<25} {:<10} {:<10} {:<10}".format('SERVIÇO', 'PREÇO', 'QTD', 'TOTAL'))
            print("-" * 55)
            for _, row in cliente_df.iterrows():
                print("{:<25} R${:<9.2f} {:<10} R${:<9.2f}".format(
                    row['Servico'], float(row['Preco']), int(row['Quantidade']),
                    float(row['Preco'] * row['Quantidade'])
                ))
            print("-" * 55)
            print("{:<25} {:<10} {:<10} R${:<9.2f}".format("TOTAL", "", "", float(total_cliente)))
        
        total_geral = df['Total'].sum()
        print("\n" + "=" * 55)
        print("{:<25} {:<10} {:<10} R${:<9.2f}".format("TOTAL GERAL", "", "", float(total_geral)))
        print("=" * 55)
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
        print(f"\n🧾🧾 Valor arrecadado: R${float(total_arrecadado):.2f}")

        clientes_destaque = df.groupby('Cliente').agg({
            'Quantidade': 'sum',
            'Preco': lambda x: (x * df.loc[x.index, 'Quantidade']).sum()
        }).rename(columns={'Preco': 'TotalGasto'})
        
        if not clientes_destaque.empty:
            cliente_mais_servicos = clientes_destaque['Quantidade'].idxmax()
            qtd_mais_servicos = clientes_destaque['Quantidade'].max()
            
            cliente_maior_gasto = clientes_destaque['TotalGasto'].idxmax()
            total_maior_gasto = clientes_destaque['TotalGasto'].max()
            
            print("\n🏆 DESTAQUES DO DIA:")
            print(f"👑 Cliente com mais serviços: {cliente_mais_servicos} ({int(qtd_mais_servicos)} serviços)")
            print(f"💰 Cliente com maior gasto: {cliente_maior_gasto} (R${float(total_maior_gasto):.2f})")

        clientes = df['Cliente'].unique()
        print("\n📋📋 Serviços por cliente:")
        for cliente in clientes:
            cliente_df = df[df['Cliente'] == cliente]
            total_cliente = (cliente_df['Preco'] * cliente_df['Quantidade']).sum()
            print(f"\nCliente: {cliente}")
            for _, row in cliente_df.iterrows():
                print(f" - {row['Servico']}: {int(row['Quantidade'])}x (R${float(row['Preco']):.2f} cada)")
            print(f"Total do cliente: R${float(total_cliente):.2f}")
        
        print("\n═══════════════════════════════")
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        raise

def mostrar_ajuda():
    help_text = """
✂️  GERENCIADOR DE BARBEARIA - COMANDOS: ✂️

add "Nome Completo" servico  Registra um serviço para um cliente
remover                     Remove o último serviço adicionado
list                        Mostra lista detalhada por cliente
resumo                      Mostra resumo financeiro com destaques
help                        Mostra esta ajuda
sair                        Encerra o programa

Exemplos:
add "Andrew Reis" corte_masculino
add "Gustavo Lima" barba

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

            user_input = input("\nDigite um comando (ou 'sair' para encerrar): ").strip()
            if not user_input:
                continue

            if user_input.lower() == 'sair':
                logger.info("=== Servico encerrado pelo usuario ===")
                print("Encerrando o programa...")
                salvar_servicos(df)
                break
            elif user_input.lower() == 'help':
                logger.info("Mostrando lista de comandos")
                mostrar_ajuda()
                loop_count = 0
            elif user_input.lower() == 'remover':
                logger.info("Remocao de servico solicitada")
                df = remover_ultimo_servico(df)
                salvar_servicos(df)
                loop_count = 0
            elif user_input.lower() == 'list':
                logger.info("Listagem de serviços solicitada")
                listar_servicos(df)
                loop_count = 0
            elif user_input.lower() == 'resumo':
                logger.info("Resumo diario solicitado")
                resumo_diario(df)
                loop_count = 0
            elif user_input.lower().startswith('add '):
                parts = user_input[len('add '):].strip().split('"')
                if len(parts) >= 3:
                    cliente = parts[1].strip()
                    servico = parts[2].strip()
                    if cliente and servico:
                        df = adicionar_cliente_servico(cliente, servico, df)
                        salvar_servicos(df)
                        loop_count = 0
                    else:
                        print("❌ Formato incorreto. Uso: add \"Nome Completo\" servico ✅")
                else:
                    print("❌ Formato incorreto. Uso: add \"Nome Completo\" servico ✅")
            else:
                logger.warning(f"Comando nao reconhecido: {user_input}")
                print("Comando não reconhecido. Digite 'help' para ajuda.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}\nDigite 'help' para ajuda.")
            logger.error(f"Erro durante execucao: {e}")

if __name__ == "__main__":
    main()