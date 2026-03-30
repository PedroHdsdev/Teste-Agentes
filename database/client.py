"""
Módulo para gerenciar conexões e operações com PostgreSQL.
"""

import os
from datetime import datetime
from typing import Any
import psycopg2
from psycopg2 import sql, Error
from dotenv import load_dotenv


class PostgreSQLClient:
    """Cliente para gerenciar conexões e queries ao PostgreSQL."""

    def __init__(self, host: str | None = None, port: int | None = None, 
                 database: str | None = None, user: str | None = None, 
                 password: str | None = None) -> None:
        """
        Inicializa o cliente PostgreSQL com credenciais.
        
        Se os parâmetros não forem fornecidos, tenta ler do .env
        """
        load_dotenv()
        
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = port or int(os.getenv("DB_PORT", "5432"))
        self.database = database or os.getenv("DB_NAME", "postgres")
        self.user = user or os.getenv("DB_USER", "postgres")
        self.password = password or os.getenv("DB_PASSWORD", "")
        
        self._connection = None

    def conectar(self) -> bool:
        """
        Estabelece conexão com o banco PostgreSQL.
        
        Returns:
            bool: True se conectado com sucesso, False caso contrário.
        """
        try:
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return False

    def desconectar(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def executar_query(self, query: str, params: tuple | None = None) -> list[dict] | None:
        """
        Executa uma query SELECT e retorna os resultados.
        
        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (para evitar SQL injection)
            
        Returns:
            list[dict]: Lista de dicionários com os resultados, ou None em caso de erro
        """
        if not self._connection:
            if not self.conectar():
                return None

        try:
            cursor = self._connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obter nomes das colunas
            colunas = [desc[0] for desc in cursor.description]
            
            # Converter resultados para lista de dicionários
            resultados = []
            for linha in cursor.fetchall():
                resultados.append(dict(zip(colunas, linha)))
            
            cursor.close()
            return resultados
        
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return None

    def buscar_por_periodo(self, tabela: str, coluna_data: str, 
                          data_inicio: str, data_fim: str,
                          colunas: str = "*") -> list[dict] | None:
        """
        Busca dados em um período específico.
        
        Args:
            tabela: Nome da tabela
            coluna_data: Nome da coluna de data
            data_inicio: Data inicial (formato YYYY-MM-DD)
            data_fim: Data final (formato YYYY-MM-DD)
            colunas: Colunas a selecionar (padrão: *)
            
        Returns:
            list[dict]: Dados encontrados
        """
        query = f"""
            SELECT {colunas}
            FROM "{tabela}"
            WHERE "{coluna_data}"::DATE >= %s::DATE
            AND "{coluna_data}"::DATE <= %s::DATE
            ORDER BY "{coluna_data}"
        """
        
        return self.executar_query(query, (data_inicio, data_fim))

    def obter_tabelas(self) -> list[str] | None:
        """
        Obtém lista de todas as tabelas do banco.
        
        Returns:
            list[str]: Nomes das tabelas
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """
        
        resultados = self.executar_query(query)
        if resultados:
            return [r['table_name'] for r in resultados]
        return None

    def obter_colunas_tabela(self, tabela: str) -> dict[str, str] | None:
        """
        Obtém informações sobre as colunas de uma tabela.
        
        Args:
            tabela: Nome da tabela
            
        Returns:
            dict: Dicionário com nomes das colunas e tipos de dados
        """
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        
        resultados = self.executar_query(query, (tabela,))
        if resultados:
            return {r['column_name']: r['data_type'] for r in resultados}
        return None

    def obter_estatisticas_tabela(self, tabela: str) -> dict[str, Any] | None:
        """
        Obtém estatísticas básicas de uma tabela.
        
        Args:
            tabela: Nome da tabela
            
        Returns:
            dict: Informações sobre total de linhas, número de colunas, etc
        """
        # Total de linhas
        query_count = f'SELECT COUNT(*) as total FROM "{tabela}"'
        result_count = self.executar_query(query_count)
        
        # Informações das colunas
        colunas = self.obter_colunas_tabela(tabela)
        
        if result_count and colunas:
            return {
                "total_linhas": result_count[0]['total'],
                "total_colunas": len(colunas),
                "colunas": colunas
            }
        return None


class AnalisadorDados:
    """Classe para análise de dados do PostgreSQL."""

    def __init__(self, db_client: PostgreSQLClient) -> None:
        """
        Inicializa o analisador com um cliente PostgreSQL.
        
        Args:
            db_client: Instância de PostgreSQLClient
        """
        self.db = db_client

    def gerar_relatorio_periodo(self, tabela: str, coluna_data: str,
                               data_inicio: str, data_fim: str) -> str:
        """
        Gera um relatório resumido dos dados de um período.
        
        Args:
            tabela: Nome da tabela
            coluna_data: Coluna com data
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            
        Returns:
            str: Relatório resumido em texto
        """
        # Buscar dados
        dados = self.db.buscar_por_periodo(tabela, coluna_data, data_inicio, data_fim)
        
        if not dados:
            return f"Nenhum dado encontrado para a tabela '{tabela}' entre {data_inicio} e {data_fim}."
        
        # Gerar relatório
        relatorio = f"""
╔════════════════════════════════════════════╗
║          RELATÓRIO DE DADOS                ║
╚════════════════════════════════════════════╝

📊 INFORMAÇÕES GERAIS
└─ Tabela: {tabela}
└─ Período: {data_inicio} a {data_fim}
└─ Total de registros: {len(dados)}

📌 ESTRUTURA DOS DADOS
└─ Colunas: {', '.join(dados[0].keys())}

📈 PRIMEIROS 5 REGISTROS
"""
        
        # Mostrar primeiros 5 registros
        for i, registro in enumerate(dados[:5], 1):
            relatorio += f"\n{i}. {registro}"
        
        if len(dados) > 5:
            relatorio += f"\n\n... e mais {len(dados) - 5} registros"
        
        # Estatísticas adicionais
        relatorio += f"""

📊 ANÁLISE RÁPIDA
└─ Primeiro registro: {dados[0] if dados else 'N/A'}
└─ Último registro: {dados[-1] if dados else 'N/A'}
└─ Total de colunas: {len(dados[0]) if dados else 0}

"""
        
        return relatorio

    def listar_tabelas_disponiveis(self) -> str:
        """
        Lista todas as tabelas disponíveis no banco.
        
        Returns:
            str: Relatório com as tabelas
        """
        tabelas = self.db.obter_tabelas()
        
        if not tabelas:
            return "Nenhuma tabela encontrada no banco de dados."
        
        relatorio = """
╔════════════════════════════════════════════╗
║       TABELAS DISPONÍVEIS                  ║
╚════════════════════════════════════════════╝

"""
        for i, tabela in enumerate(tabelas, 1):
            stats = self.db.obter_estatisticas_tabela(tabela)
            if stats:
                relatorio += f"{i}. {tabela}\n"
                relatorio += f"   └─ Registros: {stats['total_linhas']}\n"
                relatorio += f"   └─ Colunas: {stats['total_colunas']}\n\n"
        
        return relatorio

    def analisar_coluna(self, tabela: str, coluna: str) -> str:
        """
        Análise de uma coluna específica.
        
        Args:
            tabela: Nome da tabela
            coluna: Nome da coluna
            
        Returns:
            str: Análise da coluna
        """
        query = f"""
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT "{coluna}") as distintos,
                COUNT(*) FILTER (WHERE "{coluna}" IS NULL) as nulos
            FROM "{tabela}"
        """
        
        resultado = self.db.executar_query(query)
        
        if resultado:
            r = resultado[0]
            return f"""
            Análise da Coluna: {coluna} (Tabela: {tabela})
            ├─ Total de valores: {r['total']}
            ├─ Valores únicos: {r['distintos']}
            └─ Valores nulos: {r['nulos']}
            """
        return "Erro ao analisar a coluna."
