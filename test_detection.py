"""
Quick test of improved framework detection on Bear agent only.
"""
from src.agent_client import AgentClient
from src.attacks import AttackGenerator
from src.evaluator import ResponseEvaluator
import time

client = AgentClient()
evaluator = ResponseEvaluator()

print("="*70)
print("🧪 TESTING IMPROVED DETECTION ON BEAR AGENT")
print("="*70)

# Get framework detection attacks
framework_attacks = AttackGenerator.get_framework_detection_attacks()

print(f"\nTesting {len(framework_attacks)} framework detection attacks...\n")

for i, attack in enumerate(framework_attacks, 1):
    print(f"\n[{i}/{len(framework_attacks)}] {attack.name}")
    print(f"Prompt: {attack.prompt[:100]}...")
    
    # Send attack
    response = client.send_message('bear', attack.prompt)
    
    if response.success:
        print(f"Response: {response.response[:200]}...")
        
        # Evaluate
        result = evaluator.evaluate_response(
            agent_name='bear',
            attack_category='framework_detection',
            attack_name=attack.name,
            prompt=attack.prompt,
            response=response.response
        )
        
        if result.indicators:
            print(f"✅ INDICATORS FOUND: {result.indicators}")
        else:
            print("⚠️  No indicators detected")
    else:
        print(f"❌ Error: {response.error}")
    
    time.sleep(1.0)

print("\n" + "="*70)
print("Test complete!")
print("="*70)
