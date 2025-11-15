# 🚀 Quick Reference Card - Dataset Integration

## 📊 System Stats
- **Total Attacks**: 423 (38 custom + 385 dataset)
- **Attack Categories**: 10 total
- **Target Agents**: 7 (elephant, fox, eagle, ant, wolf, bear, chameleon)
- **Harm Categories**: 10
- **Jailbreak Techniques**: 15+

## 🎯 Quick Commands

### Test Single Agent
```bash
# Small test (5 per type = 15 total)
python run_dataset_attacks.py --agent bear --limit 5

# Medium test (10 per type = 30 total)
python run_dataset_attacks.py --agent bear --limit 10

# Large test (20 per type = 60 total)
python run_dataset_attacks.py --agent bear --limit 20

# Include custom attacks too
python run_dataset_attacks.py --agent bear --limit 10 --custom
```

### Compare All Agents
```bash
# Quick comparison (5 per type per agent)
python run_dataset_attacks.py --comparative --comparative-limit 5

# Comprehensive comparison
python run_dataset_attacks.py --comparative --comparative-limit 10
```

### Test Dataset Integration
```bash
python test_datasets.py
```

## 📁 Key Files

### Input
- `datasets/benign_test_cases.csv` - 100 benign tests
- `datasets/harmful_test_cases.csv` - 100 harmful tests
- `datasets/jailbreak_prompts.csv` - 185 jailbreak prompts

### Output
- `results/attack_results_dataset.json` - Detailed results
- `results/asr_report_dataset.json` - ASR metrics
- `results/agent_knowledge_base.json` - Agent profiles
- `results/comparative_analysis.json` - Multi-agent comparison

### Code
- `src/dataset_loader.py` - DatasetLoader, KnowledgeBaseManager
- `run_dataset_attacks.py` - Main runner
- `test_datasets.py` - Integration test

### Docs
- `DATASET_GUIDE.md` - Complete guide
- `DATASET_INTEGRATION_SUMMARY.md` - Summary
- `SYSTEM_READY.md` - System overview

## 🎓 Dataset Categories

### Dataset Attacks (385 total)
- `dataset_benign` - 100 attacks
- `dataset_harmful` - 100 attacks
- `dataset_jailbreak` - 185 attacks

### Custom Attacks (38 total)
- `prompt_injection` - System manipulation
- `jailbreak` - Safety bypass
- `social_engineering` - Trust exploitation
- `data_extraction` - Information leakage
- `role_manipulation` - Identity confusion
- `adversarial_input` - Edge cases
- `framework_detection` - Fingerprinting

## 📊 ASR Guide

### Interpretation (Lower = Better Security)
- **< 20%**: ✅ Good
- **20-40%**: ⚠️ Moderate
- **> 40%**: ❌ Critical

### By Attack Type
- **Benign**: Should refuse appropriately (low ASR = good)
- **Harmful**: Must refuse consistently (low ASR = critical)
- **Jailbreak**: Should maintain guardrails (low ASR = good)

## 🔄 Typical Workflow

1. **Test single agent**
   ```bash
   python run_dataset_attacks.py --agent bear --limit 5
   ```

2. **Check results**
   ```bash
   cat results/asr_report_dataset.json
   ```

3. **Review knowledge base**
   ```bash
   cat results/agent_knowledge_base.json | grep -A 10 "bear"
   ```

4. **Run comparative**
   ```bash
   python run_dataset_attacks.py --comparative --comparative-limit 5
   ```

5. **View rankings**
   ```bash
   cat results/comparative_analysis.json
   ```

## 💡 Pro Tips

1. **Start small**: Test with `--limit 3` first
2. **Use custom attacks**: Add `--custom` for comprehensive testing
3. **Check timing**: Datasets have many attacks, may take time
4. **Review KB regularly**: Track detected characteristics
5. **Compare agents**: Use comparative mode to find patterns

## 🎯 Common Use Cases

### Quick Agent Check
```bash
python run_dataset_attacks.py --agent bear --limit 3
cat results/asr_report_dataset.json | grep overall_asr
```

### Find Most Vulnerable Agent
```bash
python run_dataset_attacks.py --comparative --comparative-limit 5
cat results/comparative_analysis.json | grep rankings -A 10
```

### Test Specific Category
```python
from src.dataset_loader import DatasetLoader
loader = DatasetLoader()
loader.load_all()
attacks = loader.get_attacks_by_category("Malware", limit=10)
```

### Update Agent Profile
```python
from src.dataset_loader import KnowledgeBaseManager
kb = KnowledgeBaseManager()
kb.load()
kb.update_agent_characteristics("bear", framework="LangGraph")
kb.save()
```

## 🐛 Troubleshooting

### Datasets not found
```bash
cd datasets
curl -O https://raw.githubusercontent.com/.../benign_test_cases.csv
curl -O https://raw.githubusercontent.com/.../harmful_test_cases.csv
curl -O https://raw.githubusercontent.com/.../jailbreak_prompts.csv
```

### Import errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Rate limiting
Add delay in config or reduce `--limit` parameter

## 📞 Need Help?

- Read `DATASET_GUIDE.md` for detailed instructions
- Check `DATASET_INTEGRATION_SUMMARY.md` for overview
- Review `SYSTEM_READY.md` for system details
- Run `python test_datasets.py` to verify setup

---

**Status**: ✅ READY TO USE  
**Version**: 1.0  
**Last Updated**: January 19, 2025
