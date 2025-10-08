import json
import random
from typing import List
from torch.utils.data import Dataset
from anagram_game import AnagramSolverEnv
from base.data import Data

class AnagramDataset(Dataset):
    """PyTorch Dataset for anagram tasks"""
    
    def __init__(self, data: List[Data]):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

def create_english_dictionary():
    """Create English dictionary file"""
    english_words = [
        # 3-letter words
        "cat", "dog", "car", "sun", "run", "big", "red", "hot", "old", "new",
        "boy", "man", "day", "way", "may", "say", "try", "fly", "sky", "eye",
        
        # 4-letter words  
        "book", "tree", "door", "fire", "wind", "star", "moon", "fish", "bird", "bear",
        "house", "water", "light", "dark", "fast", "slow", "good", "nice", "blue", "green",
        "black", "white", "small", "large", "phone", "table", "chair", "paper", "money", "happy",
        
        # 5-letter words
        "world", "right", "great", "small", "every", "start", "place", "where", "after",
        "think", "never", "again", "might", "still", "while", "sound", "below", "voice", "young"
    ]
    
    with open("dictionary.txt", 'w', encoding='utf-8') as f:
        for word in english_words:
            f.write(word + '\n')

def generate_datasets():
    """Generate training and test datasets"""
    print("Creating dictionary...")
    create_english_dictionary()
    
    print("Generating datasets...")
    env = AnagramSolverEnv()
    
    # Training dataset
    train_tasks = []
    for difficulty in range(1, 11):
        tasks = env.generate(num_of_questions=200, difficulty=difficulty)
        train_tasks.extend(tasks)
    
    random.shuffle(train_tasks)
    
    # Save training dataset
    with open("train_dataset.jsonl", 'w', encoding='utf-8') as f:
        for task in train_tasks:
            f.write(task.to_json_str() + '\n')
    
    print(f"Training dataset: {len(train_tasks)} samples")
    
    # Test datasets by difficulty
    random.seed(42)  # For reproducibility
    for difficulty in range(1, 11):
        tasks = env.generate(num_of_questions=50, difficulty=difficulty)
        
        with open(f"test_dataset_difficulty_{difficulty}.jsonl", 'w', encoding='utf-8') as f:
            for task in tasks:
                f.write(task.to_json_str() + '\n')
        
        print(f"Test dataset difficulty {difficulty}: {len(tasks)} samples")
    
    random.seed()  # Reset seed
    print("Dataset generation complete!")

def correctness_reward_func(question: str, response: str) -> float:
    """Reward function for GRPO training"""
    try:
        env = AnagramSolverEnv()
        
        # Create dummy task for verification
        dummy_task = Data(question=question, answer='{"solutions": []}', difficulty=1, metadata={'anagrams': []})
        
        # Extract and verify answer
        extracted_answer = env.extract_answer(response)
        is_correct = env.verify(dummy_task, extracted_answer)
        
        return 1.0 if is_correct else 0.0
        
    except Exception:
        return 0.0

if __name__ == "__main__":
    generate_datasets()