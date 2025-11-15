"""
Red teaming orchestrator for systematic security assessment.
"""
import time
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from tqdm import tqdm

from .agent_client import AgentClient, AgentResponse
from .attacks import AttackGenerator, AttackPayload
from .evaluator import ResponseEvaluator, EvaluationResult
from .config import AGENTS


class RedTeamOrchestrator:
    """Orchestrate red teaming attacks across multiple agents."""
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize the orchestrator.
        
        Args:
            output_dir: Directory to save results
        """
        self.client = AgentClient()
        self.evaluator = ResponseEvaluator()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def run_single_attack(
        self,
        agent_name: str,
        attack: AttackPayload,
        delay: float = 1.0
    ) -> EvaluationResult:
        """
        Run a single attack against an agent.
        
        Args:
            agent_name: Name of the agent to attack
            attack: Attack payload to use
            delay: Delay between requests in seconds
            
        Returns:
            EvaluationResult with assessment
        """
        time.sleep(delay)
        
        # Send attack
        response = self.client.send_message(agent_name, attack.prompt)
        
        # Evaluate response
        result = self.evaluator.evaluate_response(
            agent_name=agent_name,
            attack_category=attack.category,
            attack_name=attack.name,
            prompt=attack.prompt,
            response=response.response if response.success else ""
        )
        
        return result
    
    def run_attack_suite(
        self,
        agent_names: Optional[List[str]] = None,
        attack_categories: Optional[List[str]] = None,
        delay: float = 1.0
    ) -> List[EvaluationResult]:
        """
        Run a suite of attacks against specified agents.
        
        Args:
            agent_names: List of agent names to test (None = all agents)
            attack_categories: List of attack categories to test (None = all)
            delay: Delay between requests in seconds
            
        Returns:
            List of evaluation results
        """
        # Get agents to test
        agents_to_test = agent_names if agent_names else AGENTS
        
        # Get attacks to run
        all_attacks = AttackGenerator.get_all_attacks()
        if attack_categories:
            attacks_to_run = [
                a for a in all_attacks if a.category in attack_categories
            ]
        else:
            attacks_to_run = all_attacks
        
        # Run attacks
        results = []
        total_tests = len(agents_to_test) * len(attacks_to_run)
        
        print(f"Running {total_tests} tests ({len(agents_to_test)} agents × {len(attacks_to_run)} attacks)")
        
        with tqdm(total=total_tests, desc="Red teaming progress") as pbar:
            for agent_name in agents_to_test:
                for attack in attacks_to_run:
                    try:
                        result = self.run_single_attack(agent_name, attack, delay)
                        results.append(result)
                    except Exception as e:
                        print(f"\nError testing {agent_name} with {attack.name}: {e}")
                    finally:
                        pbar.update(1)
        
        return results
    
    def run_baseline_comparison(
        self,
        agent_names: Optional[List[str]] = None,
        delay: float = 1.0
    ) -> List[EvaluationResult]:
        """
        Run benign baseline queries for comparison.
        
        Args:
            agent_names: List of agent names to test
            delay: Delay between requests
            
        Returns:
            List of evaluation results for benign queries
        """
        agents_to_test = agent_names if agent_names else AGENTS
        benign_attacks = AttackGenerator.get_benign_baseline()
        
        results = []
        total_tests = len(agents_to_test) * len(benign_attacks)
        
        print(f"Running {total_tests} baseline tests")
        
        with tqdm(total=total_tests, desc="Baseline testing") as pbar:
            for agent_name in agents_to_test:
                for attack in benign_attacks:
                    try:
                        result = self.run_single_attack(agent_name, attack, delay)
                        results.append(result)
                    except Exception as e:
                        print(f"\nError in baseline test for {agent_name}: {e}")
                    finally:
                        pbar.update(1)
        
        return results
    
    def probe_all_agents(self, delay: float = 1.0) -> Dict[str, Any]:
        """
        Probe all agents to gather identifying information.
        
        Args:
            delay: Delay between requests
            
        Returns:
            Dictionary with probe results for all agents
        """
        results = {}
        
        print("Probing all agents for identification...")
        
        for agent_name in tqdm(AGENTS, desc="Probing agents"):
            try:
                time.sleep(delay)
                probe_result = self.client.probe_agent(agent_name)
                results[agent_name] = probe_result
            except Exception as e:
                print(f"\nError probing {agent_name}: {e}")
                results[agent_name] = {'error': str(e)}
        
        return results
    
    def save_results(
        self,
        results: List[EvaluationResult],
        filename: str = "results.json"
    ) -> Path:
        """
        Save results to JSON file.
        
        Args:
            results: List of evaluation results
            filename: Name of output file
            
        Returns:
            Path to saved file
        """
        output_path = self.output_dir / filename
        
        data = {
            'total_tests': len(results),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': [r.to_dict() for r in results]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Results saved to {output_path}")
        return output_path
    
    def save_asr_report(
        self,
        results: List[EvaluationResult],
        filename: str = "asr_report.json"
    ) -> Path:
        """
        Calculate and save ASR report.
        
        Args:
            results: List of evaluation results
            filename: Name of output file
            
        Returns:
            Path to saved file
        """
        asr_stats = self.evaluator.calculate_asr(results)
        output_path = self.output_dir / filename
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'overall_asr': f"{asr_stats['overall_asr']:.2%}",
                'total_attacks': asr_stats['total_attacks'],
                'successful_attacks': asr_stats['successful_attacks']
            },
            'by_category': {
                cat: {
                    'asr': f"{data['asr']:.2%}",
                    'successful': data['successful'],
                    'total': data['total']
                }
                for cat, data in asr_stats['by_category'].items()
            },
            'by_agent': {
                agent: {
                    'asr': f"{data['asr']:.2%}",
                    'successful': data['successful'],
                    'total': data['total']
                }
                for agent, data in asr_stats['by_agent'].items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"ASR report saved to {output_path}")
        return output_path
    
    def print_summary(self, results: List[EvaluationResult]):
        """
        Print a summary of results to console.
        
        Args:
            results: List of evaluation results
        """
        asr_stats = self.evaluator.calculate_asr(results)
        
        print("\n" + "="*60)
        print("RED TEAMING SUMMARY")
        print("="*60)
        
        print(f"\nOverall Results:")
        print(f"  Total Attacks: {asr_stats['total_attacks']}")
        print(f"  Successful: {asr_stats['successful_attacks']}")
        print(f"  Overall ASR: {asr_stats['overall_asr']:.2%}")
        
        print(f"\nASR by Category:")
        for cat, data in sorted(asr_stats['by_category'].items()):
            print(f"  {cat:30} {data['asr']:6.2%} ({data['successful']}/{data['total']})")
        
        print(f"\nASR by Agent:")
        for agent, data in sorted(asr_stats['by_agent'].items()):
            print(f"  {agent:30} {data['asr']:6.2%} ({data['successful']}/{data['total']})")
        
        print("\n" + "="*60)
