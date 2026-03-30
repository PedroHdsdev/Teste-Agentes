# 🤖 Agente de IA com Personalidades e Análise PostgreSQL

Um sistema Python completo que integra múltiplas personalidades de IA (Ollama/OpenAI) com análise de dados PostgreSQL.

## ✨ Principais Características

- 🎭 **7 Personalidades de IA** - Assistente, Criativa, Educador, Analítica, Amigável, Pragmática e AnalistaDados
- 💾 **Integração PostgreSQL** - Conexão, queries e análise automática de dados
- 🎯 **Interface CLI** - Chat interativo com seleção de personalidade
- 📊 **Coleta Interativa** - Seletar tabelas, campos e períodos de forma guiada
- 🔄 **Suporte Dual** - Ollama (local) ou OpenAI (cloud)

---

## 📁 Estrutura do Projeto

```
test_agent/
├── src/                    # Núcleo da aplicação
│   ├── main.py            # CLI do chat
│   ├── agente_service.py  # Serviço de agentes (Ollama/OpenAI)
│   └── __init__.py
│
├── agents/                 # Sistema de personalidades
│   ├── personality.py     # Definição de personalidades
│   └── __init__.py
│
├── database/               # Integração PostgreSQL
│   ├── client.py          # PostgreSQLClient e AnalisadorDados
│   └── __init__.py
│
├── tools/                  # Ferramentas utilitárias
│   ├── data_collector.py           # Coleta interativa de dados
│   ├── analista_interativo.py      # Workflow: coleta + IA
│   └── __init__.py
│
├── examples/               # Scripts de exemplo
│   ├── exemplo_analista.py
│   └── __init__.py
│
├── docs/                   # Documentação
│   ├── ESTRUTURA.md
│   └── REORGANIZACAO_COMPLETA.md
│
├── config/                 # Configurações
│   ├── .env               # Variáveis de ambiente (NUNCA commitar)
│   └── .env.example       # Template
│
├── venv/                   # Ambiente virtual Python
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorados
└── README.md              # Este arquivo
```

---

## 🚀 Instalação

### 1. Clonar/Preparar o Projeto
```bash
cd test_agent
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
# Copiar template
cp config/.env.example config/.env

# Editar config/.env com seus dados:
# - OLLAMA_HOST e OLLAMA_MODEL (ou OPENAI_API_KEY)
# - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
```

---

## 📖 Como Usar

### 1️⃣ Chat com Personalidades
```bash
# Executar com personalidade
python -m src.main assistente
python -m src.main criativa
python -m src.main analista_dados

# Listar personalidades disponíveis
python -m src.main --listar

# Ver ajuda
python -m src.main --help
```

### 2️⃣ Análise Interativa de Dados
Coleta de dados PostgreSQL + Análise com IA integrada:
```bash
python -m tools.analista_interativo
```

Fluxo:
1. Selecione uma tabela do banco
2. Escolha os campos a analisar
3. Defina um período (opcional)
4. IA analisa e você faz perguntas

### 3️⃣ Exemplos de PostgreSQL
```bash
python -m examples.exemplo_analista
```

---

## 🎭 Personalidades Disponíveis

| Nome | Descrição | Melhor para |
|------|-----------|-----------|
| **Assistente** | Ajudante versátil | Qualquer pergunta |
| **Criativa** | Geração de ideias | Brainstorm, inovação |
| **Educador** | Ensina conceitos | Aprender, tutoriais |
| **Analítica** | Pensamento crítico | Análise profunda |
| **Amigável** | Conversas calorosas | Chat casual |
| **Pragmática** | Soluções diretas | Resolver problemas |
| **AnalistaDados** | Especialista BD | Analise de dados PostgreSQL |

### Criar Personalidade Customizada
Ver [docs/PERSONALIDADES.md](docs/PERSONALIDADES.md)

---

## 🔧 Configuração

### Arquivo .env
```env
# LLM - Escolha um:
# Ollama (local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OU OpenAI (cloud)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# PostgreSQL
DB_HOST=10.0.1.19
DB_PORT=5432
DB_NAME=sua_base
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

### Dependências Principais
- **httpx** - Requisições HTTP
- **psycopg2-binary** - Driver PostgreSQL
- **openai** - API OpenAI
- **python-dotenv** - Gerenciar variáveis de ambiente

Ver `requirements.txt` para lista completa.

---

## 📊 Funcionalidades PostgreSQL

### PostgreSQLClient
- ✅ Conexão com pooling
- ✅ Execução de queries
- ✅ Busca por período (date filtering)
- ✅ Enumeração de tabelas e colunas
- ✅ Estatísticas de tabelas

### AnalisadorDados
- ✅ Geração de relatórios
- ✅ Análise de distribuição
- ✅ Estatísticas sobre colunas
- ✅ Formato estruturado para IA

### ColetorDadosInterativo
- ✅ Seleção interativa de tabelas
- ✅ Seleção de campos
- ✅ Filtro por período
- ✅ Preview dos dados
- ✅ Formatação para análise IA

---

## 🧪 Testando o Projeto

### 1. Testar Conectividade PostgreSQL
```bash
python -m examples.exemplo_analista
```
Deve listar as tabelas do seu banco.

### 2. Testar Chat
```bash
python -m src.main assistente
# Digite: "Olá, quem você é?"
# Saia com: sair
```

### 3. Testar Análise Completa
```bash
python -m tools.analista_interativo
# Siga os passos guiados
```

---

## 🔐 Segurança

⚠️ **IMPORTANTE:**
- ❌ **NUNCA** commitar `config/.env` com credenciais reais
- ✅ Commitar apenas `config/.env.example` como template
- ✅ Adicionar `config/.env` no `.gitignore`

---

## 📚 Documentação Adicional

- [ESTRUTURA.md](docs/ESTRUTURA.md) - Detalhes da arquitetura
- [REORGANIZACAO_COMPLETA.md](docs/REORGANIZACAO_COMPLETA.md) - Histórico de reorganização
- [PERSONALIDADES.md](docs/PERSONALIDADES.md) - Como criar personalidades

---

## 🛠️ Desenvolvimento

### Adicionar Novo Arquivo
1. Escolher pasta apropriada (src/, agents/, database/, tools/, examples/)
2. Criar arquivo com `__init__.py` se necessário
3. Atualizar imports em quem o usar

### Adicionar Nova Personalidade
Ver [docs/PERSONALIDADES.md](docs/PERSONALIDADES.md)

### Adicionar Novo Comando CLI
Editar [src/main.py](src/main.py)

---

## 🤝 Contribuindo

Para melhorias:
1. Teste localmente
2. Verifique imports
3. Mantenha a estrutura de pastas
4. Atualize documentação se necessário

---

## 📝 Licença

Projeto pessoal para uso educacional e profissional.

---

## 📞 Suporte

- Consulte a documentação em `docs/`
- Verifique `.env.example` para configuração
- Rodar exemplos para referência

---

**Última atualização**: 30/03/2026  
**Status**: ✅ Pronto para produção
