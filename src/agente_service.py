import os
from abc import ABC, abstractmethod
import httpx
from dotenv import load_dotenv
from openai import OpenAI
from agents.personality import GerenciadorPersonalidades, PersonalidadeBase


SYSTEM_PROMPT = (
    "Voce e um assistente inteligente, direto e util. "
    "Responda em portugues do Brasil, de forma clara e objetiva."
)


class AgenteChatBase(ABC):
    def __init__(self, model: str, system_prompt: str = SYSTEM_PROMPT, personalidade: PersonalidadeBase | None = None) -> None:
        self.model = model
        self.personalidade = personalidade
        self.system_prompt = personalidade.system_prompt if personalidade else system_prompt
        self.historico: list[dict[str, str]] = []

    @property
    @abstractmethod
    def nome_provider(self) -> str:
        pass

    def obter_mensagem_inicial(self) -> str:
        return (
            f"Agente iniciado com {self.nome_provider} usando o modelo '{self.model}' "
            "(digite 'sair' para encerrar)\n"
        )

    def perguntar(self, pergunta: str) -> str:
        self.historico.append({"role": "user", "content": pergunta})
        mensagem = self._gerar_resposta()

        if mensagem:
            self.historico.append({"role": "assistant", "content": mensagem})
            return mensagem

        return f"{self.nome_provider} nao retornou uma resposta."

    def conversar(self, mensagens: list[dict[str, str]]) -> str:
        """
        Conversa usando um histórico de mensagens externo.
        Útil para manter histórico customizado.
        
        Args:
            mensagens: Lista de mensagens com role e content
            
        Returns:
            Resposta da IA
        """
        # Salvar histórico atual
        historico_backup = self.historico.copy()
        
        try:
            # Usar mensagens fornecidas
            self.historico = [msg for msg in mensagens if msg.get("role") != "system"]
            return self._gerar_resposta()
        finally:
            # Restaurar histórico
            self.historico = historico_backup

    def _obter_mensagens(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": self.system_prompt}, *self.historico]

    @abstractmethod
    def verificar_configuracao(self) -> None:
        pass

    @abstractmethod
    def _gerar_resposta(self) -> str:
        pass


class OllamaAgent(AgenteChatBase):
    def __init__(self, ollama_url: str, model: str, personalidade: PersonalidadeBase | None = None) -> None:
        super().__init__(model=model, personalidade=personalidade)
        self.ollama_url = ollama_url

    @property
    def nome_provider(self) -> str:
        return "Ollama"

    def verificar_configuracao(self) -> None:
        try:
            resposta = httpx.get(f"{self.ollama_url}/api/tags", timeout=5.0)
            resposta.raise_for_status()
        except httpx.HTTPError as exc:
            raise RuntimeError(
                "Nao consegui acessar o Ollama local.\n"
                "Instale e inicie o Ollama, depois baixe um modelo.\n"
                "Exemplo:\n"
                "1. Instalar: https://ollama.com/download\n"
                f"2. Baixar modelo: ollama pull {self.model}\n"
                "3. Rodar o chat novamente."
            ) from exc

    def _gerar_resposta(self) -> str:
        payload = {
            "model": self.model,
            "messages": self._obter_mensagens(),
            "stream": False,
        }

        try:
            resposta = httpx.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=120.0,
            )
            resposta.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return (
                    f"O modelo '{self.model}' nao foi encontrado no Ollama.\n"
                    f"Execute: ollama pull {self.model}"
                )
            return f"Ollama respondeu com erro HTTP {exc.response.status_code}."
        except httpx.HTTPError:
            return (
                "Falha ao conversar com o Ollama. "
                "Confira se o aplicativo esta aberto e funcionando."
            )

        dados = resposta.json()
        return dados.get("message", {}).get("content", "").strip()


class OpenAIAgent(AgenteChatBase):
    def __init__(self, api_key: str, model: str, personalidade: PersonalidadeBase | None = None) -> None:
        super().__init__(model=model, personalidade=personalidade)
        self.api_key = api_key
        self.cliente = OpenAI(api_key=api_key)

    @property
    def nome_provider(self) -> str:
        return "OpenAI"

    def verificar_configuracao(self) -> None:
        if not self.api_key:
            raise RuntimeError(
                "Nao encontrei a variavel OPENAI_API_KEY.\n"
                "Adicione sua chave no arquivo .env para usar a OpenAI.\n"
                f"Modelo configurado: {self.model}"
            )

    def _gerar_resposta(self) -> str:
        try:
            resposta = self.cliente.chat.completions.create(
                model=self.model,
                messages=self._obter_mensagens(),
            )
        except Exception as exc:
            return f"Falha ao conversar com a OpenAI: {exc}"

        return (resposta.choices[0].message.content or "").strip()


def criar_agente(nome_personalidade: str | None = None) -> AgenteChatBase:
    load_dotenv()

    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if nome_personalidade is None:
        nome_personalidade = os.getenv("PERSONALIDADE_AGENTE", "assistente").strip().lower()

    try:
        personalidade = GerenciadorPersonalidades.obter_personalidade(nome_personalidade)
    except ValueError as exc:
        raise RuntimeError(f"Erro ao carregar personalidade: {exc}") from exc

    if provider == "ollama":
        return OllamaAgent(
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            personalidade=personalidade,
        )

    if provider == "openai":
        return OpenAIAgent(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            personalidade=personalidade,
        )

    raise RuntimeError(
        "Provedor invalido em AI_PROVIDER.\n"
        "Use 'ollama' ou 'openai'."
    )
