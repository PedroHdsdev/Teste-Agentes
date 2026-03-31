#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar e demonstrar todas as personalidades disponíveis.
"""

from agents.personality import GerenciadorPersonalidades


def main():
    """Exibe todas as personalidades e seus detalhes."""
    
    print("=" * 80)
    print("🎭 PERSONALIDADES DISPONÍVEIS NA PLATAFORMA".center(80))
    print("=" * 80)
    
    personalidades = GerenciadorPersonalidades.listar_personalidades()
    
    for idx, (chave, descricao) in enumerate(personalidades.items(), 1):
        pers = GerenciadorPersonalidades.obter_personalidade(chave)
        
        print(f"\n{idx}. {pers.nome.upper()}")
        print("-" * 80)
        print(f"   Chave: {chave}")
        print(f"   Descrição: {descricao}")
        print(f"\n   System Prompt:")
        print("   " + "\n   ".join(pers.system_prompt.split("\n")))
    
    print("\n" + "=" * 80)
    print(f"Total de personalidades: {len(personalidades)}")
    print("=" * 80)
    
    # Exemplo de uso
    print("\n📖 EXEMPLO DE USO:")
    print("-" * 80)
    print("""
    from agents.personality import GerenciadorPersonalidades
    
    # Obter uma personalidade específica
    pers = GerenciadorPersonalidades.obter_personalidade("marketing")
    
    # Acessar propriedades
    print(pers.nome)               # "Marketing"
    print(pers.descricao)          # Descrição detalhada
    print(pers.system_prompt)      # Prompt para usar com LLM
    
    # Listar todas as personalidades
    todas = GerenciadorPersonalidades.listar_personalidades()
    for chave, descricao in todas.items():
        print(f"{chave}: {descricao}")
    """)


if __name__ == "__main__":
    main()
