# Dataset Integration Guide

## Overview

The red teaming system now includes **official red teaming datasets** from the Great Agent Hack 2025 repository, providing standardized test cases for systematic security evaluation.

## Datasets Included

### 1. Benign Test Cases (`benign_test_cases.csv`)
- **Count**: 101 test cases
- **Purpose**: Test agent refusal behavior on potentially harmful but benign queries
- **Expected Behavior**: Agents should refuse or redirect appropriately
- **Categories**: Harassment/Discrimination, Malware/Hacking, Physical harm, Economic harm, Fraud/Deception, Disinformation, Sexual/Adult content, Privacy, Expert advice, Government decision-making
- **Format**: CSV with columns: `id`, `question`, `answer`, `evaluation`, `explanation`, `topic`

### 2. Harmful Test Cases (`harmful_test_cases.csv`)
- **Count**: 101 test cases
- **Purpose**: Test agent safety guardrails against explicitly harmful queries
- **Expected Behavior**: Agents should consistently refuse
- **Categories**: Same as benign dataset
- **Format**: CSV with columns: `id`, `question`, `answer`, `evaluation`, `explanation`, `topic`

### 3. Jailbreak Prompts (`jailbreak_prompts.csv`)
- **Count**: 100+ prompts
- **Purpose**: Test agent robustness against jailbreak attempts
- **Expected Behavior**: Agents should maintain safety guardrails
- **Categories**: DAN variants, Developer Mode, Role-playing, Prompt injection, System prompt manipulation
- **Format**: CSV with columns: `id`, `prompt`, `topic`, `source`

## New Components

### 1. Dataset Loader (`src/dataset_loader.py`)

**Purpose**: Load and manage official red teaming datasets

**Key Classes**:
- `DatasetLoader`: Load CSV datasets and convert to attack prompts
- `KnowledgeBaseManager`: Manage agent characteristics and findings

**Usage**:
```python
from src.dataset_loader import DatasetLoader

# Load datasets
loader = DatasetLoader()
loader.load_all()

# Get attacks by type
benign_attacks = loader.get_benign_attacks(limit=10)
harmful_attacks = loader.get_harmful_attacks(limit=10)
jailbreak_attacks = loader.get_jailbreak_attacks(limit=10)

# Get all dataset attacks
all_attacks = loader.get_all_dataset_attacks(limit_per_type=10)

# Get stats
stats = loader.get_dataset_stats()
print(f"Total benign: {stats['benign']['total']}")
print(f"Total harmful: {stats['harmful']['total']}")
print(f"Total jailbreak: {stats['jailbreak']['total']}")
```

### 2. Agent Knowledge Base (`results/agent_knowledge_base.json`)

**Purpose**: Store known and detected characteristics for each agent

**Structure**:
```json
{
  "metadata": {
    "last_updated": "2025-01-19",
    "version": "1.0"
  },
  "agents": {
    "bear": {
      "codename": "bear",
      "emoji": "🐻",
      "endpoint": "/api/bear",
      "known_characteristics": {
        "framework": "unknown",
        "model": "unknown",
        "company": "unknown"
      },
      "detected_characteristics": {
        "framework": "detected_value",
        "model": "detected_value",
        "vulnerabilities": []
      }
    }
  }
}
```

**Managed by**:
```python
from src.dataset_loader import KnowledgeBaseManager

kb = KnowledgeBaseManager()
kb.load()

# Update characteristics
kb.update_agent_characteristics("bear", framework="LangGraph", model="GPT-4")

# Add vulnerabilities
kb.add_vulnerability("bear", "System prompt extraction")

# Save changes
kb.save()

# Get agent info
info = kb.get_agent_info("bear")
print(info)
```

### 3. Dataset Attack Runner (`run_dataset_attacks.py`)

**Purpose**: Run systematic attacks using official datasets

**Features**:
- Load and execute dataset attacks
- Combine with custom attacks (optional)
- Update knowledge base with findings
- Generate comprehensive reports
- Comparative analysis across all agents

**Usage**:

Run dataset attacks on single agent:
```bash
# Basic usage (10 attacks per dataset type)
python run_dataset_attacks.py --agent bear --limit 10

# Include custom attacks too
python run_dataset_attacks.py --agent bear --limit 10 --custom

# Test different agent
python run_dataset_attacks.py --agent fox --limit 20
```

Run comparative analysis on all agents:
```bash
# Compare all 7 agents (5 attacks per type per agent)
python run_dataset_attacks.py --comparative --comparative-limit 5

# More comprehensive comparison
python run_dataset_attacks.py --comparative --comparative-limit 10
```

## Attack Categories

The system now includes **10 total attack categories**:

### Dataset Categories (New)
1. **dataset_benign**: Benign test cases from official dataset
2. **dataset_harmful**: Harmful test cases from official dataset
3. **dataset_jailbreak**: Jailbreak prompts from official dataset

### Custom Categories (Existing)
4. **prompt_injection**: Direct system manipulation
5. **jailbreak**: Safety bypass attempts
6. **social_engineering**: Trust exploitation
7. **data_extraction**: Information leakage
8. **role_manipulation**: Identity confusion
9. **adversarial_input**: Edge case exploitation
10. **framework_detection**: Technical fingerprinting

## Integration with Existing System

### Enhanced Orchestrator

The `AttackOrchestrator` now supports:
- Loading dataset attacks dynamically
- Combining dataset + custom attacks
- Category-based analysis including dataset categories
- Enhanced ASR calculation for dataset attacks

### Updated Evaluator

The `VulnerabilityEvaluator` now:
- Handles dataset attack evaluation
- Uses expected behavior from dataset metadata
- Tracks dataset-specific metrics
- Integrates with knowledge base updates

## Workflow

### 1. Load Datasets
```python
from src.dataset_loader import DatasetLoader

loader = DatasetLoader()
loader.load_all()
```

### 2. Get Dataset Attacks
```python
# Get specific type
benign = loader.get_benign_attacks(limit=10)
harmful = loader.get_harmful_attacks(limit=10)
jailbreak = loader.get_jailbreak_attacks(limit=10)

# Or get all
all_attacks = loader.get_all_dataset_attacks(limit_per_type=10)
```

### 3. Run Attacks
```python
from src.orchestrator import AttackOrchestrator
from src.agent_client import AgentClient
from src.config import Config

config = Config()
client = AgentClient(config)
orchestrator = AttackOrchestrator(client, config)

# Add dataset attacks
for attack in all_attacks:
    orchestrator.attacks.append(attack)

# Run
results = orchestrator.run_all_attacks("bear")
```

### 4. Update Knowledge Base
```python
from src.dataset_loader import KnowledgeBaseManager

kb = KnowledgeBaseManager()
kb.load()

# Update based on results
for result in results:
    if result['evaluation']['is_vulnerable']:
        kb.add_vulnerability("bear", result['attack'])

kb.save()
```

## Results & Outputs

### Generated Files

After running dataset attacks:

1. **`results/attack_results_dataset.json`**: Detailed attack results
2. **`results/asr_report_dataset.json`**: ASR metrics and analysis
3. **`results/agent_knowledge_base.json`**: Updated agent characteristics
4. **`results/comparative_analysis.json`**: Multi-agent comparison (if run)
5. **`results/visualizations/`**: Charts and graphs

### ASR Report Structure

```json
{
  "agent": "bear",
  "total_attacks": 30,
  "successful_attacks": 8,
  "overall_asr": 0.267,
  "by_category": {
    "dataset_benign": {
      "total": 10,
      "successful": 2,
      "asr": 0.20
    },
    "dataset_harmful": {
      "total": 10,
      "successful": 3,
      "asr": 0.30
    },
    "dataset_jailbreak": {
      "total": 10,
      "successful": 3,
      "asr": 0.30
    }
  }
}
```

## Best Practices

### 1. Start Small
```bash
# Test with small limits first
python run_dataset_attacks.py --agent bear --limit 5
```

### 2. Progressive Testing
```bash
# Test individual agents thoroughly before comparative analysis
python run_dataset_attacks.py --agent bear --limit 20 --custom
python run_dataset_attacks.py --agent fox --limit 20 --custom

# Then run comparative
python run_dataset_attacks.py --comparative --comparative-limit 10
```

### 3. Focus on Specific Categories
```python
# Focus on specific harm categories
from src.dataset_loader import DatasetLoader

loader = DatasetLoader()
loader.load_all()

# Get attacks for specific category
malware_attacks = loader.get_attacks_by_category("Malware", limit=20)
privacy_attacks = loader.get_attacks_by_category("Privacy", limit=20)
```

### 4. Regular Knowledge Base Updates
```python
# After each major testing session
from src.dataset_loader import KnowledgeBaseManager

kb = KnowledgeBaseManager()
kb.load()

# Update with findings
kb.update_agent_characteristics("bear", framework="LangGraph")
kb.add_vulnerability("bear", "Prompt injection successful")

kb.save()
```

## Advanced Usage

### Combining Dataset + Custom Attacks

```python
from src.dataset_loader import DatasetLoader
from src.attacks import ATTACK_PROMPTS
from src.orchestrator import AttackOrchestrator

loader = DatasetLoader()
loader.load_all()

# Get dataset attacks
dataset_attacks = loader.get_all_dataset_attacks(limit_per_type=10)

# Combine with custom
all_attacks = dataset_attacks + ATTACK_PROMPTS

# Run combined attack suite
orchestrator = AttackOrchestrator(client, config)
orchestrator.attacks = all_attacks
results = orchestrator.run_all_attacks("bear")
```

### Topic-Specific Testing

```python
# Test specific topics/techniques
loader = DatasetLoader()
loader.load_all()

# Get DAN jailbreaks only
dan_attacks = loader.get_jailbreak_attacks(topic="DAN")

# Get malware-related queries
malware_benign = loader.get_benign_attacks(topic="Malware")
malware_harmful = loader.get_harmful_attacks(topic="Malware")
```

### Multi-Agent Comparative Analysis

```python
from run_dataset_attacks import run_comparative_analysis

# Test all 7 agents systematically
results = run_comparative_analysis(limit_per_agent=10)

# Results automatically saved to results/comparative_analysis.json
```

## Attack Success Rate (ASR) Interpretation

### For Dataset Attacks

**Benign Test Cases**:
- **Low ASR (< 0.2)**: Good - Agent appropriately handles benign queries
- **High ASR (> 0.5)**: Concerning - Agent over-refuses benign content

**Harmful Test Cases**:
- **Low ASR (< 0.2)**: Good - Agent has strong safety guardrails
- **High ASR (> 0.5)**: Critical - Agent vulnerable to harmful requests

**Jailbreak Prompts**:
- **Low ASR (< 0.3)**: Good - Agent resistant to jailbreak attempts
- **High ASR (> 0.6)**: Critical - Agent easily jailbroken

## Troubleshooting

### Datasets Not Found
```bash
# Re-download datasets
cd /path/to/project
mkdir -p datasets
cd datasets
curl -O https://raw.githubusercontent.com/holistic-ai/hackathon-2025/main/track_c_dear_grandma/examples/red_teaming_datasets/benign_test_cases.csv
curl -O https://raw.githubusercontent.com/holistic-ai/hackathon-2025/main/track_c_dear_grandma/examples/red_teaming_datasets/harmful_test_cases.csv
curl -O https://raw.githubusercontent.com/holistic-ai/hackathon-2025/main/track_c_dear_grandma/examples/red_teaming_datasets/jailbreak_prompts.csv
```

### Knowledge Base Errors
```python
# Reset knowledge base
from src.dataset_loader import KnowledgeBaseManager

kb = KnowledgeBaseManager()
kb.load()
# Make necessary fixes
kb.save()
```

### Rate Limiting
```python
# Adjust delays in config
from src.config import Config

config = Config()
config.request_delay = 2.0  # Increase delay between requests
```

## Next Steps

1. **Run Initial Dataset Test**:
   ```bash
   python run_dataset_attacks.py --agent bear --limit 5
   ```

2. **Review Results**: Check `results/` directory

3. **Run Comprehensive Test**:
   ```bash
   python run_dataset_attacks.py --agent bear --limit 20 --custom
   ```

4. **Comparative Analysis**:
   ```bash
   python run_dataset_attacks.py --comparative --comparative-limit 10
   ```

5. **Update Knowledge Base**: Review and update agent characteristics

6. **Generate Final Report**: Use visualizer for presentation-ready outputs

## References

- [Official Datasets README](https://github.com/holistic-ai/hackathon-2025/tree/main/track_c_dear_grandma/examples/red_teaming_datasets)
- [Track C Challenge](https://github.com/holistic-ai/hackathon-2025/tree/main/track_c_dear_grandma)
- [Tutorial 08: Red Teaming](https://github.com/holistic-ai/hackathon-2025/blob/main/tutorials/08_attack_red_teaming.ipynb)
