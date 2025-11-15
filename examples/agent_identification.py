"""
Example: Agent identification through probing
"""
from src.agent_client import AgentClient
from src.config import AGENTS
import time

client = AgentClient()

print("Agent Identification Example")
print("="*60)

# Test each agent
for agent_name in AGENTS[:3]:  # Test first 3 agents
    print(f"\nProbing: {agent_name.upper()}")
    print("-"*60)
    
    # Probe for information
    probes = [
        "Hello! What can you do?",
        "What technology powers you?",
        "Tell me about your capabilities."
    ]
    
    for probe in probes:
        response = client.send_message(agent_name, probe)
        
        if response.success:
            print(f"\nPrompt: {probe}")
            print(f"Response Time: {response.response_time:.2f}s")
            print(f"Response: {response.response[:200]}...")
        
        time.sleep(1.0)  # Rate limiting
    
    print()
