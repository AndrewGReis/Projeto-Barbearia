import pandas as pd
import logging
from pathlib import Path
import os

logging.basicConfig(
    filename='./servicos_barbearia.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger()

DATABASE = "servicos_barbearia.csv"

SERVICOS_PREDEFINIDOS = {
    'maquina': 20,
    'maquina2': 25,
    'barba': 15,
    'tintura': 40,
    'social': 30
}

def inicializar_base_dados() -> pd.DataFrame:
    """Pergunta ao usuário se deseja excluir o CSV existente e criar um novo."""
    if Path(DATABASE).exists():
        resposta = input(f"\n⚠️ O arquivo '{DATABASE}' já existe. Deseja apagar e começar um novo? (s/n): ").strip().lower()
        if resposta == 's':
            try:
                os.remove(DATABASE)
                logger.info("Arquivo CSV existente foi excluído a pedido do usuário.")
                print("🆕 Novo arquivo será criado. Dados antigos foram apagados.")
                return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])
            except Exception as e:
                logger.error(f"Erro ao excluir arquivo existente: {e}")
                print(f"Erro ao excluir o arquivo existente: {e}")
                return carregar_servicos()
        else:
            logger.info("Usuario optou por manter o arquivo CSV existente.")
            print("✅ Arquivo existente será utilizado normalmente.")
            return carregar_servicos()
    else:
        logger.info("Arquivo CSV nao encontrado. Novo sera criado.")
        print("🆕 Nenhum arquivo existente. Novo será criado.")
        return pd.DataFrame(columns=['Servico', 'Preco', 'Quantidade'])

def carregar_servicos() -> pd.DataFrame:
    try:
        if Path(DATABASE).exists():
            logger.info(f"Carregando servicos do arquivo {DATABASE}")
            df = pd.read_csv(DATABASE, encoding='utf-8-sig')
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

def salvar_servicos(df: pd.DataFrame):
    try:
        logger.info("Salvando servicos no arquivo CSV")
        os.makedirs(os.path.dirname(DATABASE) or '.', exist_ok=True)
        df.to_csv(
            DATABASE,
            mode='w',
            index=False,
            columns=['Servico', 'Preco', 'Quantidade'],
            header=['Serviço', 'Preço (R$)', 'Quantidade'],
            encoding='utf-8-sig'
        )
    except Exception as e:
        logger.error(f"Falha ao salvar servicos: {e}")
        raise

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
        print("       RESUMO DE SERVIÇOS ATÉ O MOMENTO       ")
        print("═══════════════════════════════")
        print(f"\n🔹 Total de serviços: {int(total_servicos)}")
        print(f"🔹 Valor arrecadado: R${float(total_arrecadado):.2f}")

        print("\n🔸 Serviços prestados:")
        for _, row in df.iterrows():
            print(f" - {row['Servico']}: {int(row['Quantidade'])}x (R${float(row['Preco']):.2f} cada)")
        print("\n═══════════════════════════════")
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        raise

def mostrar_ajuda():
    help_text = """
GERENCIADOR DE BARBEARIA - COMANDOS:

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
    logger.info("=== Sistema de Barbearia Iniciado ===")
    df = inicializar_base_dados()

    print("\n=== GERENCIADOR DE BARBEARIA ===")
    mostrar_ajuda()

    loop_count = 0
    MAX_LOOPS = 6

    while True:
        try:
            loop_count += 1
            logger.debug(f"Loop {loop_count}/{MAX_LOOPS} - Aguardando comando...")

            if loop_count >= MAX_LOOPS:
                logger.error("Limite maximo de loops atingido! Encerrando por seguranca.")
                print("\n⚠️ Limite de operações excedido. Reinicie o programa.")
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
                    print("Formato incorreto. Uso: add servico")
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
