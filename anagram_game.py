import json
import random
from typing import Optional, List, Dict
from base.env import Env
from base.data import Data
from anagram_verifier import AnagramVerifier

def generate_anagram_prompt(anagrams: List[str], hints: Optional[Dict[str, str]] = None) -> str:
    """Generate English prompt for anagram task"""
    prompt = """ANAGRAM SOLVING TASK

RULES:
1. You are given scrambled letters (anagrams) that form valid English words
2. Each anagram corresponds to exactly one word
3. Use only the letters provided in each anagram
4. Each letter must be used exactly once
5. The solution must be a valid English word

TASK:
Solve the following anagrams by rearranging the letters to form valid English words.

ANAGRAMS:
"""
    
    for i, anagram in enumerate(anagrams, 1):
        prompt += f"{i}. {anagram}\n"
    
    if hints:
        prompt += "\nHINTS:\n"
        for key, hint in hints.items():
            prompt += f"- {key}: {hint}\n"
    
    prompt += """
OUTPUT FORMAT:
Provide your answer as a JSON object:
{"solutions": ["word1", "word2", "word3", ...]}

Your answer:"""
    
    return prompt

class AnagramSolverEnv(Env):
    """Anagram solving environment"""
    
    def __init__(self):
        super().__init__("AnagramSolver", AnagramVerifier)
        self.dictionary = self._load_dictionary()
    
    def _load_dictionary(self, path: str = "dictionary.txt") -> set:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return {word.strip().lower() for word in f.readlines() if word.strip()}
        except FileNotFoundError:
            return {
                "cat", "dog", "house", "tree", "book", "water", "fire", "earth", "wind", "star",
                "moon", "sun", "car", "bike", "phone", "table", "chair", "door", "window", "light"
            }
    
    def generate(self, num_of_questions: int = 100, max_attempts: int = 100, difficulty: Optional[int] = 1) -> List[Data]:
        """Generate anagram tasks"""
        config = self._get_difficulty_config(difficulty)
        tasks = []
        
        for _ in range(num_of_questions):
            for attempt in range(max_attempts):
                try:
                    suitable_words = [w for w in self.dictionary 
                                    if config['min_length'] <= len(w) <= config['max_length']]
                    
                    if len(suitable_words) < config['word_count']:
                        continue
                    
                    words = random.sample(suitable_words, config['word_count'])
                    anagrams = [self._create_anagram(word, config['false_letters']) for word in words]
                    hints = self._generate_hints(words, config['hint_type']) if config['hint_type'] else None
                    
                    question = generate_anagram_prompt(anagrams, hints)
                    answer = json.dumps({"solutions": words})
                    metadata = {'anagrams': anagrams, 'target_words': words, 'hints': hints}
                    
                    tasks.append(Data(question=question, answer=answer, difficulty=difficulty, metadata=metadata))
                    break
                except Exception:
                    if attempt == max_attempts - 1:
                        continue
        
        return tasks
    
    def extract_answer(self, test_solution: str) -> str:
        """Extract answer from test solution"""
        return self.verifier.extract_answer(test_solution)
    
    def _get_difficulty_config(self, difficulty: int) -> Dict:
        """Map difficulty to parameters"""
        if difficulty <= 3:
            return {'word_count': 1, 'min_length': 3, 'max_length': 4, 'false_letters': 0, 'hint_type': 'category'}
        elif difficulty <= 5:
            return {'word_count': 2, 'min_length': 3, 'max_length': 5, 'false_letters': 0, 'hint_type': 'length'}
        elif difficulty <= 7:
            return {'word_count': 2, 'min_length': 4, 'max_length': 6, 'false_letters': 1, 'hint_type': 'length'}
        elif difficulty <= 9:
            return {'word_count': 3, 'min_length': 4, 'max_length': 7, 'false_letters': 1, 'hint_type': None}
        else:
            return {'word_count': 3, 'min_length': 5, 'max_length': 8, 'false_letters': 2, 'hint_type': None}
    
    def _create_anagram(self, word: str, false_letters: int) -> str:
        """Create anagram with optional false letters"""
        letters = list(word)
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for _ in range(false_letters):
            letters.append(random.choice(alphabet))
        random.shuffle(letters)
        return ''.join(letters)
    
    def _generate_hints(self, words: List[str], hint_type: str) -> Dict[str, str]:
        """Generate hints for words"""
        hints = {}
        categories = {
            'animal': ['cat', 'dog', 'bird', 'fish', 'bear', 'lion', 'wolf'],
            'object': ['house', 'tree', 'book', 'table', 'chair', 'phone', 'car'],
            'nature': ['water', 'fire', 'earth', 'wind', 'star', 'moon', 'sun'],
            'color': ['red', 'blue', 'green', 'black', 'white']
        }
        
        for i, word in enumerate(words):
            if hint_type == 'category':
                category = 'other'
                for cat_name, cat_words in categories.items():
                    if word in cat_words:
                        category = cat_name
                        break
                hints[f'word_{i+1}'] = f"category: {category}"
            elif hint_type == 'length':
                hints[f'word_{i+1}'] = f"length: {len(word)} letters"
        return hints