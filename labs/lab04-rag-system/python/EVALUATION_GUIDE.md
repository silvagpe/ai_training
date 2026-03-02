# RAG System - Evaluation Guide

## Quick Start

### 1. Start the RAG System

```bash
# Make sure you're in the python directory
cd /mnt/dados/projetos/taller/ai_training/labs/lab04-rag-system/python

# Activate virtual environment
source .venv/bin/activate

# Start the server
uvicorn main:app --reload
```

### 2. Index Lab02 Files

Before running evaluation, you need to index the code from lab02:

```bash
python index_lab02.py
```

This will:
- Load all Python files from lab02 (analyzer.py, llm_client.py, main.py, prompts.py)
- Chunk them using smart code-aware chunking
- Store embeddings in ChromaDB
- Report number of chunks indexed

### 3. Run Evaluation

```bash
python run_evaluation.py
```

This will:
- Load 3 evaluation examples from `eval_examples.json` (quick test)
- Query the RAG system for each question
- **Automatically add 15s delays between examples** to avoid rate limits
- Calculate retrieval metrics (Precision@5, Recall@5, MRR)
- Use LLM-as-judge to evaluate answer quality
- Display comprehensive results

**Note:** Each example makes 3 LLM calls (1 for RAG answer + 2 for judging), so with Google Gemini's free tier limit of 5 requests/minute, the evaluation adds automatic delays to stay within limits.

**For full evaluation with 15 examples:**
```bash
python run_evaluation.py --file eval_examples_full.json
# This will take ~4-5 minutes due to rate limit delays
```

## Troubleshooting

### Rate Limit Errors

If you see quota/rate limit errors from Google Gemini:

**The evaluation now includes automatic 15s delays between examples to prevent rate limits.**

This works because:
- Each example makes 3 LLM calls (1 RAG answer + 2 judge scores)
- Google Gemini free tier: 5 requests/minute
- With 15s delays: 4 calls/minute (safely under limit)

If you still hit rate limits:

**Option 1: Use different LLM provider (recommended)**
```bash
# Use Anthropic Claude (requires ANTHROPIC_API_KEY)
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your-key
# Restart the server
uvicorn main:app --reload

# Or use OpenAI (requires OPENAI_API_KEY)
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your-key
uvicorn main:app --reload
```

**Option 2: Wait and retry**
```bash
# Wait 1 minute then retry
sleep 60 && python run_evaluation.py
```

**Option 3: Use smaller dataset (recommended)**

The default `eval_examples.json` now has only 3 examples to avoid rate limits. For comprehensive testing with 15 examples:
```bash
python run_evaluation.py --file eval_examples_full.json
```

### Empty Index Error

If you see "Number of requested results 5 is greater than number of elements in index 2":

```bash
# Re-index the files
python index_lab02.py
```

### Connection Errors

Make sure the RAG system is running:
```bash
# Check health
curl http://localhost:8000/health

# View docs
open http://localhost:8000/docs
```

### Customizing Rate Limit Delays

To adjust the delay between examples, modify `main.py`:

```python
# In main.py, change delay_between_examples parameter
@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    # ...
    gen_metrics = evaluator.evaluate_generation(
        examples,
        delay_between_examples=20.0  # Increase for stricter limits
    )
```

**Recommended delays by provider:**
- Google Gemini free tier: 15-20s
- Anthropic/OpenAI: 0-5s (more generous limits)
- Paid tiers: 0s (no delays needed)

## Files

- `eval_examples.json` - **3 Q&A examples** (quick test, avoids rate limits)
- `eval_examples_full.json` - **15 Q&A examples** (comprehensive evaluation)
- `index_lab02.py` - Script to index lab02 files
- `run_evaluation.py` - Script to run full evaluation
- `main.py` - FastAPI RAG application
- `rag/` - RAG implementation (chunker, pipeline, evaluation, vector store)

**Note:** The reduced 3-example dataset avoids rate limit issues with free-tier LLM providers while still testing all core functionality.

## Example Usage

```bash
# Full workflow
python index_lab02.py
python run_evaluation.py

# Custom URL
python run_evaluation.py --url http://localhost:3000

# Custom dataset
python run_evaluation.py --file my_examples.json
```

## Expected Output

```
📊 RAG EVALUATION
======================================================================

⚠️  Make sure you have indexed files first:
   python index_lab02.py

✅ RAG system is healthy at http://localhost:8000
✅ Loaded 3 evaluation examples from eval_examples.json

🔍 Running evaluation against http://localhost:8000/evaluate...
📊 Testing with 3 examples

======================================================================
📈 EVALUATION RESULTS
======================================================================

🎯 RETRIEVAL METRICS:
  Precision@5: 0.867
  Recall@5:    0.933
  MRR:         0.889

✨ GENERATION METRICS:
  Avg Relevance: 4.3/5.0
  Avg Accuracy:  3.9/5.0

✅ Evaluation completed successfully!
```

## Next Steps

1. Analyze which questions have low precision/recall
2. Improve chunking strategy for better retrieval
3. Experiment with different embedding models
4. Add more diverse evaluation examples
5. Deploy to Railway/Vercel (see main README.md)
