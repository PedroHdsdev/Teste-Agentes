# Estrutura do Projeto

Uma documentação completa da organização de arquivos do projeto.

## 🗂️ Estrutura de Pastas

```
test_agent/
│
├── 📂 src/                          # Código principal do agente
│   ├── __init__.py
│   ├── main.py                      # Ponto de entrada (chat interativo)
│   └── agente_service.py            # Serviço de agentes (Ollama, OpenAI)
│
├── 📂 agents/                       # Personalidades do agente
│   ├── __init__.py
│   └── personality.py               # Classes de personalidades
│
├── 📂 database/                     # Integração com PostgreSQL
│   ├── __init__.py
│   └── client.py                    # PostgreSQLClient e AnalisadorDados
│
├── 📂 tools/                        # Ferramentas e utilitários
│   ├── __init__.py
│   ├── data_collector.py            # Coleta interativa de dados
│   └── analista_interativo.py       # Interface interativa do analista
│
├── 📂 examples/                     # Exemplos e scripts de teste
│   ├── __init__.py
│   └── exemplo_analista.py          # Exemplos de uso das classes
│
├── 📂 docs/                         # Documentação
│   ├── README.md                    # Guia rápido
│   ├── DATABASE.md                  # Integração com PostgreSQL
│   ├── PERSONALIDADES.md            # Criar personalidades customizadas
│   └── ESTRUTURA.md                 # Este arquivo
│
├── 📂 config/                       # Arquivos de configuração
│   ├── .env                         # Variáveis de ambiente (local)
│   └── .env.example                 # Template de configuração
│
├── README.md                        # Índice principal
└── venv/                            # Ambiente virtual Python
```

## 📝 Descrição das Pastas

### `src/` - Código Principal
- **main.py**: Ponto de entrada do projeto. Execute com `python src/main.py`
- **agente_service.py**: Serviço que cria agentes (Ollama ou OpenAI)

**Como usar:**
```bash
python src/main.py                  # Chat com personalidade padrão
python src/main.py criativa         # Chat com personalidade criativa
python src/main.py analista_dados   # Chat com analista de dados
```

### `agents/` - Personalidades
- **personality.py**: Define o comportamento dos agentes
  - PersonalidadeAssistente
  - PersonalidadeCriativa
  - PersonalidadeEducador
  - PersonalidadeAnalitica
  - PersonalidadeAmigavel
  - PersonalidadePragmatica
  - PersonalidadeAnalistaDados
  - GerenciadorPersonalidades (gerencia todas as personalidades)

**Como usar:**
```python
from agents.personality import GerenciadorPersonalidades, PersonalidadeBase

# Usar uma personalidade existente
pers = GerenciadorPersonalidades.obter_personalidade("criativa")

# Criar e registrar uma personalidade custom
class MinhaPersonalidade(PersonalidadeBase):
    @property
    def nome(self) -> str:
        return "Minha"
    
    @property
    def descricao(self) -> str:
        return "Minha personalidade custom"
    
    @property
    def system_prompt(self) -> str:
        return "..."

GerenciadorPersonalidades.registrar_personalidade("minha", MinhaPersonalidade())
```

### `database/` - PostgreSQL
- **client.py**: Gerencia conexões e análises do banco de dados
  - PostgreSQLClient: Conexão, queries, busca por período
  - AnalisadorDados: Análise resumida, relatórios

**Recursos:**
- Conectar/desconectar do banco
- Executar queries personalizadas
- Buscar dados por período de data
- Listar tabelas e colunas
- Análise de colunas individuais
- Gerar relatórios

**Como usar:**
```python
from database.client import PostgreSQLClient, AnalisadorDados

db = PostgreSQLClient()
db.conectar()

# Listar tabelas
tabelas = db.obter_tabelas()

# Buscar dados de um período
dados = db.buscar_por_periodo(
    tabela="vendas",
    coluna_data="data_venda",
    data_inicio="2024-01-01",
    data_fim="2024-12-31"
)

# Análise
analisador = AnalisadorDados(db)
relatorio = analisador.gerar_relatorio_periodo(...)

db.desconectar()
```

### `tools/` - Ferramentas
- **data_collector.py**: Coleta interativa de dados
  - ColetorDadosInterativo: Interface amigável para selecionar tabela, campos, período
  
- **analista_interativo.py**: Interface do analista de dados com IA
  - Fluxo: 1) Usuário coleta dados → 2) IA analisa os dados

**Como usar:**
```bash
python tools/analista_interativo.py
```

Fluxo:
1. Selecione uma tabela
2. Escolha os campos que quer
3. Defina o período
4. Dados são coletados
5. IA gera análise resumida dos dados

### `examples/` - Exemplos
- **exemplo_analista.py**: Exemplos de código mostrando como usar as classes

**Como executar:**
```bash
python examples/exemplo_analista.py
```

### `docs/` - Documentação
- **README.md**: Guia rápido de início
- **DATABASE.md**: Documentação completa de PostgreSQL
- **PERSONALIDADES.md**: Como criar personalidades customizadas
- **ESTRUTURA.md**: Este arquivo

### `config/` - Configuração
- **.env**: Suas credenciais (não versionar)
- **.env.example**: Template padrão

## 🚀 Como Iniciar

### 1. Clone/Configure
```bash
cd test_agent
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 2. Configure .env
```bash
cp config/.env.example config/.env
# Edite config/.env com suas credenciais
```

### 3. Teste Conexão
```bash
python examples/exemplo_analista.py
```

### 4. Use o Chat
```bash
# Chat padrão
python src/main.py

# Com personalidade específica
python src/main.py analista_dados
```

### 5. Análise Interativa
```bash
python tools/analista_interativo.py
```

## 📚 Fluxos de Uso

### Fluxo 1: Chat Direto com IA
```
python src/main.py
→ Escolha personalidade
→ Digite perguntas
→ IA responde
```

### Fluxo 2: Análise de Dados com IA
```
python tools/analista_interativo.py
→ Selecione tabela
→ Escolha campos
→ Defina período
→ Dados são coletados
→ IA analisa e gera relatório
```

### Fluxo 3: Uso Programático
```python
from database.client import PostgreSQLClient, AnalisadorDados
from agents.personality import GerenciadorPersonalidades

# Seu código aqui
```

## 🔧 Dependências

- **psycopg2-binary**: Conexão com PostgreSQL
- **httpx**: Requisições HTTP para Ollama
- **openai**: SDK OpenAI
- **python-dotenv**: Carregamento de variáveis de ambiente

## 📝 Variáveis de Ambiente (.env)

```ini
# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OpenAI (opcional)
# OPENAI_API_KEY=sua-chave
# OPENAI_MODEL=gpt-4o-mini

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=postgres
DB_PASSWORD=sua_senha

# Provedor (ollama ou openai)
AI_PROVIDER=ollama

# Personalidade padrão
PERSONALIDADE_AGENTE=assistente
```

## 🎯 Próximos Passos

- [ ] Adicionar testes unitários em `tests/`
- [ ] Criar arquivo `requirements.txt`
- [ ] Adicionar logging
- [ ] Criar API REST em `api/`
- [ ] Adicionar mais personalidades
- [ ] Suporte a múltiplos bancos de dados

## 📞 Suporte

Veja os arquivos em `/docs` para documentação detalhada.
