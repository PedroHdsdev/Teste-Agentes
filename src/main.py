import sys
from src.agente_service import criar_agente
from agents.personality import GerenciadorPersonalidades


def listar_personalidades() -> None:
    """Exibe todas as personalidades disponíveis."""
    personalidades = GerenciadorPersonalidades.listar_personalidades()
    print("\n📋 Personalidades disponíveis:\n")
    for chave, descricao in personalidades.items():
        print(f"  • {chave:<12} - {descricao}")
    print()


def main() -> None:
    personalidade = None
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "--listar" or comando == "-l":
            listar_personalidades()
            return
        
        if comando == "--help" or comando == "-h":
            print("Uso: python main.py [PERSONALIDADE]")
            print("\nExemplos:")
            print("  python main.py                    # Usa personalidade padrão")
            print("  python main.py criativa          # Começa com personalidade criativa")
            print("  python main.py --listar          # Lista todas as personalidades")
            print("  python main.py --help            # Mostra esta ajuda\n")
            return
        
        personalidade = comando

    try:
        agente = criar_agente(nome_personalidade=personalidade)
    except RuntimeError as erro:
        print(f"❌ {erro}")
        raise SystemExit(1)

    try:
        agente.verificar_configuracao()
    except RuntimeError as erro:
        print(f"❌ {erro}")
        raise SystemExit(1)

    nome_personalidade = agente.personalidade.nome if agente.personalidade else "Padrão"
    print(f"\n🤖 {agente.obter_mensagem_inicial()}")
    print(f"😊 Personalidade: {nome_personalidade}\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() == "sair":
            print("\n🤖 Agente: Até mais!\n")
            break

        if pergunta.lower() == "personalidades":
            listar_personalidades()
            continue

        resposta = agente.perguntar(pergunta)
        print(f"\n🤖 Agente: {resposta}\n")


if __name__ == "__main__":
    main()
