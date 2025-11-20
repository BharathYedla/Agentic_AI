from agno.agent import Agent
import inspect

try:
    sig = inspect.signature(Agent.__init__)
    print("Valid parameters:")
    for param in sig.parameters:
        print(f"- {param}")
except Exception as e:
    print(f"Error: {e}")
