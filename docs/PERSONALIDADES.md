# 📚 Guia de Personalidades

Como criar e usar personalidades customizadas no projeto.

---

## 📖 O que é uma Personalidade?

Uma **personalidade** é um padrão de instrução que define como a IA se comporta. Cada personalidade tem:

- **nome**: Identificador único
- **descricao**: Resumo do tipo de resposta
- **system_prompt**: Instruções completas para a IA

---

## 🏗️ Arquitetura

### PersonalidadeBase (Classe Abstrata)

```python
from agents.personality import PersonalidadeBase

class MinhaPersonalidade(PersonalidadeBase):
    @property
    def nome(self):
        return "minha_personalidade"
    
    @property
    def descricao(self):
        return "Descrição da minha personalidade"
    
    @property
    def system_prompt(self):
        return "Instruções para o modelo de IA..."
```

### GerenciadorPersonalidades (Registry)

```python
from agents.personality import GerenciadorPersonalidades

# Registrar uma nova personalidade
gerenciador = GerenciadorPersonalidades()
gerenciador.registrar_personalidade(MinhaPersonalidade)

# Obter uma personalidade
personalidade = gerenciador.obter_personalidade("minha_personalidade")

# Listar todas
personalidades = gerenciador.listar_personalidades()
```

---

## 🎭 Personalidades Padrão

### 1. Assistente
```python
nome: "assistente"
descricao: "Um assistente versátil para qualquer pergunta"
system_prompt: "Você é um assistente útil, educado e informativo..."
```

### 2. Criativa
```python
nome: "criativa"
descricao: "Especialista em ideias novas e inovadoras"
system_prompt: "Você é criativa, imaginativa e gera ideias originais..."
```

### 3. Educador
```python
nome: "educador"
descricao: "Ensinador paciente que explica conceitos"
system_prompt: "Você é educador paciente que ensina e explica conceitos..."
```

### 4. Analítica
```python
nome: "analtica"
descricao: "Análises profundas com pensamento crítico"
system_prompt: "Você analisa temas em profundidade com pensamento crítico..."
```

### 5. Amigável
```python
nome: "amigvel"
descricao: "Conversas calorosas e empáticas"
system_prompt: "Você é amigável, empático e gosta de conversar..."
```

### 6. Pragmática
```python
nome: "pragmtica"
descricao: "Soluções práticas e diretas"
system_prompt: "Você é pragmático e oferece soluções práticas e diretas..."
```

### 7. AnalistaDados
```python
nome: "analista_dados"
descricao: "Especialista em análise de dados PostgreSQL"
system_prompt: "Você é especialista em análise de dados SQL..."
```

---

## ➕ Como Adicionar Uma Personalidade

### Passo 1: Criar a Classe

Editar [agents/personality.py](../agents/personality.py):

```python
class MinhaPersonalidade(PersonalidadeBase):
    """Descrição da minha personalidade."""
    
    @property
    def nome(self):
        return "minha_personalidade"
    
    @property
    def descricao(self):
        return "Breve descrição do comportamento"
    
    @property
    def system_prompt(self):
        return """
        Você é...
        
        Instruções detalhadas do comportamento esperado.
        Defina o tom, estilo, restrições e foco.
        """
```

### Passo 2: Registrar no GerenciadorPersonalidades

No final do arquivo `agents/personality.py`, adicionar no construtor:

```python
class GerenciadorPersonalidades:
    def __init__(self):
        # ... personalidades existentes ...
        self.registrar_personalidade(MinhaPersonalidade)
```

### Passo 3: Testar

```bash
# Listar personalidades
python -m src.main --listar

# Usar a nova personalidade
python -m src.main minha_personalidade
```

---

## 🎯 Exemplos de System Prompts

### Exemplo 1: Personalidade Técnica
```
Você é um especialista em programação Python.
Seu objetivo é ajudar desenvolvedores com:
- Boas práticas de código
- Debugging
- Arquitetura de projetos
- Explicação de conceitos

Sempre forneça exemplos de código bem estruturados.
```

### Exemplo 2: Personalidade Criativa
```
Você é um gerador de ideias criativas.
Seu objetivo é:
- Gerar ideias inovadoras
- Pensar fora da caixa
- Questionar pressupostos
- Explorar possibilidades

Seja imaginativo e encoraje pensamento livre.
```

### Exemplo 3: Personalidade Scientific
```
Você é um cientista cuidadoso.
Seu objetivo é:
- Fornecer informações baseadas em evidências
- Citar fontes quando possível
- Questionar suposições
- Explicar limitações

Sempre inclua advertências sobre o nível de confiança.
```

---

## 🔧 Propriedades Importantes

### nome
- **Tipo**: str
- **Uso**: Identificador único, usado na CLI
- **Restrições**: sem espaços, minúsculas
- **Exemplo**: `"assistente"`, `"criativa"`, `"meu_agente"`

### descricao
- **Tipo**: str
- **Uso**: Exibido ao listar personalidades
- **Tamanho**: 50-200 caracteres
- **Exemplo**: `"Especialista em análise de dados"`

### system_prompt
- **Tipo**: str
- **Uso**: Instruções para o modelo de IA
- **Tamanho**: 200-2000 caracteres
- **Dica**: Seja específico e claro sobre comportamento esperado

---

## 💡 Boas Práticas

### ✅ Faça
- Use nomes descritivos e in inglês/português consistente
- Escreva system_prompt claro e específico
- Teste a personalidade após criar
- Documente o propósito da personalidade
- Considere o tom e estilo desejado

### ❌ Evite
- Prompts muito longos ou ambíguos
- Personalidades que se contradizem
- Usar espaços em branco no nome
- Personalidades muito similares

---

## 🧪 Testando Personalidades

### Teste Manual
```bash
python -m src.main minha_personalidade
# Digite perguntas para testar o comportamento
```

### Teste Programático
```python
from agents.personality import GerenciadorPersonalidades
from src.agente_service import criar_agente

# Testar com Ollama
agente = criar_agente("minha_personalidade")
resposta = agente.conversar([{"role": "user", "content": "Teste"}])
print(resposta)
```

---

## 📊 Integração com Análise de Dados

A personalidade **AnalistaDados** é especial - ela é usada com ColetorDadosInterativo:

```bash
# Coleta dados PostgreSQL + IA especializada em dados
python -m tools.analista_interativo
```

Sistema Prompt da AnalistaDados:
```
Você é especialista em análise de dados SQL e Business Intelligence.
Seu objetivo é analisar dados de bancos de dados PostgreSQL...
```

---

## 🚀 Padrões Avançados

### Personalidade com Contexto
```python
class MinhaPersonalidadeContextual(PersonalidadeBase):
    def __init__(self, contexto=""):
        self.contexto = contexto
    
    @property
    def system_prompt(self):
        return f"""
        Contexto: {self.contexto}
        
        Você é...
        """
```

### Personalidade Multilíngue
```python
class PersonalidadeMultilíngue(PersonalidadeBase):
    @property
    def system_prompt(self):
        return """
        Você responde em português, inglês ou espanhol.
        Detecte automaticamente o idioma da pergunta
        e responda no mesmo idioma.
        """
```

---

## 📝 Checklist para Nova Personalidade

- [ ] Nome único (sem conflitos)
- [ ] System prompt específico e claro
- [ ] Descrição breve e descritiva
- [ ] Registrado no GerenciadorPersonalidades
- [ ] Testado via CLI
- [ ] Documentado

---

## 🔗 Referências

- [agents/personality.py](../agents/personality.py) - Código fonte
- [src/agente_service.py](../src/agente_service.py) - Como agentes usam personalidades
- [src/main.py](../src/main.py) - Como personalidades são selecionadas

---

**Dúvidas?** Consulte o código em `agents/personality.py` para ver a implementação completa.
