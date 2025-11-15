"""
Quick test of dataset integration
"""

from src.dataset_loader import DatasetLoader, KnowledgeBaseManager

print("=" * 80)
print("DATASET INTEGRATION TEST")
print("=" * 80)

# Test loader
loader = DatasetLoader()
print("\n📊 Loading datasets...")
loader.load_all()

stats = loader.get_dataset_stats()
print("\n✅ Loaded successfully!")
print(f"  • Benign: {stats['benign']['total']} test cases")
print(f"  • Harmful: {stats['harmful']['total']} test cases")
print(f"  • Jailbreak: {stats['jailbreak']['total']} prompts")
print(f"  • TOTAL: {sum(s['total'] for s in stats.values())} dataset attacks available")

# Show benign topics
print("\n📋 Benign Test Case Topics:")
for topic, count in list(stats['benign']['topics'].items())[:5]:
    print(f"  • {topic}: {count}")

# Show jailbreak topics
print("\n🔓 Jailbreak Prompt Categories:")
for topic, count in list(stats['jailbreak']['topics'].items())[:5]:
    print(f"  • {topic}: {count}")

# Get sample attacks
print("\n🎯 Sample Attacks:")
benign = loader.get_benign_attacks(limit=1)
harmful = loader.get_harmful_attacks(limit=1)
jailbreak = loader.get_jailbreak_attacks(limit=1)

print(f"\n  1. Benign: {benign[0]['prompt'][:80]}...")
print(f"  2. Harmful: {harmful[0]['prompt'][:80]}...")
print(f"  3. Jailbreak: {jailbreak[0]['prompt'][:80]}...")

# Test knowledge base
print("\n" + "=" * 80)
print("KNOWLEDGE BASE TEST")
print("=" * 80)

kb = KnowledgeBaseManager()
kb.load()

agents = kb.get_all_agents()
print(f"\n📚 Agent Knowledge Base:")
print(f"  • Total agents: {len(agents)}")
print(f"  • Agents: {', '.join(agents)}")

# Show one agent details
bear_info = kb.get_agent_info('bear')
print(f"\n🐻 Sample Agent (Bear):")
print(f"  • Endpoint: {bear_info['endpoint']}")
print(f"  • Status: {bear_info['status']}")
print(f"  • Framework: {bear_info['known_characteristics']['framework']}")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - SYSTEM READY")
print("=" * 80)
print("\nNext steps:")
print("  1. Run: python run_dataset_attacks.py --agent bear --limit 5")
print("  2. Review results in results/ directory")
print("  3. Run comparative analysis when ready")
