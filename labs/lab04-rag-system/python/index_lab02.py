#!/usr/bin/env python3
"""Script to index the lab02 code analyzer files into the RAG system."""
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


def read_lab02_files(lab02_path: str = "../../lab02-code-analyzer-agent/python") -> dict:
    """Read all Python files from lab02."""
    base_path = Path(lab02_path)
    
    if not base_path.exists():
        print(f"❌ Error: Lab02 path not found: {base_path.absolute()}")
        sys.exit(1)
    
    files_to_index = {}
    python_files = [
        "analyzer.py",
        "llm_client.py", 
        "main.py",
        "prompts.py"
    ]
    
    for filename in python_files:
        filepath = base_path / filename
        if filepath.exists():
            try:
                content = filepath.read_text(encoding='utf-8')
                files_to_index[filename] = content
                print(f"✅ Loaded {filename} ({len(content)} chars)")
            except Exception as e:
                print(f"⚠️  Warning: Could not read {filename}: {e}")
        else:
            print(f"⚠️  Warning: File not found: {filepath}")
    
    if not files_to_index:
        print("❌ Error: No Python files found to index")
        sys.exit(1)
    
    return files_to_index


def index_files(base_url: str, files: dict):
    """Index files into the RAG system."""
    endpoint = f"{base_url}/index/files"
    
    print(f"\n🔍 Indexing {len(files)} files to {endpoint}...")
    
    try:
        response = requests.post(
            endpoint,
            json={"files": files},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ Successfully indexed {result.get('num_chunks', '?')} chunks!")
        print(f"   Message: {result.get('message', 'N/A')}")
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {base_url}")
        print("   Make sure the RAG system is running:")
        print("   uvicorn main:app --reload")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Index lab02 code analyzer files into RAG system"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the RAG API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--lab02-path",
        default="../../lab02-code-analyzer-agent/python",
        help="Path to lab02 python directory"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📚 LAB02 CODE INDEXING")
    print("=" * 70)
    
    # Check if server is healthy
    try:
        health_response = requests.get(f"{args.url}/health", timeout=5)
        health_response.raise_for_status()
        print(f"✅ RAG system is healthy at {args.url}\n")
    except Exception as e:
        print(f"❌ RAG system is not responding at {args.url}")
        print(f"   Error: {e}")
        print("\n   Start the server with: uvicorn main:app --reload")
        sys.exit(1)
    
    # Read lab02 files
    files = read_lab02_files(args.lab02_path)
    
    # Index files
    result = index_files(args.url, files)
    
    print("\n" + "=" * 70)
    print("✅ Indexing complete! You can now run evaluations.")
    print("=" * 70)
    print("\nNext step: python run_evaluation.py")


if __name__ == "__main__":
    main()
