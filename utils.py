import os
import getpass
from pathlib import Path

from langchain_core.runnables.graph_mermaid import MermaidDrawMethod
from IPython.display import Image, display


def load_env_file(env_file=".env"):
    """Load environment variables from a .env file"""
    env_path = Path(env_file)

    if env_path.exists():
        print(f"Loading environment variables from {env_file}")
        with open(env_path, "r") as file:
            for line in file:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    # Split on first '=' only
                    if "=" in line:
                        key, value = line.split("=", 1)
                        # Remove quotes if present
                        value = value.strip("\"'")
                        os.environ[key.strip()] = value
        print("✅ Environment variables loaded from .env file")
    else:
        print(f"⚠️  No {env_file} file found")


def _set_env(var: str):
    """Set environment variable, prompting securely if not already set"""
    if not os.environ.get(var):
        print(f"🔑 {var} not found in environment")
        os.environ[var] = getpass.getpass(f"Enter {var}: ")
        print(f"✅ {var} has been set")
    else:
        print(f"✅ {var} already configured")


def setup_environment(env_vars=None, env_file=".env"):
    """
    Complete environment setup:
    1. Load from .env file if it exists
    2. Prompt for any missing required variables

    Args:
        env_vars: List of required environment variable names
        env_file: Path to .env file (default: ".env")
    """
    if env_vars is None:
        env_vars = [
            "GROQ_API_KEY",
            "OPENAI_API_KEY",
            "LANGSMITH_API_KEY",
            "TAVILY_API_KEY",
        ]

    print("🚀 Setting up environment variables...")

    # First, try to load from .env file
    load_env_file(env_file)

    # Then check/prompt for required variables
    print("\n📋 Checking required environment variables:")
    for var in env_vars:
        _set_env(var)

    print("\n🎉 Environment setup complete!")


def plot_graph(graph):
    try:
        # Try local rendering
        display(
            Image(
                graph.get_graph().draw_mermaid_png(
                    draw_method=MermaidDrawMethod.PYPPETEER
                )
            )
        )
    except Exception as e:
        print(f"Pyppeteer failed with error:\n`{e}`\n")
        # Fallback to ASCII
        # # ASCII visualization (always works)
        print("ASCII visualization of the Graph Structure:")
        print(graph.get_graph().draw_ascii())


# Example usage:
if __name__ == "__main__":
    # Setup with default variables
    # setup_environment(env_file="../.env")

    # Or specify your required variables
    setup_environment(
        ["LANGSMITH_API_KEY", "GROQ_API_KEY", "TAVILY_API_KEY"], env_file="../.env"
    )

    # Or use a different .env file
    # setup_environment(env_file="production.env")
