# ✂️ Gerenciador de Serviços de Barbearia ✂️

Sistema em desenvolvimento para gestão de serviços em barbearia com controle individual por cliente, relatórios financeiros detalhados e armazenamento seguro de dados.

![Progresso](https://geps.dev/progress/80?style=for-the-badge&color=2ecc71)


 📂 Estrutura do Projeto

```bash
📁 Projeto-Barbearia/
├── 📄 barbearia.py          # Código principal
├── 📁 planilhas_de_servico/ # Armazena os CSVs diários
├── 📁 logs/                 # Registros de operações
└── 📄 README.md             # Documentação do projeto

 ⚙️ Funcionalidades 💻

- 👤  Cadastro por cliente com nome e sobrenome
- 🏆  Destaques automáticos para o dia
- 📈  Relatórios financeiros aprimorados

 📋 Funcionalidades Principais

  📝  Registro de serviços com preços pré-definidos 
  🔄  Incremento automático de quantidade para serviços repetidos 
  🗑️  Opção de Remoção de último serviço adicionado 
  📊  Relatórios detalhados em formato de tabela 
  💾  Armazenamento em CSV com compatibilidade Excel 
  📌  Sistema completo de logs de operações 

 🛠️ Tecnologias Utilizadas

-  Python
- Bibliotecas:
  - `pandas` para manipulação de dados
  - `logging` para registro de logs
  - `pathlib` e `os` para manipulação de arquivos

 💾 Estrutura de armazenamento:

- Formato: CSV com UTF-8-sig (Excel compatível)
- Nomenclatura: balanco_diario[DDMMAAAA].csv
- Local: /planilhas_de_servico/
- Logs: /logs/servicos_barbearia.log
- Nomenclatura: servicos_barbearia[DDMMAAAA].log


 🚀 Como Usar

add "Nome Completo" serviço  # Registra um serviço
remover                      # Remove o último serviço
list                         # Lista todos serviços
resumo                       # Mostra relatório completo
help                         # Exibe ajuda
sair                         # Encerra o programa


 📋  Serviços Pré-definidos e Preços  🧾

| Serviço                   | Preço (R$) |
| ------------------------- | ---------- |
| corte_masculino           | 35,00      |
| barba                     | 25,00      |
| acabamento_pezinho        | 10,00      |
| pigmentacao               | 35,00      |
| sobrancelhas              | 10,00      |
| barboterapia              | 35,00      |
| depilacao_nariz_orelha    | 20,00      |
| selagem                   | 80,00      |
| limpeza_pele              | 50,00      |
| hidratacao                | 15,00      |
| reflexo                   | 50,00      |
| platinado                 | 100,00     |
| camuflagem_cabelo         | 20,00      |
| camuflagem_barba          | 10,00      |
---


 🏆 Destaques Automáticos
═══════════════════════════════
      ✂️ RESUMO DIÁRIO ✂️      
═══════════════════════════════
  Exemplo da Funcionalidade 
  📋📋 Total de serviços: 9  
  🧾🧾 Valor arrecadado: R$525.00

 🏆 DESTAQUES:  
 👑 Cliente Top: André Silva (8 serviços)  
 💰 Maior Gasto: Anderson Silva (R$250.00) 

 🔍 Detalhamento por Cliente:
 Exemplo:

 📋📋 Serviços por cliente:

Cliente: Carlos Oliveira  
- selagem: 1x (R$80.00)  
- barboterapia: 1x (R$35.00)
- Total: R$115.00  

Cliente: Anderson Silva  
- reflexo: 1x (R$50.00)  
- depilacao_nariz_orelha: 1x (R$20.00)  
- platinado: 1x (R$100.00)  
- selagem: 1x (R$80.00)  
- Total: R$250.00  

═══════════════════════════════

═══════════════════════════════

 ⚙️ Detalhes de Implementação

 📂 Sistema de Arquivos
- Verificação automática: arquivo `balanco_diario[DATA].csv` ao iniciar
- Opção de continuar com arquivo existente ou criar novo
- Logs diários em `servicos_barbearia.log` com timestamp

 🛠️  Funcionalidades Implementadas
  - Cadastro por Cliente Completo:
  - Registro com nomes entre aspas (ex: `"João Silva"`)
  - Histórico individual de serviços por cliente
  - Compatibilidade com versões anteriores (clientes sem nome ficam como "Geral")

   Estrutura DataFrame:
  Colunas: [Cliente, Serviço, Preço, Quantidade, Total]

 👥 Agrupamento Inteligente
- Agrupa serviços por cliente automaticamente
- Calcula totais individuais e comparativos
- Ordena por volume de serviços ou valor gasto

 🔒 Segurança e Controle
 Funcionalidade  Descrição 

  ⏳ Limite de Operações  6 comandos por execução 
  💾 Backup Automático  Salva dados antes de operações críticas 
  🛡️ Tratamento de Erros  Valida nomes e serviços em tempo real 

 💾 Persistência de Dados

  Estrutura de armazenamento:
  
- Formato: CSV com UTF-8-sig (Excel compatível)
- Nomenclatura: balanco_diario[DDMMAAAA].csv
- Local: /planilhas_de_servico/
- Logs: /logs/servicos_barbearia.log

💻 Modificações Recomendadas para Adição de Banco de Dados Local com Integração na Nuvem

![Progresso](https://geps.dev/progress/20?style=for-the-badge&color=2ecc71)

📊 Sistema atualmente compatível Adição de banco de dados

O código atual já tem uma estrutura perfeita para migrar para um banco de dados na nuvem!
Ele usa pandas (ótimo para manipulação de dados antes de enviar para a nuvem).
Já tem lógica de CRUD (adicionar, remover, listar serviços).
Gera logs e CSVs (que podem ser substituídos por queries SQL ou chamadas à API).

## 🌟 Visão Geral
Sistema completo para gerenciamento de barbearias com:
- Armazenamento local (CSV)
- Integração em nuvem (Google Sheets)
- Dashboard profissional (Looker Studio)

🛠️ Configuração Necessária
Requisitos de Bibliotecas
gspread
google-auth
