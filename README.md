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

## Day 18 – Vector Index Optimization

- Built FAISS index at startup
- Avoided rebuilding on each request
- Improved retrieval performance

## Day 19 – Embedding Optimization

- Implemented batch embeddings
- Reduced API calls
- Improved performance and cost efficiency

## Day 20 – Embedding Persistence

- Stored embeddings in database
- Avoided recomputation
- Improved performance and cost

## Day 21 – Document Ingestion

- Added API to upload knowledge
- Enabled dynamic RAG improvement
- Built platform-like capability

## Day 22 – Tag-Based Retrieval

- Added tagging to documents
- Enabled filtered RAG search
- Improved relevance and accuracy

## Day 23 – Auto Tagging

- Added AI-based log classification
- Automated tagging process
- Improved retrieval accuracy

## Day 24 – Feedback Loop

- Added feedback API
- Enabled system learning
- Improved future responses using feedback

## Day 25 – Metrics & Evaluation

- Added request tracking
- Measured latency and success rate
- Introduced AI evaluation metrics

## Day 26 – Dashboard

- Added visual dashboard for metrics
- Displayed system health
- Improved observability

## Day 27 – Charts & Monitoring

- Added time-based metrics
- Built charts using Chart.js
- Visualized system performance

## Day 28 – Live Dashboard

- Added auto-refresh functionality
- Implemented real-time metric updates
- Improved observability experience

## Day 29 – Alerting System

- Added failure rate alerts
- Added latency alerts
- Enabled proactive monitoring