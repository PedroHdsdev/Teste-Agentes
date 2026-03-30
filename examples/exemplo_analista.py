"""
Script de exemplo mostrando como usar o AnalisadorDados e PostgreSQLClient.
"""

from database.client import PostgreSQLClient, AnalisadorDados


def exemplo_basico():
    """Exemplo básico de conexão e queries."""
    print("\n" + "="*60)
    print("EXEMPLO 1: Conexão Básica")
    print("="*60)
    
    # Criar cliente
    db = PostgreSQLClient()
    
    # Conectar
    if db.conectar():
        print("✓ Conectado ao banco de dados com sucesso!")
        
        # Listar tabelas
        tabelas = db.obter_tabelas()
        if tabelas:
            print(f"\nTabelas encontradas: {', '.join(tabelas)}")
        
        # Obter estatísticas de uma tabela (se existir)
        if tabelas:
            primeira_tabela = tabelas[0]
            stats = db.obter_estatisticas_tabela(primeira_tabela)
            if stats:
                print(f"\nEstatísticas de '{primeira_tabela}':")
                print(f"  - Total de linhas: {stats['total_linhas']}")
                print(f"  - Total de colunas: {stats['total_colunas']}")
                print(f"  - Colunas: {', '.join(stats['colunas'].keys())}")
        
        db.desconectar()
        print("\n✓ Desconectado")
    else:
        print("✗ Falha ao conectar ao banco de dados")
        print("Verifique as configurações no arquivo .env")


def exemplo_query_customizada():
    """Exemplo de query customizada."""
    print("\n" + "="*60)
    print("EXEMPLO 2: Query Customizada")
    print("="*60)
    
    db = PostgreSQLClient()
    
    if db.conectar():
        # Query customizada
        query = 'SELECT * FROM "information_schema"."tables" LIMIT 5'
        
        print(f"\nExecutando query:\n  {query}\n")
        
        resultados = db.executar_query(query)
        
        if resultados:
            print(f"✓ Retornados {len(resultados)} registros")
            for i, registro in enumerate(resultados[:3], 1):
                print(f"\n  Registro {i}:")
                for chave, valor in registro.items():
                    print(f"    {chave}: {valor}")
            if len(resultados) > 3:
                print(f"\n  ... e mais {len(resultados) - 3} registros")
        else:
            print("✗ Query retornou vazio ou erro")
        
        db.desconectar()
    else:
        print("✗ Falha ao conectar")


def exemplo_busca_periodo():
    """Exemplo de busca com filtro de período."""
    print("\n" + "="*60)
    print("EXEMPLO 3: Busca por Período (Filtro de Data)")
    print("="*60)
    
    db = PostgreSQLClient()
    
    if db.conectar():
        print("""
Para usar busca por período, você precisa de:
  1. Uma tabela com coluna de data (DATE ou TIMESTAMP)
  2. Nomes dos campos a retornar

Exemplo:
  dados = db.buscar_por_periodo(
      tabela="minha_tabela",
      coluna_data="data_criacao",
      data_inicio="2024-01-01",
      data_fim="2024-12-31",
      colunas="id, nome, valor"
  )
        """)
        db.desconectar()
    else:
        print("✗ Falha ao conectar")


def exemplo_criar_dados_teste():
    """Exemplo de como criar dados de teste."""
    print("\n" + "="*60)
    print("EXEMPLO 4: Criar Dados de Teste")
    print("="*60)
    
    db = PostgreSQLClient()
    
    if db.conectar():
        print("""
Para usar o analista de dados, você precisa ter dados no PostgreSQL.

Script SQL para criar tabela de exemplo:

```sql
-- Criar tabela
CREATE TABLE teste_vendas (
    id SERIAL PRIMARY KEY,
    data_venda DATE,
    produto VARCHAR(100),
    quantidade INT,
    valor DECIMAL(10, 2)
);

-- Inserir dados de exemplo
INSERT INTO teste_vendas (data_venda, produto, quantidade, valor) VALUES
('2024-01-01', 'Produto A', 10, 100.00),
('2024-01-02', 'Produto B', 5, 50.00),
('2024-01-03', 'Produto A', 20, 200.00),
('2024-02-01', 'Produto C', 15, 150.00),
('2024-02-02', 'Produto B', 8, 80.00),
('2024-03-01', 'Produto A', 12, 120.00);

-- Confirmar inserção
SELECT * FROM teste_vendas;
```

Depois de executar este SQL, você pode usar:
  python main.py analista_dados
  
E pedir:
  "Mostra o relatório de vendas de janeiro de 2024"
        """)
        db.desconectar()


def exemplo_seguro():
    """Exemplo com tratamento de erros robusto."""
    print("\n" + "="*60)
    print("EXEMPLO 5: Tratamento Robusto de Erros")
    print("="*60)
    
    try:
        db = PostgreSQLClient()
        
        if not db.conectar():
            print("✗ Não foi possível conectar ao banco de dados")
            print("  - Verifique se PostgreSQL está rodando")
            print("  - Confirme as credenciais em .env")
            print("  - Verifique DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
            return
        
        print("✓ Conexão estabelecida")
        
        # Tentar operação segura
        tabelas = db.obter_tabelas()
        
        if tabelas is None:
            print("✗ Erro ao obter lista de tabelas")
        elif len(tabelas) == 0:
            print("⚠ Nenhuma tabela encontrada no banco de dados")
        else:
            print(f"✓ {len(tabelas)} tabela(s) encontrada(s)")
            for tabela in tabelas[:5]:  # Mostrar apenas as primeiras 5
                print(f"  - {tabela}")
            if len(tabelas) > 5:
                print(f"  ... e mais {len(tabelas) - 5}")
        
        db.desconectar()
        print("✓ Desconexão realizada")
    
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════╗
║  EXEMPLOS - ANALISTA DE DADOS / POSTGRESQL ║
╚════════════════════════════════════════════╝

Este script demonstra como usar as classes:
  - PostgreSQLClient
  - AnalisadorDados

Para rodar os exemplos:
  python exemplo_analista.py

Certifique-se que:
  1. PostgreSQL está instalado e rodando
  2. As variáveis de ambiente estão configuradas em .env
  3. O banco de dados existe
  4. Ter permissão de acesso
    """)
    
    # Rodar exemplo mais seguro por padrão
    exemplo_seguro()
    
    # Descomente os outros exemplos conforme necessário:
    # exemplo_basico()
    # exemplo_query_customizada()
    # exemplo_busca_periodo()
    # exemplo_criar_dados_teste()
