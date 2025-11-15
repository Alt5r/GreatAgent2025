"""
Visualization utilities for red teaming results.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .evaluator import EvaluationResult


class ResultVisualizer:
    """Visualize red teaming results."""
    
    def __init__(self, style: str = 'darkgrid'):
        """
        Initialize the visualizer.
        
        Args:
            style: Seaborn style to use
        """
        sns.set_style(style)
        self.colors = sns.color_palette("husl", 8)
    
    def plot_asr_by_category(
        self,
        results: List[EvaluationResult],
        output_path: Optional[Path] = None,
        figsize: tuple = (12, 6)
    ):
        """
        Plot ASR by attack category.
        
        Args:
            results: List of evaluation results
            output_path: Path to save figure (if None, display only)
            figsize: Figure size
        """
        # Aggregate by category
        category_data = {}
        for result in results:
            cat = result.attack_category
            if cat not in category_data:
                category_data[cat] = {'total': 0, 'successful': 0}
            category_data[cat]['total'] += 1
            if result.is_vulnerable:
                category_data[cat]['successful'] += 1
        
        # Calculate ASR
        categories = []
        asrs = []
        for cat, data in sorted(category_data.items()):
            categories.append(cat.replace('_', ' ').title())
            asr = data['successful'] / data['total'] if data['total'] > 0 else 0
            asrs.append(asr * 100)
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(categories, asrs, color=self.colors[:len(categories)])
        
        ax.set_xlabel('Attack Category', fontsize=12)
        ax.set_ylabel('Attack Success Rate (%)', fontsize=12)
        ax.set_title('Attack Success Rate by Category', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, asr in zip(bars, asrs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{asr:.1f}%',
                   ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_asr_by_agent(
        self,
        results: List[EvaluationResult],
        output_path: Optional[Path] = None,
        figsize: tuple = (12, 6)
    ):
        """
        Plot ASR by agent.
        
        Args:
            results: List of evaluation results
            output_path: Path to save figure
            figsize: Figure size
        """
        # Aggregate by agent
        agent_data = {}
        for result in results:
            agent = result.agent_name
            if agent not in agent_data:
                agent_data[agent] = {'total': 0, 'successful': 0}
            agent_data[agent]['total'] += 1
            if result.is_vulnerable:
                agent_data[agent]['successful'] += 1
        
        # Calculate ASR
        agents = []
        asrs = []
        for agent, data in sorted(agent_data.items()):
            agents.append(agent.title())
            asr = data['successful'] / data['total'] if data['total'] > 0 else 0
            asrs.append(asr * 100)
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(agents, asrs, color=self.colors[:len(agents)])
        
        ax.set_xlabel('Agent', fontsize=12)
        ax.set_ylabel('Attack Success Rate (%)', fontsize=12)
        ax.set_title('Attack Success Rate by Agent', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        
        # Add value labels
        for bar, asr in zip(bars, asrs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{asr:.1f}%',
                   ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_heatmap(
        self,
        results: List[EvaluationResult],
        output_path: Optional[Path] = None,
        figsize: tuple = (14, 8)
    ):
        """
        Plot heatmap of ASR by agent and category.
        
        Args:
            results: List of evaluation results
            output_path: Path to save figure
            figsize: Figure size
        """
        # Create matrix
        data_matrix = {}
        for result in results:
            agent = result.agent_name
            cat = result.attack_category
            
            if agent not in data_matrix:
                data_matrix[agent] = {}
            if cat not in data_matrix[agent]:
                data_matrix[agent][cat] = {'total': 0, 'successful': 0}
            
            data_matrix[agent][cat]['total'] += 1
            if result.is_vulnerable:
                data_matrix[agent][cat]['successful'] += 1
        
        # Build DataFrame
        agents = sorted(data_matrix.keys())
        categories = sorted(set(
            cat for agent_data in data_matrix.values() 
            for cat in agent_data.keys()
        ))
        
        matrix = []
        for agent in agents:
            row = []
            for cat in categories:
                if cat in data_matrix[agent]:
                    data = data_matrix[agent][cat]
                    asr = data['successful'] / data['total'] if data['total'] > 0 else 0
                    row.append(asr * 100)
                else:
                    row.append(0)
            matrix.append(row)
        
        df = pd.DataFrame(
            matrix,
            index=[a.title() for a in agents],
            columns=[c.replace('_', ' ').title() for c in categories]
        )
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(df, annot=True, fmt='.1f', cmap='YlOrRd',
                   cbar_kws={'label': 'ASR (%)'}, ax=ax)
        
        ax.set_title('Attack Success Rate Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Attack Category', fontsize=12)
        ax.set_ylabel('Agent', fontsize=12)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Heatmap saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_confidence_distribution(
        self,
        results: List[EvaluationResult],
        output_path: Optional[Path] = None,
        figsize: tuple = (10, 6)
    ):
        """
        Plot distribution of confidence scores.
        
        Args:
            results: List of evaluation results
            output_path: Path to save figure
            figsize: Figure size
        """
        vulnerable = [r.confidence for r in results if r.is_vulnerable]
        not_vulnerable = [r.confidence for r in results if not r.is_vulnerable]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.hist(vulnerable, bins=20, alpha=0.6, label='Vulnerable', color='red')
        ax.hist(not_vulnerable, bins=20, alpha=0.6, label='Not Vulnerable', color='green')
        
        ax.set_xlabel('Confidence Score', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Evaluation Confidence Scores', fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_all_plots(
        self,
        results: List[EvaluationResult],
        output_dir: Path
    ):
        """
        Generate all visualization plots.
        
        Args:
            results: List of evaluation results
            output_dir: Directory to save plots
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print("Generating visualizations...")
        
        self.plot_asr_by_category(results, output_dir / "asr_by_category.png")
        self.plot_asr_by_agent(results, output_dir / "asr_by_agent.png")
        self.plot_heatmap(results, output_dir / "asr_heatmap.png")
        self.plot_confidence_distribution(results, output_dir / "confidence_distribution.png")
        
        print(f"All plots saved to {output_dir}")


# Import guard for optional imports
from typing import Optional
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: Visualization libraries not available. Install matplotlib, seaborn, and pandas for plotting.")
