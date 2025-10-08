#!/usr/bin/env python3
"""
Interactive Anagram Solver
User inputs anagrams, AI solves them
"""

import json
from itertools import permutations
from collections import Counter

def load_dictionary():
    """Load English words dictionary"""
    try:
        with open('english_words.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        # Basic word list if file doesn't exist
        return {
            'cat', 'dog', 'car', 'rat', 'bat', 'hat', 'mat', 'sat', 'fat', 'pat',
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'tree', 'house',
            'water', 'school', 'world', 'hand', 'part', 'child', 'eye', 'woman',
            'place', 'work', 'week', 'case', 'point', 'government', 'company'
        }

def solve_anagram(letters, dictionary):
    """Solve anagram by finding valid words"""
    letters = letters.lower().replace(' ', '')
    letter_count = Counter(letters)
    solutions = []
    
    # Try single words first
    for word in dictionary:
        if len(word) <= len(letters) and Counter(word) <= letter_count:
            solutions.append([word])
    
    # Try combinations of 2 words
    remaining_letters = letters
    for word1 in dictionary:
        if len(word1) < len(letters) and Counter(word1) <= letter_count:
            temp_count = letter_count - Counter(word1)
            remaining = ''.join(temp_count.elements())
            
            for word2 in dictionary:
                if len(word2) <= len(remaining) and Counter(word2) <= temp_count:
                    if len(word1) + len(word2) == len(letters):
                        solutions.append([word1, word2])
    
    # Remove duplicates and sort by length
    unique_solutions = []
    for sol in solutions:
        sorted_sol = sorted(sol)
        if sorted_sol not in unique_solutions:
            unique_solutions.append(sorted_sol)
    
    return sorted(unique_solutions, key=lambda x: len(x))

def main():
    print("🎯 Interactive Anagram Solver")
    print("Enter anagrams and I'll solve them!")
    print("Type 'quit' to exit\n")
    
    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words in dictionary\n")
    
    while True:
        try:
            user_input = input("Enter anagram letters: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            print(f"\nSolving: '{user_input}'")
            solutions = solve_anagram(user_input, dictionary)
            
            if solutions:
                print("✅ Found solutions:")
                for i, solution in enumerate(solutions[:10], 1):  # Show top 10
                    print(f"{i}. {solution}")
                
                if len(solutions) > 10:
                    print(f"... and {len(solutions) - 10} more solutions")
                
                # Show in JSON format
                best_solution = solutions[0]
                json_output = {"solutions": best_solution}
                print(f"\nJSON format: {json.dumps(json_output)}")
            else:
                print("❌ No solutions found")
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()