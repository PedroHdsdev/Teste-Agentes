"""
Módulo para coleta interativa de dados do PostgreSQL.
"""

from database.client import PostgreSQLClient, AnalisadorDados
from datetime import datetime


class ColetorDadosInterativo:
    """Classe para coletar dados de forma interativa."""

    def __init__(self):
        """Inicializa o coletor."""
        self.db = PostgreSQLClient()
        self.analisador = AnalisadorDados(self.db)
        self.dados_coletados = None
        self.metadados = {}

    def conectar(self) -> bool:
        """Conecta ao banco de dados."""
        return self.db.conectar()

    def desconectar(self) -> None:
        """Desconecta do banco."""
        self.db.desconectar()

    def listar_tabelas(self) -> list[str] | None:
        """Lista todas as tabelas disponíveis."""
        return self.db.obter_tabelas()

    def selecionar_tabela(self) -> str | None:
        """
        Permite ao usuário selecionar uma tabela interativamente.
        
        Returns:
            str: Nome da tabela selecionada
        """
        tabelas = self.listar_tabelas()
        
        if not tabelas:
            print("❌ Nenhuma tabela encontrada no banco de dados.")
            return None
        
        print("\n" + "="*60)
        print("📋 TABELAS DISPONÍVEIS")
        print("="*60)
        
        for i, tabela in enumerate(tabelas, 1):
            stats = self.db.obter_estatisticas_tabela(tabela)
            if stats:
                total_linhas = stats.get('total_linhas', '?')
                print(f"  {i}. {tabela} ({total_linhas} linhas)")
            else:
                print(f"  {i}. {tabela}")
        
        while True:
            try:
                entrada = input("\nSelecione o número da tabela (ou 'sair'): ").strip()
                if entrada.lower() == 'sair':
                    return None
                
                numero = int(entrada)
                if 1 <= numero <= len(tabelas):
                    return tabelas[numero - 1]
                else:
                    print("❌ Número inválido. Tente novamente.")
            except ValueError:
                print("❌ Entrada inválida. Digite um número ou 'sair'.")

    def selecionar_campos(self, tabela: str) -> str | None:
        """
        Permite ao usuário selecionar campos para coleta.
        
        Args:
            tabela: Nome da tabela
            
        Returns:
            str: Campos selecionados em formato SQL (ex: "campo1, campo2")
        """
        colunas = self.db.obter_colunas_tabela(tabela)
        
        if not colunas:
            print("❌ Nenhuma coluna encontrada na tabela.")
            return None
        
        lista_colunas = list(colunas.keys())
        
        print("\n" + "="*60)
        print("📊 COLUNAS DISPONÍVEIS")
        print("="*60)
        
        for i, coluna in enumerate(lista_colunas, 1):
            tipo = colunas[coluna]
            print(f"  {i}. {coluna} ({tipo})")
        
        print("\n💡 Dicas:")
        print("  - Digite os números separados por vírgula: 1,2,3")
        print("  - Digite '*' para selecionar todas")
        print("  - Digite 'sair' para cancelar")
        
        while True:
            entrada = input("\nSelecione os campos: ").strip()
            
            if entrada.lower() == 'sair':
                return None
            
            if entrada == '*':
                return ', '.join([f'"{c}"' for c in lista_colunas])
            
            try:
                indices = [int(x.strip()) - 1 for x in entrada.split(',')]
                
                if all(0 <= i < len(lista_colunas) for i in indices):
                    campos_selecionados = [lista_colunas[i] for i in indices]
                    return ', '.join([f'"{c}"' for c in campos_selecionados])
                else:
                    print("❌ Um ou mais números fora do intervalo. Tente novamente.")
            except ValueError:
                print("❌ Entrada inválida. Use números separados por vírgula ou '*'.")

    def selecionar_periodo(self, tabela: str, colunas_info: dict) -> tuple[str, str, str] | None:
        """
        Permite ao usuário selecionar um período de datas.
        
        Args:
            tabela: Nome da tabela
            colunas_info: Informações das colunas
            
        Returns:
            tuple: (coluna_data, data_inicio, data_fim) ou None se cancelado
        """
        # Procurar colunas de tipo data
        colunas_data = [col for col, tipo in colunas_info.items() 
                       if 'date' in tipo.lower() or 'timestamp' in tipo.lower()]
        
        if not colunas_data:
            print("\n⚠ Nenhuma coluna de data encontrada. Usaremos todos os dados.")
            return None
        
        print("\n" + "="*60)
        print("📅 COLUNAS DE DATA DISPONÍVEIS")
        print("="*60)
        
        for i, coluna in enumerate(colunas_data, 1):
            print(f"  {i}. {coluna}")
        
        while True:
            entrada = input("\nSelecione coluna de data (número ou 'não'): ").strip()
            
            if entrada.lower() == 'não':
                return None
            
            try:
                idx = int(entrada) - 1
                if 0 <= idx < len(colunas_data):
                    coluna_data = colunas_data[idx]
                    break
                else:
                    print("❌ Número inválido.")
            except ValueError:
                print("❌ Entrada inválida.")
        
        # Solicitar datas
        print("\n💡 Use formato: YYYY-MM-DD (ex: 2024-01-15)")
        
        while True:
            data_inicio = input("Data inicial: ").strip()
            data_fim = input("Data final: ").strip()
            
            try:
                datetime.strptime(data_inicio, "%Y-%m-%d")
                datetime.strptime(data_fim, "%Y-%m-%d")
                return (coluna_data, data_inicio, data_fim)
            except ValueError:
                print("❌ Formato de data inválido. Use YYYY-MM-DD")

    def coletar_dados(self, tabela: str, campos: str, 
                     coluna_data: str = None, 
                     data_inicio: str = None, 
                     data_fim: str = None) -> dict | None:
        """
        Coleta dados da tabela com base nos parâmetros.
        
        Args:
            tabela: Nome da tabela
            campos: Campos a selecionar
            coluna_data: Coluna de data para filtro
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            dict: Informações dos dados coletados
        """
        print("\n⏳ Coletando dados...")
        
        if coluna_data and data_inicio and data_fim:
            dados = self.db.buscar_por_periodo(
                tabela=tabela,
                coluna_data=coluna_data,
                data_inicio=data_inicio,
                data_fim=data_fim,
                colunas=campos
            )
        else:
            query = f'SELECT {campos} FROM "{tabela}" LIMIT 10000'
            dados = self.db.executar_query(query)
        
        if not dados:
            print("❌ Nenhum dado encontrado com os filtros especificados.")
            return None
        
        self.dados_coletados = dados
        self.metadados = {
            "tabela": tabela,
            "campos": campos,
            "coluna_data": coluna_data,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "total_registros": len(dados)
        }
        
        print(f"✅ {len(dados)} registros coletados com sucesso!")
        return self.metadados

    def exibir_preview_dados(self, max_linhas: int = 3) -> None:
        """
        Exibe um preview dos dados coletados.
        
        Args:
            max_linhas: Número máximo de linhas a exibir
        """
        if not self.dados_coletados:
            print("❌ Nenhum dado coletado ainda.")
            return
        
        print("\n" + "="*60)
        print("📊 PREVIEW DOS DADOS")
        print("="*60)
        
        for i, registro in enumerate(self.dados_coletados[:max_linhas], 1):
            print(f"\nRegistro {i}:")
            for chave, valor in registro.items():
                print(f"  {chave}: {valor}")
        
        if len(self.dados_coletados) > max_linhas:
            print(f"\n... e mais {len(self.dados_coletados) - max_linhas} registros")

    def obter_dados_para_analise(self) -> str:
        """
        Prepara os dados coletados para serem analisados pela IA.
        
        Returns:
            str: String formatada com os dados para análise
        """
        if not self.dados_coletados:
            return "Nenhum dado foi coletado."
        
        # Criar resumo estruturado
        resumo = f"""
╔════════════════════════════════════════════╗
║         DADOS COLETADOS PARA ANÁLISE       ║
╚════════════════════════════════════════════╝

📋 INFORMAÇÕES DA COLETA:
  • Tabela: {self.metadados.get('tabela')}
  • Total de registros: {self.metadados.get('total_registros')}
  • Campos: {self.metadados.get('campos')}
  • Período: {self.metadados.get('data_inicio')} a {self.metadados.get('data_fim')}

📊 PRIMEIROS REGISTROS:
"""
        
        for i, registro in enumerate(self.dados_coletados[:5], 1):
            resumo += f"\n{i}. {registro}"
        
        if len(self.dados_coletados) > 5:
            resumo += f"\n\n... e mais {len(self.dados_coletados) - 5} registros"
        
        # Estatísticas simples
        resumo += f"""

📈 DADOS BRUTOS PARA ANÁLISE IA:
```
{str(self.dados_coletados[:10])}
```

Por favor, analise esses dados e forneça insights, tendências e conclusões.
"""
        
        return resumo

    def fluxo_completo(self) -> str | None:
        """
        Executa o fluxo completo de coleta de dados de forma interativa.
        
        Returns:
            str: Dados formatados para análise pela IA, ou None se cancelado
        """
        if not self.conectar():
            print("❌ Falha ao conectar ao banco de dados.")
            return None
        
        try:
            # Passo 1: Selecionar tabela
            tabela = self.selecionar_tabela()
            if not tabela:
                return None
            
            print(f"\n✓ Tabela selecionada: {tabela}")
            
            # Passo 2: Selecionar campos
            campos = self.selecionar_campos(tabela)
            print(f"\n✓ Campos selecionados: {campos}")
            
            # Passo 3: Selecionar período
            colunas_info = self.db.obter_colunas_tabela(tabela)
            periodo = self.selecionar_periodo(tabela, colunas_info)
            
            coluna_data, data_inicio, data_fim = periodo if periodo else (None, None, None)
            
            # Passo 4: Coletar dados
            metadados = self.coletar_dados(
                tabela=tabela,
                campos=campos,
                coluna_data=coluna_data,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            if not metadados:
                return None
            
            # Passo 5: Preview dos dados
            self.exibir_preview_dados()
            
            # Passo 6: Preparar para análise
            dados_para_ia = self.obter_dados_para_analise()
            
            return dados_para_ia
        
        finally:
            self.desconectar()
