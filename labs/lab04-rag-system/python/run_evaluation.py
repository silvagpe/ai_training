#!/usr/bin/env python3
"""Script to run RAG evaluation with the dataset."""
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


def load_eval_examples(filepath: str = "eval_examples.json") -> list:
    """Load evaluation examples from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            examples = json.load(f)
        print(f"✅ Loaded {len(examples)} evaluation examples from {filepath}")
        return examples
    except FileNotFoundError:
        print(f"❌ Error: File {filepath} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def run_evaluation(base_url: str = "http://localhost:8000", examples: list = None):
    """Run evaluation against the RAG API."""
    if examples is None:
        examples = load_eval_examples()
    
    endpoint = f"{base_url}/evaluate"
    
    print(f"\n🔍 Running evaluation against {endpoint}...")
    print(f"📊 Testing with {len(examples)} examples\n")
    
    try:
        response = requests.post(
            endpoint,
            json={"examples": examples},  # Wrap in object with 'examples' field
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutes timeout for longer evaluations
        )
        response.raise_for_status()
        
        results = response.json()
        
        # Display results
        print("=" * 70)
        print("📈 EVALUATION RESULTS")
        print("=" * 70)
        
        # Retrieval metrics
        if "retrieval" in results:
            print("\n🎯 RETRIEVAL METRICS:")
            retrieval = results["retrieval"]
            print(f"  Precision@5: {retrieval.get('precision_at_5', 0):.3f}")
            print(f"  Recall@5:    {retrieval.get('recall_at_5', 0):.3f}")
            print(f"  MRR:         {retrieval.get('mrr', 0):.3f}")
        
        # Generation metrics
        if "generation" in results:
            print("\n✨ GENERATION METRICS:")
            generation = results["generation"]
            print(f"  Avg Relevance: {generation.get('avg_relevance', 0):.2f}/5.0")
            print(f"  Avg Accuracy:  {generation.get('avg_accuracy', 0):.2f}/5.0")
        
        # Individual results (if available)
        if "details" in results and results["details"]:
            print("\n📝 INDIVIDUAL RESULTS:")
            for i, detail in enumerate(results["details"][:5], 1):  # Show first 5
                print(f"\n  Example {i}:")
                print(f"    Question: {detail.get('question', 'N/A')[:60]}...")
                print(f"    Precision: {detail.get('precision', 0):.2f}")
                print(f"    Relevance: {detail.get('relevance', 0):.1f}/5")
                print(f"    Accuracy:  {detail.get('accuracy', 0):.1f}/5")
            
            if len(results["details"]) > 5:
                print(f"\n  ... and {len(results['details']) - 5} more examples")
        
        print("\n" + "=" * 70)
        print("✅ Evaluation completed successfully!")
        return results
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {base_url}")
        print("   Make sure the RAG system is running:")
        print("   uvicorn main:app --reload")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"❌ Error: Request timed out after 5 minutes")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        
        # Check for rate limit errors
        if response.status_code == 500:
            try:
                error_detail = response.json().get("detail", "")
                if "quota" in error_detail.lower() or "rate" in error_detail.lower():
                    print("\n⚠️  RATE LIMIT EXCEEDED")
                    print("   The LLM provider has rate limits on the free tier.")
                    print("\n   Solutions:")
                    print("   1. Wait a minute and try again")
                    print("   2. Use a different LLM provider (set LLM_PROVIDER env var)")
                    print("   3. Test with fewer examples first")
                    print("   4. Use Anthropic or OpenAI instead of Google Gemini")
                    print(f"\n   Error details: {error_detail[:200]}...")
            except:
                pass
        
        print(f"\n   Full response: {response.text[:500]}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run RAG evaluation with the dataset"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the RAG API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--file",
        default="eval_examples.json",
        help="Path to evaluation examples JSON file (default: eval_examples.json)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("📊 RAG EVALUATION")
    print("=" * 70)
    print("\n⚠️  Make sure you have indexed files first:")
    print("   python index_lab02.py\n")
    
    # Check if server is healthy
    try:
        health_response = requests.get(f"{args.url}/health", timeout=5)
        health_response.raise_for_status()
        print(f"✅ RAG system is healthy at {args.url}")
    except:
        print(f"⚠️  Warning: Could not verify RAG system health at {args.url}")
        print("   Proceeding anyway...\n")
    
    # Load and run evaluation
    examples = load_eval_examples(args.file)
    run_evaluation(args.url, examples)


if __name__ == "__main__":
    main()
