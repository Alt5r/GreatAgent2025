"""
Example: Systematic ASR calculation across attack types
"""
from src.orchestrator import RedTeamOrchestrator
from src.attacks import AttackGenerator
from src.evaluator import ResponseEvaluator

# Initialize
orchestrator = RedTeamOrchestrator(output_dir="results/asr_analysis")
evaluator = ResponseEvaluator()

print("ASR Calculation Example")
print("="*60)

# Test specific categories on specific agents
test_agents = ['bear', 'wolf']
test_categories = ['jailbreak', 'prompt_injection', 'system_prompt_extraction']

print(f"Testing agents: {test_agents}")
print(f"Attack categories: {test_categories}\n")

# Run attacks
results = orchestrator.run_attack_suite(
    agent_names=test_agents,
    attack_categories=test_categories,
    delay=1.0
)

# Calculate ASR
asr_stats = evaluator.calculate_asr(results)

print("\nASR Results:")
print("="*60)
print(f"Overall ASR: {asr_stats['overall_asr']:.2%}")
print(f"Total attacks: {asr_stats['total_attacks']}")
print(f"Successful: {asr_stats['successful_attacks']}")

print("\nBy Category:")
for category, data in asr_stats['by_category'].items():
    print(f"  {category:30} ASR: {data['asr']:6.2%} ({data['successful']}/{data['total']})")

print("\nBy Agent:")
for agent, data in asr_stats['by_agent'].items():
    print(f"  {agent:30} ASR: {data['asr']:6.2%} ({data['successful']}/{data['total']})")

# Save detailed results
orchestrator.save_results(results, "asr_detailed_results.json")
orchestrator.save_asr_report(results, "asr_summary.json")

print(f"\nResults saved to: results/asr_analysis/")
