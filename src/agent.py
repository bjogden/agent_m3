import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

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
        self.system_prompt = SystemMessage(
            content="You are a helpful and witty AI agent. Keep your answers concise and smart."
        )

    def run(self, user_input: str) -> str:
        messages = [self.system_prompt, HumanMessage(content=user_input)]
        response = self.llm.invoke(messages)
        return response.content

if __name__ == "__main__":
    agent = SimpleAgent()
    print("Agent initialized. Type 'exit' to quit.\n")
    
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["exit", "quit"]:
            break
        
        try:
            response = agent.run(user_prompt)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\nError: {e}\n")