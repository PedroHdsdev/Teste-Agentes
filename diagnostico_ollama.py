"""
Script para diagnosticar problemas com Ollama.
Verifica se Ollama está rodando e acessível.
"""

import os
import sys
import httpx
from dotenv import load_dotenv

def diagnosticar_ollama():
    """Diagnostica problema com Ollama."""
    
    print("="*60)
    print("🔍 DIAGNÓSTICO - OLLAMA")
    print("="*60)
    
    # Carregar .env
    load_dotenv()
    
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434").strip()
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2").strip()
    
    print(f"\n📋 CONFIGURAÇÃO ATUAL:")
    print(f"   OLLAMA_URL: {ollama_url}")
    print(f"   OLLAMA_MODEL: {ollama_model}")
    
    # Teste 1: Verificar se URL é válida
    print(f"\n🧪 TESTE 1: Verificar URL...")
    if not ollama_url.startswith("http"):
        print(f"   ❌ URL inválida: {ollama_url}")
        print(f"   ℹ️  Use: http://localhost:11434")
        return False
    print(f"   ✅ URL válida")
    
    # Teste 2: Tentar conectar
    print(f"\n🧪 TESTE 2: Conectar em {ollama_url}...")
    try:
        resposta = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
        print(f"   ✅ Ollama acessível!")
        print(f"   Status: {resposta.status_code}")
        
        if resposta.status_code == 200:
            modelos = resposta.json().get("models", [])
            print(f"\n   📦 Modelos instalados ({len(modelos)}):")
            if modelos:
                for modelo in modelos:
                    nome = modelo.get("name", "Desconhecido")
                    print(f"      • {nome}")
            else:
                print(f"      ❌ Nenhum modelo instalado!")
    except httpx.ConnectError:
        print(f"   ❌ Não consegui conectar em {ollama_url}")
        print(f"   📌 Possíveis causas:")
        print(f"      1. Ollama não está rodando")
        print(f"      2. URL incorreta em .env")
        print(f"      3. Ollama está em outro host/porta")
        return False
    except httpx.TimeoutException:
        print(f"   ❌ Timeout ao conectar (demora > 5s)")
        print(f"   📌 Possíveis causas:")
        print(f"      1. Ollama está muito lento")
        print(f"      2. Problema de rede")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Verificar se modelo está instalado
    print(f"\n🧪 TESTE 3: Verificar modelo '{ollama_model}'...")
    try:
        resposta = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
        modelos = [m.get("name", "") for m in resposta.json().get("models", [])]
        
        if ollama_model in modelos or any(ollama_model in m for m in modelos):
            print(f"   ✅ Modelo '{ollama_model}' encontrado!")
        else:
            print(f"   ❌ Modelo '{ollama_model}' NÃO está instalado")
            print(f"   📌 Para instalar:")
            print(f"      ollama pull {ollama_model}")
            
            if modelos:
                print(f"   📌 Modelos disponíveis:")
                for modelo in modelos[:3]:
                    print(f"      • {modelo}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao verificar modelo: {e}")
        return False
    
    # Teste 4: Testar chat
    print(f"\n🧪 TESTE 4: Testar chat...")
    try:
        payload = {
            "model": ollama_model,
            "messages": [{"role": "user", "content": "Olá"}],
            "stream": False,
        }
        
        resposta = httpx.post(
            f"{ollama_url}/api/chat",
            json=payload,
            timeout=30.0,
        )
        
        if resposta.status_code == 200:
            dados = resposta.json()
            conteudo = dados.get("message", {}).get("content", "").strip()
            print(f"   ✅ Chat funcionando!")
            print(f"   Resposta: {conteudo[:50]}...")
        else:
            print(f"   ❌ Erro HTTP {resposta.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao testar chat: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ TUDO OK! Ollama está funcionando corretamente!")
    print("="*60)
    return True

def sugerir_solucoes():
    """Sugerir soluções para problemas comuns."""
    
    print("\n" + "="*60)
    print("💡 SOLUÇÕES COMUNS")
    print("="*60)
    
    print("\n1️⃣  OLLAMA NÃO ESTÁ RODANDO")
    print("   Windows:")
    print("   • Abra o aplicativo Ollama")
    print("   • Ou: ollama serve")
    print("   ")
    print("   Linux:")
    print("   • ollama serve")
    print("   ")
    print("   macOS:")
    print("   • Abra o aplicativo Ollama")
    
    print("\n2️⃣  MODELO NÃO ESTÁ INSTALADO")
    print("   Execute:")
    print("   ollama pull llama3.2")
    print("   (ou outro modelo desejado)")
    
    print("\n3️⃣  URL INCORRETA")
    print("   Edite config/.env:")
    print("   OLLAMA_URL=http://localhost:11434")
    print("   OLLAMA_MODEL=llama3.2")
    
    print("\n4️⃣  PORTA DIFERENTE")
    print("   Se Ollama estiver em outra porta:")
    print("   OLLAMA_URL=http://localhost:11435")
    print("   (ou a porta que está usando)")
    
    print("\n5️⃣  HOST DIFERENTE")
    print("   Se Ollama estiver em outro computador:")
    print("   OLLAMA_URL=http://192.168.1.100:11434")

if __name__ == "__main__":
    print("\n")
    sucesso = diagnosticar_ollama()
    
    if not sucesso:
        print("\n")
        sugerir_solucoes()
        sys.exit(1)
    
    sys.exit(0)
