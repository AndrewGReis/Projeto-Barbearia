# ✂️ Gerenciador de Serviços de Barbearia

Automação para registro de serviços prestados em barbearia, com cálculo de valores, relatórios diários e armazenamento em CSV.

---

## ⚙️ Funcionalidades

- 📝 **Registro automático de serviços** (com preços pré-definidos e incremento automático da quantidade)
- 🗑️ **Remoção do último serviço adicionado** (remover o serviço mais recente da lista)
- 📊 **Relatórios detalhados:**
  - 📋 Listagem em tabela dos serviços com preço unitário, quantidade e total por serviço
  - 💰 Resumo financeiro diário com total arrecadado e total de serviços prestados
- 📁 **Persistência de dados em arquivo CSV** compatível com Excel, com possibilidade de manter ou recriar a base a cada execução
- 📌 **Logging completo** para rastreamento de operações, erros e eventos importantes
- 🔐 Controle de limite de operações por execução para segurança

---

## 📋 Comandos disponíveis

| Comando   | Descrição                              |
| --------- | ------------------------------------ |
| `add <servico>`  | Adiciona um serviço prestado (exemplo: `add maquina`) |
| `remover` | Remove o último serviço registrado    |
| `list`    | Mostra a lista detalhada dos serviços |
| `resumo`  | Exibe resumo financeiro do dia        |
| `help`    | Exibe esta lista de comandos           |
| `sair`    | Encerra o programa                    |

---

## 💈 Serviços Pré-definidos e Preços

| Serviço  | Preço (R$) |
| -------- | ---------- |
| maquina  | 20,00      |
| maquina2 | 25,00      |
| barba    | 15,00      |
| tintura  | 40,00      |
| social   | 30,00      |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- Bibliotecas:
  - `pandas` para manipulação de dados
  - `logging` para registro de logs
  - `pathlib` e `os` para manipulação de arquivos

---

## ⚙️ Detalhes de Implementação

- Ao iniciar, o sistema verifica se o arquivo `servicos_barbearia.csv` existe. Caso exista, o usuário pode optar por manter ou apagar o arquivo para começar um novo.
- Os dados são armazenados em um DataFrame do pandas com as colunas: Serviço, Preço e Quantidade.
- Adicionar um serviço aumenta a quantidade caso o serviço já tenha sido registrado anteriormente.
- O relatório de listagem mostra o preço unitário, quantidade e total por serviço, além do total geral.
- O resumo diário exibe o total de serviços prestados e o total arrecadado até o momento.
- Logs detalhados são salvos em `servicos_barbearia.log`, incluindo erros, ações do usuário e eventos importantes.
- Para segurança, o programa limita o número de comandos por execução para evitar loops infinitos.

---
