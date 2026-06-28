import os
import time

import tiktoken
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default).lower()).lower() in ("1", "true", "yes")

def get_llm():
    """Dynamically configures the LLM based on environment variables."""
    model_provider = os.getenv("MODEL_PROVIDER", "local").lower()
    
    if model_provider == "cloud":
        print("🤖 Using Cloud Provider (OpenAI)...")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for cloud mode.")
        return ChatOpenAI(
            model=os.getenv("CLOUD_MODEL", "gpt-4o-mini"), 
            api_key=api_key
        )
    else:
        print("💻 Using Local Provider (Ollama)...")
        # Ollama exposes an OpenAI-compatible endpoint at localhost:11434/v1
        # Inside Docker, localhost needs to change to host.docker.internal
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        return ChatOpenAI(
            model=os.getenv("LOCAL_MODEL", "llama3"),
            base_url=base_url,
            api_key="ollama"  # Required placeholder
        )

class SimpleAgent:
    def __init__(self):
        self.llm = get_llm()
        self.stream_output = env_bool("STREAM_LLM_OUTPUT", False)
        self.system_prompt = SystemMessage(
            content="You are a helpful and witty AI agent. Keep your answers concise and smart."
        )

    def _output_token_count(self, content: str, response=None) -> int:
        usage = (response.usage_metadata or {}) if response else {}
        if usage.get("output_tokens") is not None:
            return usage["output_tokens"]

        model = getattr(self.llm, "model_name", None) or "gpt-4o-mini"
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(content))

    def run(self, user_input: str) -> tuple[str, float]:
        messages = [self.system_prompt, HumanMessage(content=user_input)]
        start = time.perf_counter()
        response = None

        if self.stream_output:
            parts: list[str] = []
            print("\nAgent: ", end="", flush=True)
            for chunk in self.llm.stream(messages):
                if chunk.content:
                    print(chunk.content, end="", flush=True)
                    parts.append(chunk.content)
            print()
            content = "".join(parts)
        else:
            response = self.llm.invoke(messages)
            content = response.content or ""

        elapsed = time.perf_counter() - start
        output_tokens = self._output_token_count(content, response)
        tokens_per_sec = output_tokens / elapsed if elapsed > 0 else 0.0
        return content, tokens_per_sec

if __name__ == "__main__":
    agent = SimpleAgent()
    print("Agent initialized. Type 'exit' to quit.\n")
    
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["exit", "quit"]:
            break
        
        try:
            response, tokens_per_sec = agent.run(user_prompt)
            if not agent.stream_output:
                print(f"\nAgent: {response}")
            print(f"({tokens_per_sec:.1f} tokens/sec)\n")
        except Exception as e:
            print(f"\nError: {e}\n")