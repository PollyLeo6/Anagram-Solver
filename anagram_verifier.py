import json
import re
from collections import Counter
from base.verifier import Verifier
from base.data import Data

class AnagramVerifier(Verifier):
    """Verifier for anagram tasks"""
    
    def __init__(self):
        super().__init__()
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
    
    def extract_answer(self, test_solution: str) -> str:
        """Extract JSON answer from LLM response"""
        json_pattern = r'\{[^{}]*"solutions"[^{}]*\}'
        matches = re.findall(json_pattern, test_solution, re.IGNORECASE | re.DOTALL)
        
        if matches:
            try:
                return matches[-1]
            except:
                pass
        
        return test_solution.strip()
    
    def verify(self, data: Data, test_answer: str) -> bool:
        """Verify anagram solution"""
        try:
            answer_data = json.loads(test_answer)
            if not isinstance(answer_data, dict) or 'solutions' not in answer_data:
                return False
            
            solutions = answer_data['solutions']
            if not isinstance(solutions, list):
                return False
            
            correct_data = json.loads(data.answer)
            correct_solutions = correct_data['solutions']
            anagrams = data.metadata['anagrams']
            
            if len(solutions) != len(correct_solutions):
                return False
            
            for anagram, correct_word, solution in zip(anagrams, correct_solutions, solutions):
                if not isinstance(solution, str):
                    return False
                
                solution = solution.lower().strip()
                correct_word = correct_word.lower().strip()
                
                if not self._is_valid_anagram(anagram, solution) or solution != correct_word:
                    return False
            
            return True
            
        except (json.JSONDecodeError, KeyError, TypeError):
            return False
    
    def _is_valid_anagram(self, anagram: str, solution: str) -> bool:
        """Check if solution is valid anagram"""
        anagram = anagram.lower().strip()
        solution = solution.lower().strip()
        
        if solution not in self.dictionary:
            return False
        
        anagram_counter = Counter(anagram)
        solution_counter = Counter(solution)
        
        for letter, count in solution_counter.items():
            if anagram_counter[letter] < count:
                return False
        
        return True