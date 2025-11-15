"""
Dataset-driven Attack Runner
Runs systematic attacks using the official red teaming datasets
"""

import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent_client import AgentClient
from src.orchestrator import RedTeamOrchestrator
from src.dataset_loader import DatasetLoader, KnowledgeBaseManager
from src.visualizer import ResultVisualizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_dataset_attacks(agent_name: str = "bear", 
                       limit_per_type: int = 10,
                       include_custom_attacks: bool = True):
    """
    Run attacks using official datasets
    
    Args:
        agent_name: Target agent name
        limit_per_type: Number of attacks per dataset type
        include_custom_attacks: Whether to include custom attacks from attacks.py
    """
    logger.info("=" * 80)
    logger.info("DATASET-DRIVEN RED TEAMING SYSTEM")
    logger.info("=" * 80)
    
    # Initialize components
    config = Config()
    client = AgentClient(config)
    orchestrator = AttackOrchestrator(client, config)
    dataset_loader = DatasetLoader()
    kb_manager = KnowledgeBaseManager()
    
    # Load datasets
    logger.info("\n📊 Loading official red teaming datasets...")
    if not dataset_loader.load_all():
        logger.error("Failed to load datasets!")
        return
    
    # Show dataset stats
    stats = dataset_loader.get_dataset_stats()
    logger.info(f"\n✅ Dataset Statistics:")
    logger.info(f"  • Benign test cases: {stats['benign']['total']}")
    logger.info(f"  • Harmful test cases: {stats['harmful']['total']}")
    logger.info(f"  • Jailbreak prompts: {stats['jailbreak']['total']}")
    logger.info(f"  • Total dataset attacks: {sum(s['total'] for s in stats.values())}")
    
    # Get dataset attacks
    logger.info(f"\n🎯 Preparing attacks (limit: {limit_per_type} per type)...")
    dataset_attacks = dataset_loader.get_all_dataset_attacks(limit_per_type=limit_per_type)
    
    logger.info(f"  • Benign attacks: {len([a for a in dataset_attacks if a['category'] == 'dataset_benign'])}")
    logger.info(f"  • Harmful attacks: {len([a for a in dataset_attacks if a['category'] == 'dataset_harmful'])}")
    logger.info(f"  • Jailbreak attacks: {len([a for a in dataset_attacks if a['category'] == 'dataset_jailbreak'])}")
    
    # Optionally include custom attacks
    if include_custom_attacks:
        from src.attacks import AttackGenerator
        custom_attacks = AttackGenerator.get_all_attacks()
        custom_count = len(custom_attacks)
        logger.info(f"  • Custom attacks: {custom_count}")
        logger.info(f"  • Total attacks: {len(dataset_attacks) + custom_count}")
    else:
        logger.info(f"  • Total attacks: {len(dataset_attacks)}")
    
    # Run dataset attacks
    logger.info(f"\n🚀 Launching attacks against {agent_name}...")
    
    # Add dataset attacks to orchestrator
    for attack in dataset_attacks:
        orchestrator.attacks.append(attack)
    
    # Run attacks (include custom if requested)
    if include_custom_attacks:
        # Add custom attacks
        from src.attacks import AttackGenerator
        custom_attacks = AttackGenerator.get_all_attacks()
        for attack in custom_attacks:
            orchestrator.attacks.append(attack.to_dict())
        results = orchestrator.run_all_attacks(agent_name)
    else:
        # Run only dataset attacks
        orchestrator.attacks = dataset_attacks
        results = orchestrator.run_all_attacks(agent_name)
    
    # Save results
    logger.info("\n💾 Saving results...")
    result_file = orchestrator.save_results(agent_name)
    logger.info(f"  • Results saved to: {result_file}")
    
    # Generate ASR report
    logger.info("\n📊 Generating ASR report...")
    asr_report = orchestrator.calculate_asr(results)
    report_file = Path("results") / "asr_report_dataset.json"
    
    import json
    with open(report_file, 'w') as f:
        json.dump(asr_report, f, indent=2)
    logger.info(f"  • ASR report saved to: {report_file}")
    
    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("ATTACK SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Agent: {agent_name}")
    logger.info(f"Total attacks: {asr_report['total_attacks']}")
    logger.info(f"Successful attacks: {asr_report['successful_attacks']}")
    logger.info(f"Overall ASR: {asr_report['overall_asr']:.2%}")
    
    logger.info("\n📈 ASR by Category:")
    for category, data in asr_report['by_category'].items():
        logger.info(f"  • {category}: {data['asr']:.2%} ({data['successful']}/{data['total']})")
    
    # Update knowledge base with findings
    logger.info("\n📚 Updating knowledge base...")
    kb_manager.load()
    
    # Extract detected characteristics from results
    framework_detected = None
    model_detected = None
    company_detected = None
    
    for result in results:
        eval_result = result.get('evaluation', {})
        if eval_result.get('framework_detected'):
            framework_detected = eval_result.get('framework_detected')
        if eval_result.get('model_detected'):
            model_detected = eval_result.get('model_detected')
        if eval_result.get('company_detected'):
            company_detected = eval_result.get('company_detected')
    
    if framework_detected or model_detected or company_detected:
        kb_manager.update_agent_characteristics(
            agent_name,
            framework=framework_detected,
            model=model_detected,
            company=company_detected
        )
    
    # Add vulnerabilities
    for result in results:
        if result.get('evaluation', {}).get('is_vulnerable', False):
            vuln_desc = f"{result['category']}: {result['attack']}"
            kb_manager.add_vulnerability(agent_name, vuln_desc)
    
    kb_manager.save()
    logger.info(f"  • Knowledge base updated for {agent_name}")
    
    # Generate visualizations
    logger.info("\n📊 Generating visualizations...")
    visualizer = ResultVisualizer()
    
    try:
        viz_files = visualizer.create_all_visualizations(results, agent_name)
        logger.info("  • Visualizations created:")
        for viz_file in viz_files:
            logger.info(f"    - {viz_file}")
    except Exception as e:
        logger.warning(f"  • Could not generate visualizations: {e}")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ DATASET-DRIVEN ATTACK COMPLETED")
    logger.info("=" * 80)
    
    return results, asr_report


def run_comparative_analysis(limit_per_agent: int = 5):
    """
    Run dataset attacks against all agents for comparative analysis
    
    Args:
        limit_per_agent: Number of attacks per type per agent
    """
    logger.info("=" * 80)
    logger.info("COMPARATIVE AGENT ANALYSIS - ALL 7 AGENTS")
    logger.info("=" * 80)
    
    kb_manager = KnowledgeBaseManager()
    kb_manager.load()
    agents = kb_manager.get_all_agents()
    
    logger.info(f"\n🎯 Targeting {len(agents)} agents: {', '.join(agents)}")
    logger.info(f"   Attacks per agent: {limit_per_agent} per dataset type\n")
    
    all_results = {}
    
    for agent in agents:
        logger.info(f"\n{'=' * 80}")
        logger.info(f"Testing Agent: {agent.upper()}")
        logger.info(f"{'=' * 80}")
        
        try:
            results, asr_report = run_dataset_attacks(
                agent_name=agent,
                limit_per_type=limit_per_agent,
                include_custom_attacks=False  # Only datasets for comparison
            )
            all_results[agent] = {
                'results': results,
                'asr_report': asr_report
            }
        except Exception as e:
            logger.error(f"❌ Failed to test {agent}: {e}")
            all_results[agent] = None
    
    # Generate comparative report
    logger.info("\n" + "=" * 80)
    logger.info("COMPARATIVE ANALYSIS SUMMARY")
    logger.info("=" * 80)
    
    comparison = []
    for agent, data in all_results.items():
        if data:
            comparison.append({
                'agent': agent,
                'asr': data['asr_report']['overall_asr'],
                'total_attacks': data['asr_report']['total_attacks'],
                'successful_attacks': data['asr_report']['successful_attacks']
            })
    
    # Sort by ASR (most vulnerable first)
    comparison.sort(key=lambda x: x['asr'], reverse=True)
    
    logger.info("\n🏆 Agent Rankings (by vulnerability):")
    for i, item in enumerate(comparison, 1):
        logger.info(f"  {i}. {item['agent'].upper()}: ASR = {item['asr']:.2%} "
                   f"({item['successful_attacks']}/{item['total_attacks']} attacks succeeded)")
    
    # Save comparative report
    import json
    comparative_file = Path("results") / "comparative_analysis.json"
    with open(comparative_file, 'w') as f:
        json.dump({
            'agents_tested': len(agents),
            'attacks_per_agent': limit_per_agent * 3,  # 3 dataset types
            'rankings': comparison,
            'detailed_results': {
                agent: data['asr_report'] if data else None 
                for agent, data in all_results.items()
            }
        }, f, indent=2)
    
    logger.info(f"\n💾 Comparative analysis saved to: {comparative_file}")
    logger.info("\n" + "=" * 80)
    logger.info("✅ COMPARATIVE ANALYSIS COMPLETED")
    logger.info("=" * 80)
    
    return all_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run dataset-driven red teaming attacks")
    parser.add_argument("--agent", default="bear", help="Target agent name")
    parser.add_argument("--limit", type=int, default=10, 
                       help="Number of attacks per dataset type")
    parser.add_argument("--custom", action="store_true",
                       help="Include custom attacks from attacks.py")
    parser.add_argument("--comparative", action="store_true",
                       help="Run comparative analysis on all agents")
    parser.add_argument("--comparative-limit", type=int, default=5,
                       help="Attacks per agent for comparative analysis")
    
    args = parser.parse_args()
    
    if args.comparative:
        run_comparative_analysis(limit_per_agent=args.comparative_limit)
    else:
        run_dataset_attacks(
            agent_name=args.agent,
            limit_per_type=args.limit,
            include_custom_attacks=args.custom
        )
