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

## Day 8 – Smart Retrieval

- Added similarity threshold filtering
- Improved relevance of retrieved logs
- Reduced noise in AI responses

## Day 9 – Observability

- Added logging system
- Tracked requests and responses
- Measured execution time

## Day 10 – Caching

- Added cache layer
- Reduced repeated API calls
- Improved response time

## Day 11 – Rate Limiting

- Added request throttling
- Limited API calls per user
- Improved system stability

## Day 12 – Security

- Added API key authentication
- Secured endpoints
- Restricted unauthorized access

## Day 13 – Clean Architecture

- Separated API, service, and core layers
- Improved maintainability
- Structured system like production code

## Day 14 – Async Processing

- Converted API to async
- Improved concurrency handling
- Reduced blocking operations

## Day 15 – Background Processing

- Added async background task execution
- Improved response time
- Introduced event-driven architecture pattern

## Day 16 – Async Job System

- Added job ID tracking
- Implemented result retrieval API
- Completed async workflow

## Day 17 – Database Integration

- Replaced JSON storage with SQLite
- Added structured persistence layer
- Improved scalability and reliability