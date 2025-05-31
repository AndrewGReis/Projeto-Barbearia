import pandas as pd
import logging
from pathlib import Path
import os
from datetime import datetime
from pandas import ExcelWriter


PASTA_PLANILHAS = "planilhas_de_servico"
PASTA_LOGS = "logs"
DATA_ATUAL = datetime.now().strftime("%d%m%Y")
NOME_ARQUIVO_PADRAO = f"balanco_diario{DATA_ATUAL}.xlsx"
CAMINHO_COMPLETO = os.path.join(PASTA_PLANILHAS, NOME_ARQUIVO_PADRAO)
NOME_ARQUIVO_LOG = f"servicos_barbearia_{DATA_ATUAL}.log"
ARQUIVO_LOG = os.path.join(PASTA_LOGS, NOME_ARQUIVO_LOG)
ARQUIVO_SELECIONADO = None


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


def configurar_logging():
    """Configura o sistema de logging com arquivo diário"""
    os.makedirs(PASTA_LOGS, exist_ok=True)
    filemode = 'a' if Path(ARQUIVO_LOG).exists() else 'w'
    
    logging.basicConfig(
        filename=ARQUIVO_LOG,
        filemode=filemode,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    )
    return logging.getLogger()

logger = configurar_logging()

def selecionar_arquivo() -> str:
    """Gerencia a seleção/criação do arquivo (MODIFICADO para .xlsx)"""
    global ARQUIVO_SELECIONADO
    os.makedirs(PASTA_PLANILHAS, exist_ok=True)
    
    arquivos_existentes = [f for f in os.listdir(PASTA_PLANILHAS) 
                         if f.startswith("balanco_diario") and f.endswith(".xlsx")]
    arquivos_existentes.sort(reverse=True)
    
    if arquivos_existentes:
        print("\nArquivos disponíveis na pasta 'planilhas_de_servico':")
        for i, arquivo in enumerate(arquivos_existentes, 1):
            print(f"{i} - {arquivo}")
        
        resposta = input("\nDeseja usar algum arquivo existente ou criar novo? "
                        "(digite o número do arquivo ou 'novo'): ").strip().lower()
        
        if resposta.isdigit():
            num = int(resposta)
            if 1 <= num <= len(arquivos_existentes):
                ARQUIVO_SELECIONADO = os.path.join(PASTA_PLANILHAS, arquivos_existentes[num-1])
                logger.info(f"Arquivo selecionado: {ARQUIVO_SELECIONADO}")
                return ARQUIVO_SELECIONADO
            else:
                print("❌ Número inválido. Criando novo arquivo.")
    
    ARQUIVO_SELECIONADO = CAMINHO_COMPLETO
    logger.info(f"Novo arquivo criado: {ARQUIVO_SELECIONADO}")
    return ARQUIVO_SELECIONADO

def salvar_servicos(df: pd.DataFrame):
    """Salva em Excel (MODIFICADO completamente)"""
    try:
        global ARQUIVO_SELECIONADO
        logger.info(f"✅ Salvando servicos em: {ARQUIVO_SELECIONADO}")
        
        colunas = ['Cliente', 'Idade', 'Servico', 'Preco', 'Quantidade', 'Data']
        df = df[colunas]
        
        with ExcelWriter(ARQUIVO_SELECIONADO, engine='openpyxl', datetime_format='DD/MM/YYYY') as writer:
            df.to_excel(writer, index=False, sheet_name='Servicos')
        
        print(f"Arquivo Excel atualizado: {os.path.basename(ARQUIVO_SELECIONADO)}")
        
    except Exception as e:
        logger.error(f"Falha ao salvar servicos: {e}")
        raise

def inicializar_base_dados() -> pd.DataFrame:
    """Carrega dados existentes (MODIFICADO para Excel)"""
    database_path = selecionar_arquivo()
    
    if Path(database_path).exists():
        try:
            logger.info(f"Carregando servicos do arquivo {database_path}")
            df = pd.read_excel(database_path, engine='openpyxl')
            
            df.columns = df.columns.str.strip().str.lower()
            
            colunas_necessarias = ['cliente', 'servico', 'preco', 'quantidade']
            if all(col in df.columns for col in colunas_necessarias):
                df = df.rename(columns={
                    'cliente': 'Cliente',
                    'servico': 'Servico',
                    'preco': 'Preco',
                    'quantidade': 'Quantidade'
                })
                
                if 'idade' not in df.columns:
                    df['Idade'] = 0
                if 'data' not in df.columns:
                    df['Data'] = datetime.now().strftime("%d/%m/%Y")
                
                return df[['Cliente', 'Idade', 'Servico', 'Preco', 'Quantidade', 'Data']]
            else:
                raise ValueError("Arquivo com formato inválido")
                
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo: {e}")
            print("\n❌ Erro ao carregar arquivo. Criando novo...")
            return pd.DataFrame(columns=['Cliente', 'Idade', 'Servico', 'Preco', 'Quantidade', 'Data'])
    else:
        logger.info("Arquivo nao encontrado. Novo sera criado.")
        return pd.DataFrame(columns=['Cliente', 'Idade', 'Servico', 'Preco', 'Quantidade', 'Data'])


def adicionar_cliente_servico(cliente: str, idade: int, servico: str, df: pd.DataFrame) -> pd.DataFrame:
    try:
        servico_lower = servico.lower()
        if servico_lower not in SERVICOS_PREDEFINIDOS:
            print(f"Serviço '{servico}' não encontrado. Serviços disponíveis:")
            for serv, preco in SERVICOS_PREDEFINIDOS.items():
                print(f" - {serv}: R${preco:.2f}")
            return df

        preco = SERVICOS_PREDEFINIDOS[servico_lower]
        logger.info(f"Registrando servico: {cliente} (Idade: {idade}) - {servico} - R${preco:.2f}")
        
        mask = (df['Cliente'].str.lower() == cliente.lower()) & (df['Servico'].str.lower() == servico_lower)
        
        if not df[mask].empty:
            idx = df[mask].index[0]
            df.at[idx, 'Quantidade'] += 1
            print(f"+1 serviço para {cliente} ({idade} anos): {servico} (Total: {df.at[idx, 'Quantidade']}x)")
        else:
            novo_servico = pd.DataFrame([[cliente, idade, servico, preco, 1, datetime.now().strftime("%d/%m/%Y")]],
                                      columns=['Cliente', 'Idade', 'Servico', 'Preco', 'Quantidade', 'Data'])
            df = pd.concat([df, novo_servico], ignore_index=True)
            print(f"Serviço registrado para {cliente} ({idade} anos): {servico} (1x)")
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
        idade = df.at[ultimo_idx, 'Idade']
        servico = df.at[ultimo_idx, 'Servico']
        
        df.drop(ultimo_idx, inplace=True)
        print(f"\nServiço '{servico}' do cliente '{cliente}' ({idade} anos) removido com sucesso!")
        logger.info(f"Servico removido: {cliente} (Idade: {idade}) - {servico}")
        
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
            idade = cliente_df.iloc[0]['Idade']
            
            print(f"\nCliente: {cliente} (Idade: {idade} anos)")
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
        print(f"\n📋 Total de serviços: {int(total_servicos)}")
        print(f"💰 Valor arrecadado: R${float(total_arrecadado):.2f}")

        print("\n📊 Distribuição por Idade:")
        print(df['Idade'].value_counts().sort_index())

        clientes_destaque = df.groupby('Cliente').agg({
            'Idade': 'first',
            'Quantidade': 'sum',
            'Preco': lambda x: (x * df.loc[x.index, 'Quantidade']).sum()
        }).rename(columns={'Preco': 'TotalGasto'})
        
        if not clientes_destaque.empty:
            cliente_mais_servicos = clientes_destaque['Quantidade'].idxmax()
            qtd_mais_servicos = clientes_destaque['Quantidade'].max()
            idade_mais_servicos = clientes_destaque.loc[cliente_mais_servicos, 'Idade']
            
            cliente_maior_gasto = clientes_destaque['TotalGasto'].idxmax()
            total_maior_gasto = clientes_destaque['TotalGasto'].max()
            idade_maior_gasto = clientes_destaque.loc[cliente_maior_gasto, 'Idade']
            
            print("\n🏆 DESTAQUES DO DIA:")
            print(f"👑 Cliente com mais serviços: {cliente_mais_servicos} (Idade: {idade_mais_servicos}, {int(qtd_mais_servicos)} serviços)")
            print(f"💰 Cliente com maior gasto: {cliente_maior_gasto} (Idade: {idade_maior_gasto}, R${float(total_maior_gasto):.2f})")

        print("\n═══════════════════════════════")
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        raise

def mostrar_ajuda():
    help_text = """
✂️  GERENCIADOR DE BARBEARIA - COMANDOS: ✂️

add "Nome Completo" idade servico  *Registra um serviço (ex: add "João" 35 corte_masculino)
remover                            *Remove o último serviço adicionado
list                               *Mostra lista detalhada por cliente
resumo                             *Mostra resumo financeiro com destaques
help                               *Mostra esta ajuda
sair                               *Encerra o programa

SERVIÇOS PRÉ-DEFINIDOS:"""
    for servico, preco in SERVICOS_PREDEFINIDOS.items():
        help_text += f"\n - {servico}: R${preco:.2f}"
    print(help_text)


def main():
    logger.info("=== Sistema de Barbearia Iniciado ===")
    df = inicializar_base_dados()

    print("\n=== ✂️  GERENCIADOR DE BARBEARIA ✂️  ===")
    if Path(ARQUIVO_SELECIONADO).exists():
        print(f"📋 Arquivo existente '{os.path.basename(ARQUIVO_SELECIONADO)}' aberto")
    else:
        print(f"🆕 Novo arquivo '{os.path.basename(ARQUIVO_SELECIONADO)}' criado")
    
    mostrar_ajuda()

    loop_count = 0
    MAX_LOOPS = 6

    while True:
        try:
            loop_count += 1
            logger.debug(f"Loop {loop_count}/{MAX_LOOPS} - Aguardando comando...")

            if loop_count >= MAX_LOOPS:
                logger.error("Limite maximo de loops atingido! Encerrando por seguranca.")
                print("\n❌ Limite de operações excedido. Reinicie o programa. 🛡️")
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
                logger.info("Listagem de servicos solicitada")
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
                    idade_servico = parts[2].strip().split()
                    if len(idade_servico) >= 2:
                        try:
                            idade = int(idade_servico[0])
                            servico = idade_servico[1]
                            df = adicionar_cliente_servico(cliente, idade, servico, df)
                            salvar_servicos(df)
                            loop_count = 0
                        except ValueError:
                            print("❌ Idade deve ser um número. Ex: add \"Maria\" 25 barba")
                    else:
                        print("❌ Formato incorreto. Uso: add \"Nome\" idade servico")
                else:
                    print("❌ Formato incorreto. Uso: add \"Nome\" idade servico")
            else:
                logger.warning(f"Comando nao reconhecido: {user_input}")
                print("Comando não reconhecido. Digite 'help' para ajuda.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}\nDigite 'help' para ajuda.")
            logger.error(f"Erro durante execucao: {e}")

if __name__ == "__main__":
    main()