# Anagram Solver RL Environment

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PollyLeo6/Anagram-Solver/blob/main/train_agent.ipynb)

Reinforcement Learning environment for training LLM agents to solve anagram puzzles using GRPO.

## 🎯 What is this?

**Anagram solving** - unscramble letters to form valid English words. Train AI agents to solve puzzles of increasing difficulty.

**Example:**
```
Input: ["tac", "god"] 
Agent Output: {"solutions": ["cat", "dog"]}
Verification: ✅ Correct
```

## 🎮 Game Rules

- **Input**: Scrambled letters (anagrams)
- **Output**: JSON format `{"solutions": ["word1", "word2"]}`
- **Goal**: Use each letter exactly once to form valid dictionary words
- **Challenge**: Handle false letters, multiple words, no hints

## 📊 Difficulty Levels (1-10)

| Level | Words | Length | False Letters | Hints |
|-------|-------|--------|---------------|-------|
| 1-3   | 1     | 3-4    | 0             | Category |
| 4-5   | 2     | 3-5    | 0             | Length |
| 6-7   | 2     | 4-6    | 1             | Length |
| 8-9   | 3     | 4-7    | 1             | None |
| 10    | 3     | 5-8    | 2             | None |

## 📁 Project Structure

```
anagram-solver/
├── base/
│   ├── __init__.py          # Package initialization
│   ├── data.py              # Data class with JSON serialization
│   ├── verifier.py          # Abstract Verifier interface
│   └── env.py               # Abstract Env base class
├── anagram_verifier.py      # AnagramVerifier implementation
├── anagram_game.py          # AnagramSolverEnv (inherits from Env)
├── utils.py                 # Dataset utilities + reward function
├── demo.py                  # Manual testing and demonstration
├── train_agent.ipynb        # GRPO training notebook
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Setup
```bash
git clone <repo-url>
cd anagram-solver
pip install -r requirements.txt
```

### 2. Generate Data
```bash
python utils.py
```
Creates dictionary and training datasets.

### 3. Test Environment
```bash
python demo.py
```
Interactive testing - generate puzzles and test solutions.

### 4. Interactive Solver
```bash
python interactive_solver.py
```
Enter your own anagrams and let the AI solve them!

### 5. Train Agent

**Option A: Google Colab (Recommended)**
1. Open [Google Colab](https://colab.research.google.com/)
2. Upload `train_agent.ipynb` or create new notebook
3. Run this setup code:
```python
# Clone repository
!git clone https://github.com/PollyLeo6/Anagram-Solver.git
%cd Anagram-Solver

# Install dependencies
!pip install -r requirements.txt

# Generate datasets
!python utils.py

# Start training
# (Follow notebook instructions)
```

**Option B: Local Training**
```bash
jupyter notebook train_agent.ipynb
```

## 🏗️ Architecture

### Base Classes (`base/`)
- **`Env`**: Abstract environment with `generate()`, `verify()`, `extract_answer()`
- **`Verifier`**: Abstract verifier with `verify()`, `extract_answer()`
- **`Data`**: Task structure with JSON serialization

### Implementation
- **`AnagramSolverEnv`**: Inherits from `Env`, generates puzzles
- **`AnagramVerifier`**: Inherits from `Verifier`, validates solutions

## 💻 Usage

### Environment
```python
from anagram_game import AnagramSolverEnv

env = AnagramSolverEnv()
tasks = env.generate(num_of_questions=5, difficulty=7)
result = env.verify(task, llm_response)
```

### Manual Testing
```python
python demo.py
# Choose difficulty, get anagrams, test your solutions
```

## 🎮 Manual Testing

Test the environment with `demo.py`:

**Menu Options:**
- **1** - Environment demo (automatic demonstration)
- **2** - Interactive mode (solve anagrams yourself)
- **3** - Exit

**Important:** Enter only numbers (1, 2, or 3), not words!

### 🤖 Interactive Solver

Use `interactive_solver.py` for reverse mode - you input anagrams, AI solves them:

```bash
python interactive_solver.py
```

**Example:**
```
Enter anagram letters: tac
✅ Found solutions:
1. ['cat']
JSON format: {"solutions": ["cat"]}
```

**Features:**
- Generate tasks at different difficulty levels
- Interactive puzzle solving
- Test verification system
- See answer extraction in action

**Example:**
```
Difficulty (1-10): 5
Anagrams: ['treeh', 'rac']
Hints: {'word_1': 'length: 5 letters', 'word_2': 'length: 3 letters'}

Your solution: {"solutions": ["three", "car"]}
Result: True ✅
```

## 🎯 Key Features

- **RL Framework Compliant**: Inherits from abstract `Env` class
- **Verifiable**: Automatic solution checking
- **Configurable**: 10 difficulty levels with different parameters
- **GRPO Ready**: Custom reward function for reinforcement learning
- **Reproducible**: Fixed test datasets for evaluation

## 🔧 Customization

**Add words:**
```python
# Edit utils.py
english_words = ["your", "custom", "words"]
```

**Adjust difficulty:**
```python
# Edit anagram_game.py
def _get_difficulty_config(self, difficulty):
    return {'word_count': 3, 'false_letters': 2}
```

## 🚨 Troubleshooting

- **Import errors**: Ensure `base/__init__.py` exists
- **Missing files**: Run `python utils.py` first
- **CUDA memory**: Reduce batch size in notebook

---

**Ready to train your anagram-solving AI?**

1. `python utils.py` - Generate datasets
2. `python demo.py` - Test environment (optional)
3. Open `train_agent.ipynb` - Train with GRPO
4. Evaluate results!