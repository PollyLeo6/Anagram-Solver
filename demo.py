from anagram_game import AnagramSolverEnv
from utils import create_english_dictionary

def demo_environment():
    """Demonstrate the RL environment"""
    print("=== ANAGRAM SOLVER RL ENVIRONMENT ===\n")
    
    # Create dictionary
    print("Creating dictionary...")
    create_english_dictionary()
    
    # Initialize environment
    env = AnagramSolverEnv()
    print("✓ Environment initialized\n")
    
    # Demo 1: Generate tasks by difficulty
    print("--- Generate by Difficulty ---")
    for difficulty in [1, 5, 10]:
        tasks = env.generate(num_of_questions=1, difficulty=difficulty)
        task = tasks[0]
        
        print(f"Difficulty {difficulty}:")
        print(f"Anagrams: {task.metadata['anagrams']}")
        print(f"Answers: {task.metadata['target_words']}")
        if task.metadata['hints']:
            print(f"Hints: {task.metadata['hints']}")
        print()
    
    # Demo 2: Test verification
    print("--- Test Verification ---")
    task = tasks[0]  # Use last generated task
    
    # Correct answer
    result = env.verify(task, task.answer)
    print(f"Correct answer: {result}")
    
    # Wrong answer
    wrong_answer = '{"solutions": ["wrong", "answer"]}'
    result = env.verify(task, wrong_answer)
    print(f"Wrong answer: {result}")
    print()
    
    # Demo 3: Extract answer functionality
    print("--- Extract Answer ---")
    test_responses = [
        '{"solutions": ["cat", "dog"]}',
        'I think the answers are: {"solutions": ["house", "tree"]}',
        'The solutions are ["bird", "fish"] in JSON format.',
    ]
    
    for response in test_responses:
        extracted = env.extract_answer(response)
        print(f"Response: {response}")
        print(f"Extracted: {extracted}")
        print()

def interactive_demo():
    """Interactive demonstration"""
    print("=== INTERACTIVE MODE ===\n")
    
    env = AnagramSolverEnv()
    current_task = None
    
    while True:
        print("1. Generate task")
        print("2. Test solution")
        print("3. Exit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            difficulty = int(input("Difficulty (1-10): "))
            tasks = env.generate(num_of_questions=1, difficulty=difficulty)
            current_task = tasks[0]
            
            print(f"\nAnagrams: {current_task.metadata['anagrams']}")
            if current_task.metadata['hints']:
                print(f"Hints: {current_task.metadata['hints']}")
            print(f"(Correct answers: {current_task.metadata['target_words']})")
        
        elif choice == "2":
            if current_task is None:
                print("Generate a task first!")
                continue
            
            solution = input("Your solution (JSON format): ")
            result = env.verify(current_task, solution)
            
            print(f"Result: {result}")
        
        elif choice == "3":
            break
        
        print()

def main():
    """Main demo function"""
    print("ANAGRAM SOLVER RL ENVIRONMENT DEMO")
    print("=" * 50)
    
    while True:
        print("\n1. Environment demo")
        print("2. Interactive mode")
        print("3. Exit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            demo_environment()
        elif choice == "2":
            interactive_demo()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()