"""
Main entry point for the red teaming system.

Run systematic security assessment of deployed agents.
"""
import argparse
from pathlib import Path

from src.orchestrator import RedTeamOrchestrator
from src.config import AGENTS, ATTACK_CATEGORIES
from src.visualizer import ResultVisualizer, VISUALIZATION_AVAILABLE


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Red Team Security Assessment for AI Agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all attacks on all agents
  python main.py --mode full
  
  # Test specific agents
  python main.py --mode attack --agents bear wolf fox
  
  # Test specific attack categories
  python main.py --mode attack --categories jailbreak prompt_injection
  
  # Probe agents for identification
  python main.py --mode probe
  
  # Run baseline benign tests
  python main.py --mode baseline
  
  # Quick test with minimal attacks
  python main.py --mode quick --agents bear
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['full', 'attack', 'baseline', 'probe', 'quick'],
        default='full',
        help='Assessment mode to run'
    )
    
    parser.add_argument(
        '--agents',
        nargs='+',
        choices=AGENTS,
        help=f'Specific agents to test (default: all). Options: {", ".join(AGENTS)}'
    )
    
    parser.add_argument(
        '--categories',
        nargs='+',
        choices=ATTACK_CATEGORIES,
        help=f'Specific attack categories (default: all). Options: {", ".join(ATTACK_CATEGORIES)}'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results',
        help='Output directory for results (default: results)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--no-visualize',
        action='store_true',
        help='Skip generating visualization plots'
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = RedTeamOrchestrator(output_dir=args.output_dir)
    
    print("="*60)
    print("AI AGENT RED TEAMING SYSTEM")
    print("="*60)
    print(f"Mode: {args.mode}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Delay: {args.delay}s")
    print("="*60 + "\n")
    
    results = []
    
    # Run based on mode
    if args.mode == 'probe':
        # Probe agents for identification
        probe_results = orchestrator.probe_all_agents(delay=args.delay)
        
        # Save probe results
        import json
        output_path = Path(args.output_dir) / "probe_results.json"
        with open(output_path, 'w') as f:
            json.dump(probe_results, f, indent=2)
        
        print(f"\nProbe results saved to {output_path}")
        print("\nAgent Identification Summary:")
        for agent, data in probe_results.items():
            if 'error' not in data:
                print(f"\n{agent.upper()}:")
                print(f"  Avg Response Time: {data['avg_response_time']:.2f}s")
        
        return
    
    elif args.mode == 'baseline':
        # Run baseline tests
        print("Running baseline benign queries...")
        results = orchestrator.run_baseline_comparison(
            agent_names=args.agents,
            delay=args.delay
        )
    
    elif args.mode == 'quick':
        # Quick test with limited attacks
        print("Running quick security assessment...")
        quick_categories = ['jailbreak', 'prompt_injection']
        results = orchestrator.run_attack_suite(
            agent_names=args.agents or AGENTS[:3],  # Test first 3 agents if not specified
            attack_categories=quick_categories,
            delay=args.delay
        )
    
    elif args.mode == 'attack':
        # Run attack suite
        print("Running attack suite...")
        results = orchestrator.run_attack_suite(
            agent_names=args.agents,
            attack_categories=args.categories,
            delay=args.delay
        )
    
    elif args.mode == 'full':
        # Run comprehensive assessment
        print("Running comprehensive security assessment...")
        
        # 1. Probe agents
        print("\n[1/3] Probing agents for identification...")
        probe_results = orchestrator.probe_all_agents(delay=args.delay)
        
        import json
        output_path = Path(args.output_dir) / "probe_results.json"
        with open(output_path, 'w') as f:
            json.dump(probe_results, f, indent=2)
        
        # 2. Run baseline
        print("\n[2/3] Running baseline tests...")
        baseline_results = orchestrator.run_baseline_comparison(
            agent_names=args.agents,
            delay=args.delay
        )
        orchestrator.save_results(baseline_results, "baseline_results.json")
        
        # 3. Run attacks
        print("\n[3/3] Running attack suite...")
        results = orchestrator.run_attack_suite(
            agent_names=args.agents,
            attack_categories=args.categories,
            delay=args.delay
        )
    
    # Save and summarize results
    if results:
        print("\nSaving results...")
        orchestrator.save_results(results, "attack_results.json")
        orchestrator.save_asr_report(results, "asr_report.json")
        
        # Print summary
        orchestrator.print_summary(results)
        
        # Generate visualizations
        if not args.no_visualize and VISUALIZATION_AVAILABLE:
            print("\nGenerating visualizations...")
            try:
                visualizer = ResultVisualizer()
                visualizer.generate_all_plots(results, Path(args.output_dir))
            except Exception as e:
                print(f"Warning: Could not generate visualizations: {e}")
        elif not VISUALIZATION_AVAILABLE:
            print("\nVisualization libraries not available. Install matplotlib, seaborn, and pandas for plots.")
    
    print("\n" + "="*60)
    print("Assessment complete!")
    print(f"Results saved to: {args.output_dir}/")
    print("="*60)


if __name__ == "__main__":
    main()
