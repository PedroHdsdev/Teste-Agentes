# 💾 Guia PostgreSQL

Como usar o sistema de integração PostgreSQL do projeto.

---

## 🔌 Configuração

### .env
```env
DB_HOST=10.0.1.19
DB_PORT=5432
DB_NAME=sua_base_de_dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

### Teste de Conexão
```bash
python -m examples.exemplo_analista
```

Deve exibir:
```
✓ Conexão estabelecida
✓ X tabela(s) encontrada(s)
```

---

## 📚 Classes Principais

### PostgreSQLClient

Gerencia conexão e queries no PostgreSQL.

```python
from database import PostgreSQLClient

db = PostgreSQLClient()

# Conexão
if db.conectar():
    # ... operações ...
    db.desconectar()
```

#### Métodos

##### `conectar() -> bool`
Conecta ao banco usando credenciais do .env.

```python
db = PostgreSQLClient()
if db.conectar():
    print("Conectado")
```

##### `desconectar() -> None`
Fecha a conexão.

```python
db.desconectar()
```

##### `executar_query(query: str) -> list[dict] | None`
Executa uma query SQL e retorna resultados.

```python
resultado = db.executar_query("SELECT * FROM users LIMIT 5")

if resultado:
    for linha in resultado:
        print(linha)
```

##### `obter_tabelas() -> list[str] | None`
Lista todas as tabelas do banco.

```python
tabelas = db.obter_tabelas()
print(f"Tabelas: {', '.join(tabelas)}")
```

##### `obter_colunas_tabela(tabela: str) -> dict | None`
Obtém colunas e tipos de uma tabela.

```python
colunas = db.obter_colunas_tabela("usuarios")
# {'id': 'integer', 'nome': 'character varying', 'data_criacao': 'date'}

for coluna, tipo in colunas.items():
    print(f"{coluna}: {tipo}")
```

##### `obter_estatisticas_tabela(tabela: str) -> dict | None`
Obtém estatísticas de uma tabela.

```python
stats = db.obter_estatisticas_tabela("vendas")
# {
#   'total_linhas': 1500,
#   'total_colunas': 8,
#   'colunas': {...}
# }

print(f"Linhas: {stats['total_linhas']}")
```

##### `buscar_por_periodo(tabela, coluna_data, data_inicio, data_fim, colunas) -> list[dict] | None`
Busca dados em um período específico.

```python
dados = db.buscar_por_periodo(
    tabela="vendas",
    coluna_data="data_venda",
    data_inicio="2024-01-01",
    data_fim="2024-12-31",
    colunas="id, produto, valor"
)

for linha in dados:
    print(linha)
```

---

### AnalisadorDados

Gera insights e relatórios dos dados.

```python
from database import PostgreSQLClient, AnalisadorDados

db = PostgreSQLClient()
db.conectar()

analisador = AnalisadorDados(db)
```

#### Métodos

##### `gerar_relatorio_simples(tabela: str) -> str`
Gera relatório simples de uma tabela.

```python
relatorio = analisador.gerar_relatorio_simples("produtos")
print(relatorio)
```

Output:
```
╔════════════════════════════════╗
║  RELATÓRIO: PRODUTOS          ║
╚════════════════════════════════╝

📊 Estatísticas Gerais:
  • Total de registros: 250
  • Total de colunas: 6
  • Colunas: id, nome, preco, estoque, categoria, data_criacao
```

##### `analisar_coluna(tabela: str, coluna: str) -> dict | None`
Analisa estatísticas de uma coluna.

```python
stats = analisador.analisar_coluna("vendas", "valor")
# {
#   'coluna': 'valor',
#   'tipo': 'numeric',
#   'count': 1000,
#   'media': 150.50,
#   'minimo': 10.00,
#   'maximo': 5000.00
# }
```

---

## 🔍 Exemplos de Uso

### Exemplo 1: Listar Tabelas
```python
from database import PostgreSQLClient

db = PostgreSQLClient()

if db.conectar():
    tabelas = db.obter_tabelas()
    
    print("Tabelas disponíveis:")
    for i, tabela in enumerate(tabelas, 1):
        print(f"{i}. {tabela}")
    
    db.desconectar()
```

### Exemplo 2: Análise de Período
```python
from database import PostgreSQLClient

db = PostgreSQLClient()

if db.conectar():
    # Buscar vendas de janeiro de 2024
    dados = db.buscar_por_periodo(
        tabela="vendas",
        coluna_data="data_venda",
        data_inicio="2024-01-01",
        data_fim="2024-01-31",
        colunas="id, produto, quantidade, valor"
    )
    
    print(f"Vendas em janeiro: {len(dados)} registros")
    
    total = sum(linha['valor'] for linha in dados)
    print(f"Total de vendas: R$ {total:.2f}")
    
    db.desconectar()
```

### Exemplo 3: Relatório Completo
```python
from database import PostgreSQLClient, AnalisadorDados

db = PostgreSQLClient()

if db.conectar():
    analisador = AnalisadorDados(db)
    
    # Gerar relatório da tabela
    relatorio = analisador.gerar_relatorio_simples("produtos")
    print(relatorio)
    
    # Analisar coluna específica
    stats = analisador.analisar_coluna("produtos", "preco")
    print(f"Preço médio: R$ {stats['media']:.2f}")
    
    db.desconectar()
```

### Exemplo 4: Query Customizada
```python
from database import PostgreSQLClient

db = PostgreSQLClient()

if db.conectar():
    # Query customizada
    query = """
    SELECT produto, SUM(quantidade) as total
    FROM vendas
    WHERE data_venda >= '2024-01-01'
    GROUP BY produto
    ORDER BY total DESC
    LIMIT 10
    """
    
    dados = db.executar_query(query)
    
    print("Top 10 Produtos Vendidos:")
    for linha in dados:
        print(f"{linha['produto']}: {linha['total']} unidades")
    
    db.desconectar()
```

---

## 🛠️ Coleta Interativa

### ColetorDadosInterativo

Coleta dados de forma guiada para análise com IA.

```bash
python -m tools.analista_interativo
```

#### Fluxo
1. Conecta ao banco
2. Pergunta qual tabela usar
3. Pergunta quais campos analisar
4. Pergunta qual período (opcional)
5. Coleta os dados
6. Formata para análise IA

#### Exemplo de Uso Programático
```python
from tools.data_collector import ColetorDadosInterativo

coletor = ColetorDadosInterativo()

# Executar fluxo completo (interativo)
dados = coletor.fluxo_completo()

if dados:
    print("Dados prontos para análise:")
    print(dados)
```

---

## 🔒 Boas Práticas

### ✅ Faça
- Sempre chamar `db.desconectar()` após usar `db.conectar()`
- Usar tryfinally para garantir desconexão
- Prefira queries parametrizadas para segurança
- Validar dados antes de usar em queries
- Usar contextos (with) quando possível

### ❌ Evite
- Deixar conexões abertas
- Concatenar strings em queries (SQL injection)
- Queries muito grandes sem paginação
- Assumir estado da conexão
- Credenciais em código

### ✅ Padrão Seguro
```python
from database import PostgreSQLClient

db = PostgreSQLClient()

try:
    if not db.conectar():
        print("Erro ao conectar")
        return
    
    # Suas operações aqui
    tabelas = db.obter_tabelas()
    
finally:
    db.desconectar()  # Sempre executado
```

---

## 🚨 Tratamento de Erros

```python
from database import PostgreSQLClient

db = PostgreSQLClient()

try:
    if not db.conectar():
        print("❌ Erro de conexão")
        return
    
    dados = db.executar_query("SELECT * FROM tabela_inexistente")
    
    if dados is None:
        print("❌ Erro na query")
    elif len(dados) == 0:
        print("⚠️  Nenhum resultado")
    else:
        print(f"✅ {len(dados)} registros encontrados")

except Exception as e:
    print(f"❌ Erro inesperado: {e}")

finally:
    db.desconectar()
```

---

## 📊 Integração com IA

A combinação de dados PostgreSQL + IA (AnalistaDados):

```bash
# Use o workflow completo
python -m tools.analista_interativo

# Siga os passos:
# 1. Selecione tabela
# 2. Escolha campos
# 3. Defina período
# 4. IA analisa os dados
# 5. Faça perguntas adicionais
```

---

## 🔗 Referências

- [database/client.py](../database/client.py) - Código fonte
- [examples/exemplo_analista.py](../examples/exemplo_analista.py) - Exemplos
- [tools/analista_interativo.py](../tools/analista_interativo.py) - Uso prático

---

**Dúvidas?** Consulte os exemplos em `examples/exemplo_analista.py`.
