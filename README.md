# Day 1 – First LLM API Call

## What I did
- Setup Python environment
- Called OpenAI API
- Generated response using LLM

## Learnings
- How to use LLM API
- Basic prompt structure

## Day 2 – Log Analyzer Tool

### Features
- Takes log input
- Uses LLM to:
  - Explain issue
  - Suggest root causes
  - Provide fixes

### Example
Input:
ERROR: Kafka timeout

Output:
Explains cause and fixes

## Day 3 – Structured Output

- Converted AI response to JSON
- Enabled machine-readable output
- Added error handling for invalid responses

## Day 4 – AI Microservice

- Built REST API using FastAPI
- Endpoint: POST /analyze-log
- Input: log
- Output: structured JSON analysis

### Run
uvicorn main:app --reload

## Day 5 – Context Awareness

- Added context logs support
- Improved root cause accuracy
- Multi-log reasoning capability

## Day 6 – RAG (Memory System)

- Implemented vector search using FAISS
- Stored known issues as embeddings
- Retrieved similar logs for better analysis

## Day 7 – Persistent Memory

- Stored logs dynamically in memory.json
- Enabled learning from past logs
- Built dynamic retrieval system