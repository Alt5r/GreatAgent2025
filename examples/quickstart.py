"""
Example: Quick start - Test a single agent with a few attacks
"""
from src.orchestrator import RedTeamOrchestrator
from src.attacks import AttackGenerator

# Initialize orchestrator
orchestrator = RedTeamOrchestrator(output_dir="results")

print("Quick Start Example: Testing Bear agent\n")

# Get a few attack examples
attacks = AttackGenerator.get_jailbreak_attacks()[:3]

# Test them
results = []
for attack in attacks:
    print(f"Testing: {attack.name}")
    result = orchestrator.run_single_attack('bear', attack, delay=1.0)
    results.append(result)
    
    print(f"  Vulnerable: {result.is_vulnerable}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Response: {result.response[:100]}...\n")

# Save results
orchestrator.save_results(results, "quickstart_results.json")
orchestrator.print_summary(results)
