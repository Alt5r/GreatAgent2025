#!/usr/bin/env python3
"""
Demo script to showcase the red teaming system capabilities.
Run this after setup to verify everything works.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import (
    AGENTS,
    ATTACK_CATEGORIES,
    AgentClient,
    AttackGenerator,
    ResponseEvaluator
)


def main():
    """Run a quick demo."""
    print("=" * 70)
    print("AI AGENT RED TEAMING SYSTEM - DEMO")
    print("=" * 70)
    
    # System info
    print("\n📊 SYSTEM CAPABILITIES:")
    print(f"  • Available Agents: {len(AGENTS)}")
    print(f"    {', '.join(AGENTS)}")
    print(f"  • Attack Categories: {len(ATTACK_CATEGORIES)}")
    print(f"    {', '.join(ATTACK_CATEGORIES)}")
    
    # Count attacks
    all_attacks = AttackGenerator.get_all_attacks()
    print(f"  • Total Attack Patterns: {len(all_attacks)}")
    
    # Breakdown by category
    by_category = {}
    for attack in all_attacks:
        by_category[attack.category] = by_category.get(attack.category, 0) + 1
    
    print("\n🎯 ATTACK DISTRIBUTION:")
    for category, count in sorted(by_category.items()):
        print(f"  • {category:30} {count:2} attacks")
    
    # Test connection
    print("\n🔌 CONNECTION TEST:")
    try:
        client = AgentClient()
        print("  ✅ Agent client initialized")
        print("  ✅ API endpoint configured")
        print(f"  ✅ Base URL: {client.base_url}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return
    
    # Evaluator test
    print("\n🔬 EVALUATION SYSTEM:")
    evaluator = ResponseEvaluator()
    print(f"  ✅ Vulnerability patterns: {len(evaluator.compiled_vulnerability_patterns)}")
    print(f"  ✅ Refusal patterns: {len(evaluator.compiled_refusal_patterns)}")
    print(f"  ✅ System prompt patterns: {len(evaluator.compiled_system_prompt_patterns)}")
    
    print("\n" + "=" * 70)
    print("SYSTEM READY!")
    print("=" * 70)
    
    print("\n🚀 QUICK START COMMANDS:")
    print("  # Test one agent with jailbreak attacks")
    print("  python main.py --mode quick --agents bear")
    print()
    print("  # Probe all agents for identification")
    print("  python main.py --mode probe")
    print()
    print("  # Full comprehensive assessment")
    print("  python main.py --mode full")
    print()
    print("  # Run example scripts")
    print("  python examples/quickstart.py")
    
    print("\n📚 DOCUMENTATION:")
    print("  • README.md - Complete documentation")
    print("  • QUICKSTART.md - Quick reference")
    print("  • PROJECT_SUMMARY.md - Project overview")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
