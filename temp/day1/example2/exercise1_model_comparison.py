# exercise1_model_comparison.py
from utils.llm_client import get_llm_client
import json
from datetime import datetime

# Test prompts covering different capabilities
TEST_PROMPTS = [
    {
        "name": "code_generation",
        "prompt": "Write a function that finds the longest palindromic substring. Include type hints and a docstring.",
        "evaluate": ["correctness", "code_quality", "documentation"]
    },
    {
        "name": "reasoning",
        "prompt": "A farmer has 17 sheep. All but 9 die. How many sheep are left? Explain your reasoning step by step.",
        "evaluate": ["correct_answer", "explanation_quality"]
    },
    {
        "name": "refactoring",
        "prompt": "Refactor this code to be more idiomatic:\n\ndef get_evens(numbers):\n    result = []\n    for i in range(len(numbers)):\n        if numbers[i] % 2 == 0:\n            result.append(numbers[i])\n    return result",
        "evaluate": ["improvement", "explanation"]
    },
]

def run_comparison():
    providers = ["google", "groq", "ollama"]
    
    results = {}

    for test in TEST_PROMPTS:
        results[test["name"]] = {}
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")

        for provider in providers:
            try:
                client = get_llm_client(provider)
                messages = [
                    {"role": "system", "content": "You are a helpful programming assistant."},
                    {"role": "user", "content": test["prompt"]}
                ]

                response = client.chat(messages)
                results[test["name"]][provider] = {
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                }

                print(f"\n--- {provider.upper()} ---")
                print(response[:500] + "..." if len(response) > 500 else response)

            except Exception as e:
                results[test["name"]][provider] = {"error": str(e)}
                print(f"\n--- {provider.upper()} ---")
                print(f"Error: {e}")

    # Save results
    with open("model_comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_comparison()