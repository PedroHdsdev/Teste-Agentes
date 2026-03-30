"""
Script principal para coleta de dados + análise com IA.
Fluxo: Seleciona tabela → Escolhe campos → Define período → Coleta dados → IA analisa
"""

from tools.data_collector import ColetorDadosInterativo
from src.agente_service import criar_agente


def main():
    """Fluxo completo de coleta e análise."""
    
    print("""
╔════════════════════════════════════════════╗
║  COLETA INTERATIVA + ANÁLISE COM IA       ║
╚════════════════════════════════════════════╝

Este programa irá:
1. ✅ Perguntar qual tabela você quer
2. ✅ Perguntar quais campos você quer
3. ✅ Perguntar qual período você quer
4. ✅ Coletar os dados do PostgreSQL
5. ✅ Passar os dados para a IA fazer análise

Vamos começar!
    """)
    
    # Passo 1: Coletar dados interativamente
    print("\n" + "="*60)
    print("PASSO 1: COLETA DE DADOS")
    print("="*60)
    
    coletor = ColetorDadosInterativo()
    dados_para_analise = coletor.fluxo_completo()
    
    if not dados_para_analise:
        print("\n❌ Coleta de dados cancelada.")
        return
    
    # Passo 2: Inicializar agente para análise
    print("\n" + "="*60)
    print("PASSO 2: ANÁLISE COM IA")
    print("="*60)
    
    try:
        agente = criar_agente(nome_personalidade="analista_dados")
    except RuntimeError as e:
        print(f"❌ Erro ao criar agente: {e}")
        return
    
    print(f"\n🤖 Agente criado: {agente.personalidade.nome}")
    print(f"📝 Descrição: {agente.personalidade.descricao}\n")
    
    # Passo 3: Enviar dados para análise
    print("="*60)
    print("PASSO 3: ANÁLISE DOS DADOS")
    print("="*60)
    
    print("\n⏳ Enviando dados para a IA fazer primeira análise...")
    
    mensagens = [
        {
            "role": "user",
            "content": dados_para_analise
        }
    ]
    
    resposta = agente.conversar(mensagens)
    
    print(f"\n🤖 Análise da IA:\n{resposta}\n")
    
    # Passo 4: Loop interativo para perguntas
    print("="*60)
    print("PASSO 4: PERGUNTAS ADICIONAIS")
    print("="*60)
    print("\n💬 Você pode fazer perguntas adicionais sobre os dados.")
    print("   Digite 'sair' para finalizar.\n")
    
    # Manter contexto das mensagens
    mensagens.append({
        "role": "assistant",
        "content": resposta
    })
    
    while True:
        pergunta = input("Sua pergunta: ").strip()
        
        if pergunta.lower() == 'sair':
            print("\n✅ Análise finalizada!")
            break
        
        if not pergunta:
            print("⚠ Digite uma pergunta válida.\n")
            continue
        
        # Adicionar pergunta ao contexto
        mensagens.append({
            "role": "user",
            "content": pergunta
        })
        
        print("\n⏳ Aguardando resposta da IA...\n")
        
        # Obter resposta
        resposta = agente.conversar(mensagens)
        print(f"🤖 {resposta}\n")
        
        # Adicionar resposta ao contexto para próximas perguntas
        mensagens.append({
            "role": "assistant",
            "content": resposta
        })
    
    print("\n" + "="*60)
    print("OBRIGADO POR USAR O ANALISTA DE DADOS!")
    print("="*60)


if __name__ == "__main__":
    main()
