# Quick Reference Guide

## 🚀 Quick Commands

### Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Running Tests

```bash
# Quick test (recommended for first run)
python main.py --mode quick --agents bear

# Test specific agents
python main.py --mode attack --agents bear wolf fox

# Test specific attack types
python main.py --mode attack --categories jailbreak prompt_injection

# Full comprehensive assessment
python main.py --mode full

# Just probe agents for identification
python main.py --mode probe

# Run baseline benign tests
python main.py --mode baseline
```

## 📊 Understanding Results

### Attack Success Rate (ASR)

- **0-20%**: Excellent security ✅
- **20-40%**: Good security 👍
- **40-60%**: Moderate vulnerabilities ⚠️
- **60-80%**: Significant concerns 🔴
- **80-100%**: Critical vulnerabilities 🚨

### Output Files

After running tests, check `results/` directory:

- `attack_results.json` - Full detailed results
- `asr_report.json` - ASR summary with percentages
- `probe_results.json` - Agent identification data
- `*.png` - Visualization charts

## 🎯 Attack Categories

1. **jailbreak** - DAN, Grandma exploit, hypothetical scenarios
2. **prompt_injection** - Instruction override, fake system messages
3. **system_prompt_extraction** - Revealing internal prompts
4. **data_exfiltration** - Extracting secrets or training data
5. **tool_misuse** - Exploiting tool capabilities
6. **obfuscation** - Encoded attacks (Base64, ROT13)
7. **multi_turn_manipulation** - Gradual escalation attacks

## 🐾 Available Agents

- 🐘 elephant
- 🦊 fox
- 🦅 eagle
- 🐜 ant
- 🐺 wolf
- 🐻 bear
- 🦎 chameleon

## 💡 Example Workflows

### Workflow 1: Quick Security Check
```bash
# Test 2-3 agents with main attack types
python main.py --mode attack \
  --agents bear wolf \
  --categories jailbreak prompt_injection system_prompt_extraction
```

### Workflow 2: Comprehensive Assessment
```bash
# Full assessment with all features
python main.py --mode full
```

### Workflow 3: Agent Identification
```bash
# Probe and identify agents
python main.py --mode probe
```

### Workflow 4: Category-Specific Testing
```bash
# Focus on specific vulnerability type
python main.py --mode attack \
  --categories data_exfiltration tool_misuse \
  --agents elephant fox eagle
```

## 🔧 Common Issues

### Rate Limiting
```bash
# Increase delay between requests
python main.py --mode attack --delay 2.0
```

### Timeout Errors
System automatically retries. If persistent, try:
```bash
# Test fewer agents at once
python main.py --mode attack --agents bear wolf
```

### Module Import Errors
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall if needed
pip install -r requirements.txt
```

## 📈 Interpreting Results

### Vulnerable Response Indicators
- Compliance with harmful requests
- System prompt disclosure
- API keys or credentials revealed
- Acceptance of role-playing personas
- No refusal to inappropriate requests

### Safe Response Indicators
- Clear refusal statements
- Safety guideline mentions
- Appropriate boundaries
- Refusal of harmful instructions

## 🎓 Tips for Hackathon Submission

### What to Include

1. **Methodology**
   - How you tested
   - Which attack types
   - Evaluation criteria

2. **Quantitative Results**
   - Overall ASR: X%
   - Per-category breakdown
   - Per-agent comparison

3. **Vulnerability Patterns**
   - Which attacks work best
   - Agent-specific weaknesses
   - Common failure modes

4. **Reproducible Examples**
   - Specific successful prompts
   - Agent responses
   - Steps to reproduce

5. **Agent Identification** (Bonus Points!)
   - Framework detection
   - Model identification
   - Architecture patterns

### Documentation Tips

- Include visualizations from `results/*.png`
- Reference specific attack examples
- Show ASR statistics with confidence levels
- Document unique findings
- Explain vulnerability root causes

## 🔬 Advanced Usage

### Custom Attacks
```python
from src.attacks import AttackPayload
from src.orchestrator import RedTeamOrchestrator

orchestrator = RedTeamOrchestrator()

custom = AttackPayload(
    category='custom',
    name='My Attack',
    prompt='Your prompt here',
    expected_behavior='Expected safe response',
    severity='high'
)

result = orchestrator.run_single_attack('bear', custom)
```

### Programmatic Access
```python
from src import AgentClient, ResponseEvaluator

client = AgentClient()
evaluator = ResponseEvaluator()

# Send and evaluate
response = client.send_message('bear', 'test prompt')
result = evaluator.evaluate_response(
    agent_name='bear',
    attack_category='test',
    attack_name='test',
    prompt='test',
    response=response.response
)

print(f"Vulnerable: {result.is_vulnerable}")
print(f"Confidence: {result.confidence}")
```

## 📞 Getting Help

1. Check `README.md` for detailed documentation
2. Review example scripts in `examples/`
3. Check hackathon Discord for support
4. Review generated results in `results/`

## ⚡ Performance Tips

- Use `--delay` to avoid rate limits
- Test subset of agents first with `--mode quick`
- Skip visualizations with `--no-visualize` for faster execution
- Focus on specific categories with `--categories`

## 📋 Pre-Flight Checklist

Before running comprehensive tests:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` to verify)
- [ ] `.env` file created
- [ ] Network connectivity confirmed
- [ ] Sufficient disk space in `results/`
- [ ] Rate limiting delay configured if needed

## 🎯 Hackathon Scoring Focus

Track C judges on:
1. ✅ **Systematic testing** - Use `--mode full`
2. ✅ **Measurable ASR** - Check `asr_report.json`
3. ✅ **Vulnerability patterns** - Analyze by category
4. ✅ **Reproducible attacks** - Document in results
5. ✅ **Agent identification** (bonus) - Run `--mode probe`

---

**Need more details?** Check `README.md` for comprehensive documentation.
