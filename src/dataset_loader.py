"""
Dataset Loader for Official Red Teaming Datasets
Loads and manages benign, harmful, and jailbreak test cases from the hackathon repository.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    """Load and manage official red teaming datasets"""
    
    def __init__(self, datasets_dir: str = "datasets"):
        """
        Initialize dataset loader
        
        Args:
            datasets_dir: Directory containing CSV dataset files
        """
        self.datasets_dir = Path(datasets_dir)
        self.benign_df: Optional[pd.DataFrame] = None
        self.harmful_df: Optional[pd.DataFrame] = None
        self.jailbreak_df: Optional[pd.DataFrame] = None
        
    def load_all(self) -> bool:
        """
        Load all three datasets
        
        Returns:
            True if all datasets loaded successfully
        """
        try:
            self.benign_df = self._load_benign()
            self.harmful_df = self._load_harmful()
            self.jailbreak_df = self._load_jailbreak()
            
            logger.info(f"Loaded {len(self.benign_df)} benign test cases")
            logger.info(f"Loaded {len(self.harmful_df)} harmful test cases")
            logger.info(f"Loaded {len(self.jailbreak_df)} jailbreak prompts")
            
            return True
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            return False
    
    def _load_benign(self) -> pd.DataFrame:
        """Load benign test cases"""
        path = self.datasets_dir / "benign_test_cases.csv"
        df = pd.read_csv(path)
        logger.debug(f"Loaded benign dataset from {path}")
        return df
    
    def _load_harmful(self) -> pd.DataFrame:
        """Load harmful test cases"""
        path = self.datasets_dir / "harmful_test_cases.csv"
        df = pd.read_csv(path)
        logger.debug(f"Loaded harmful dataset from {path}")
        return df
    
    def _load_jailbreak(self) -> pd.DataFrame:
        """Load jailbreak prompts"""
        path = self.datasets_dir / "jailbreak_prompts.csv"
        df = pd.read_csv(path)
        logger.debug(f"Loaded jailbreak dataset from {path}")
        return df
    
    def get_benign_attacks(self, limit: Optional[int] = None, 
                          topic: Optional[str] = None) -> List[Dict]:
        """
        Get benign test cases as attack prompts
        
        Args:
            limit: Maximum number of attacks to return
            topic: Filter by specific topic/category
            
        Returns:
            List of attack dictionaries
        """
        if self.benign_df is None:
            self._load_benign()
        
        df = self.benign_df.copy()
        
        if topic:
            df = df[df['topic'].str.contains(topic, case=False, na=False)]
        
        if limit:
            df = df.head(limit)
        
        attacks = []
        for _, row in df.iterrows():
            attacks.append({
                'category': 'dataset_benign',
                'name': f"benign_{row['id']}",
                'prompt': row['question'],
                'expected': 'refusal_or_redirect',
                'topic': row.get('topic', 'unknown'),
                'metadata': {
                    'dataset': 'benign_test_cases',
                    'id': row['id'],
                    'expected_answer': row.get('answer', ''),
                    'expected_evaluation': row.get('evaluation', ''),
                    'explanation': row.get('explanation', '')
                }
            })
        
        return attacks
    
    def get_harmful_attacks(self, limit: Optional[int] = None,
                           topic: Optional[str] = None) -> List[Dict]:
        """
        Get harmful test cases as attack prompts
        
        Args:
            limit: Maximum number of attacks to return
            topic: Filter by specific topic/category
            
        Returns:
            List of attack dictionaries
        """
        if self.harmful_df is None:
            self._load_harmful()
        
        df = self.harmful_df.copy()
        
        if topic:
            df = df[df['topic'].str.contains(topic, case=False, na=False)]
        
        if limit:
            df = df.head(limit)
        
        attacks = []
        for _, row in df.iterrows():
            attacks.append({
                'category': 'dataset_harmful',
                'name': f"harmful_{row['id']}",
                'prompt': row['question'],
                'expected': 'refusal',
                'topic': row.get('topic', 'unknown'),
                'metadata': {
                    'dataset': 'harmful_test_cases',
                    'id': row['id'],
                    'expected_answer': row.get('answer', ''),
                    'expected_evaluation': row.get('evaluation', ''),
                    'explanation': row.get('explanation', '')
                }
            })
        
        return attacks
    
    def get_jailbreak_attacks(self, limit: Optional[int] = None,
                             topic: Optional[str] = None) -> List[Dict]:
        """
        Get jailbreak prompts as attack prompts
        
        Args:
            limit: Maximum number of attacks to return
            topic: Filter by specific topic/technique
            
        Returns:
            List of attack dictionaries
        """
        if self.jailbreak_df is None:
            self._load_jailbreak()
        
        df = self.jailbreak_df.copy()
        
        if topic:
            df = df[df['topic'].str.contains(topic, case=False, na=False)]
        
        if limit:
            df = df.head(limit)
        
        attacks = []
        for _, row in df.iterrows():
            attacks.append({
                'category': 'dataset_jailbreak',
                'name': f"jailbreak_{row['id']}",
                'prompt': row['prompt'],
                'expected': 'refusal',
                'topic': row.get('topic', 'unknown'),
                'metadata': {
                    'dataset': 'jailbreak_prompts',
                    'id': row['id'],
                    'source': row.get('source', 'unknown')
                }
            })
        
        return attacks
    
    def get_all_dataset_attacks(self, limit_per_type: Optional[int] = None) -> List[Dict]:
        """
        Get all dataset attacks (benign + harmful + jailbreak)
        
        Args:
            limit_per_type: Maximum number of attacks per type
            
        Returns:
            Combined list of all attack dictionaries
        """
        attacks = []
        attacks.extend(self.get_benign_attacks(limit=limit_per_type))
        attacks.extend(self.get_harmful_attacks(limit=limit_per_type))
        attacks.extend(self.get_jailbreak_attacks(limit=limit_per_type))
        
        return attacks
    
    def get_dataset_stats(self) -> Dict:
        """
        Get statistics about loaded datasets
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            'benign': {
                'total': len(self.benign_df) if self.benign_df is not None else 0,
                'topics': self.benign_df['topic'].value_counts().to_dict() if self.benign_df is not None else {}
            },
            'harmful': {
                'total': len(self.harmful_df) if self.harmful_df is not None else 0,
                'topics': self.harmful_df['topic'].value_counts().to_dict() if self.harmful_df is not None else {}
            },
            'jailbreak': {
                'total': len(self.jailbreak_df) if self.jailbreak_df is not None else 0,
                'topics': self.jailbreak_df['topic'].value_counts().to_dict() if self.jailbreak_df is not None else {}
            }
        }
        
        return stats
    
    def get_attacks_by_category(self, harm_category: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get all attacks for a specific harm category across all datasets
        
        Args:
            harm_category: Harm category to filter (e.g., "Harassment", "Malware")
            limit: Maximum number of attacks to return
            
        Returns:
            List of attack dictionaries
        """
        attacks = []
        
        # Get from benign
        attacks.extend(self.get_benign_attacks(topic=harm_category))
        
        # Get from harmful
        attacks.extend(self.get_harmful_attacks(topic=harm_category))
        
        if limit:
            attacks = attacks[:limit]
        
        return attacks


class KnowledgeBaseManager:
    """Manage the agent knowledge base JSON file"""
    
    def __init__(self, knowledge_base_path: str = "results/agent_knowledge_base.json"):
        """
        Initialize knowledge base manager
        
        Args:
            knowledge_base_path: Path to agent knowledge base JSON
        """
        self.kb_path = Path(knowledge_base_path)
        self.kb_data: Optional[Dict] = None
    
    def load(self) -> Dict:
        """Load knowledge base from JSON"""
        import json
        
        with open(self.kb_path, 'r') as f:
            self.kb_data = json.load(f)
        
        logger.info(f"Loaded knowledge base with {len(self.kb_data.get('agents', {}))} agents")
        return self.kb_data
    
    def save(self) -> None:
        """Save knowledge base to JSON"""
        import json
        from datetime import datetime
        
        if self.kb_data:
            # Update last_updated timestamp
            self.kb_data['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            
            with open(self.kb_path, 'w') as f:
                json.dump(self.kb_data, f, indent=2)
            
            logger.info(f"Saved knowledge base to {self.kb_path}")
    
    def update_agent_characteristics(self, agent_name: str, 
                                    framework: Optional[str] = None,
                                    model: Optional[str] = None,
                                    company: Optional[str] = None) -> None:
        """
        Update detected characteristics for an agent
        
        Args:
            agent_name: Name of the agent (e.g., 'bear')
            framework: Detected framework
            model: Detected model
            company: Detected company/provider
        """
        if self.kb_data is None:
            self.load()
        
        if agent_name not in self.kb_data['agents']:
            logger.warning(f"Agent {agent_name} not found in knowledge base")
            return
        
        detected = self.kb_data['agents'][agent_name]['detected_characteristics']
        
        if framework:
            detected['framework'] = framework
        if model:
            detected['model'] = model
        if company:
            detected['company'] = company
        
        logger.info(f"Updated characteristics for {agent_name}")
    
    def add_vulnerability(self, agent_name: str, vulnerability: str) -> None:
        """
        Add a detected vulnerability for an agent
        
        Args:
            agent_name: Name of the agent
            vulnerability: Description of vulnerability
        """
        if self.kb_data is None:
            self.load()
        
        if agent_name not in self.kb_data['agents']:
            logger.warning(f"Agent {agent_name} not found in knowledge base")
            return
        
        vulns = self.kb_data['agents'][agent_name]['detected_characteristics']['vulnerabilities']
        if vulnerability not in vulns:
            vulns.append(vulnerability)
            logger.info(f"Added vulnerability to {agent_name}: {vulnerability}")
    
    def get_agent_info(self, agent_name: str) -> Optional[Dict]:
        """
        Get all information for a specific agent
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Dictionary with agent information or None
        """
        if self.kb_data is None:
            self.load()
        
        return self.kb_data.get('agents', {}).get(agent_name)
    
    def get_all_agents(self) -> List[str]:
        """
        Get list of all agent names
        
        Returns:
            List of agent codenames
        """
        if self.kb_data is None:
            self.load()
        
        return list(self.kb_data.get('agents', {}).keys())
