# Autonomous Document Intelligence System

### Cyber Ireland 2022 Report – Agentic Query Backend

## Overview

This project implements an **agentic backend system** that transforms a static PDF report into a **dynamic, queryable knowledge source**. The system ingests the *Cyber Ireland 2022 Report*, processes its contents through an ETL pipeline, and allows complex multi-step queries to be answered through an autonomous agent architecture.

Unlike basic Retrieval-Augmented Generation (RAG) systems, this architecture introduces **task planning, tool usage, verification, and reasoning traces** to ensure reliable, explainable responses.

The backend exposes a single API endpoint that accepts natural language queries and orchestrates multiple agents to retrieve data, perform computations, and validate results before returning an answer.

---

# System Architecture

```
PDF Report
    ↓
ETL Pipeline
(Text Extraction + Table Parsing)
    ↓
Document Chunking
    ↓
Planner Agent
    ↓
Tool Agents
 ├── Retrieval Agent
 ├── Table Agent
 └── Math Agent
    ↓
Verification Agent
    ↓
FastAPI Backend (/query endpoint)
    ↓
Execution Logs (traces.json)
```

---

# Key Features

### 1. ETL Pipeline

The system begins with a structured ETL process to convert unstructured PDF data into machine-usable information.

**Extraction**

* Text extraction using **PyMuPDF**
* Table extraction using **pdfplumber**

**Transformation**

* Document chunking for retrieval
* Normalization of extracted text blocks

**Loading**

* Chunks are stored in memory for retrieval by the agent system.

Files involved:

```
etl/extract_text.py
etl/extract_tables.py
etl/chunk_documents.py
```

---

### 2. Agentic Architecture

Instead of a simple RAG system, this project implements a **multi-agent reasoning pipeline**.

#### Planner Agent

The planner determines which tool or agent should handle the query.

Example tasks:

* Retrieval queries
* Data comparison queries
* Mathematical computation queries

```
agents/planner_agent.py
```

---

#### Retrieval Agent

Responsible for locating factual information inside the document chunks.

Capabilities:

* Searches document chunks
* Returns citation text
* Provides page number reference

```
agents/retrieval_agent.py
```

---

#### Table Analysis Agent

Handles questions requiring comparative reasoning over extracted metrics.

Example:

> Compare pure-play cybersecurity firms in the South-West vs the national average.

```
agents/table logic inside API
```

---

#### Math Agent

Handles quantitative reasoning tasks such as CAGR calculations.

LLMs are unreliable for numerical reasoning, so the system uses a deterministic computation tool.

```
agents/math_agent.py
```

---

#### Verification Agent

Prevents hallucinated answers by confirming that returned information exists in the document.

The agent checks whether retrieved values appear in the source text before returning the result.

```
agents/verifier_agent.py
```

---

# Backend API

The system exposes a FastAPI backend endpoint.

### Endpoint

```
POST /query
```

Example request:

```json
{
  "query": "What is the total number of jobs reported?"
}
```

Example response:

```json
{
  "answer": "7351 jobs",
  "page": 17,
  "citation": "We estimate that there are 7,351 cyber security professionals...",
  "steps": [
    "Planner agent classified query into 'retrieve' task category",
    "Retrieval agent searched document chunks",
    "Verifier agent confirmed evidence in source text"
  ]
}
```

---

# Execution Traces

To ensure transparency and debugging visibility, the system records **reasoning traces** for every query.

Location:

```
logs/traces.json
```

Example trace:

```json
{
  "query": "What is the total number of jobs reported?",
  "steps": [
    "Planner agent classified query into 'retrieve' task category",
    "Retrieval agent searched document chunks",
    "Verifier agent confirmed evidence in source text"
  ],
  "answer": "7351 jobs",
  "source_page": 17,
  "execution_time_ms": 0.2
}
```

These logs demonstrate:

* reasoning path
* tool usage
* execution performance

---

# Evaluation Test Scenarios

The system successfully handles the three required evaluation challenges.

---

## 1. Verification Challenge

Query:

```
What is the total number of jobs reported, and where exactly is this stated?
```

Output:

```
7351 jobs
Page: 17
Citation: "We estimate that there are 7,351 cyber security professionals..."
```

Agents involved:

```
Planner → Retrieval → Verification
```

---

## 2. Data Synthesis Challenge

Query:

```
Compare the concentration of Pure-Play cybersecurity firms in the South-West against the National Average.
```

Result:

```
Pure-play firms represent 32.7% of cybersecurity firms nationally.
The South-West region shows higher concentration due to clustering in Cork.
```

Agents involved:

```
Planner → Table Analysis Agent
```

---

## 3. Forecasting Challenge

Query:

```
Based on our 2022 baseline and the 2030 target, what CAGR is required?
```

Calculation:

```
Baseline jobs: 7351
Target jobs: 17000
Years: 8

CAGR = ((17000 / 7351)^(1/8)) - 1
```

Result:

```
11.05% CAGR required
```

Agents involved:

```
Planner → Math Agent
```

---

# Project Structure

```
patronus
│
├── api
│   └── main.py
│
├── agents
│   ├── planner_agent.py
│   ├── retrieval_agent.py
│   ├── math_agent.py
│   └── verifier_agent.py
│
├── etl
│   ├── extract_text.py
│   ├── extract_tables.py
│   └── chunk_documents.py
│
├── logs
│   └── traces.json
│
├── data
│   └── cyber_report.pdf
│
├── test_queries.py
│
└── requirements.txt
```

---

# Setup Instructions

### 1. Clone repository

```
git clone <repository-url>
cd patronus
```

---

### 2. Create environment

```
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the backend

```
uvicorn api.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000/docs
```

---

### 5. Run automated tests

```
python test_queries.py
```

---

# Limitations

While the system successfully demonstrates an agentic architecture, several improvements would be required for production deployment.

### Retrieval Strategy

Currently uses keyword-based chunk search.
A production system would incorporate:

* embedding-based retrieval
* vector databases (FAISS, Pinecone, Weaviate)

---

### Table Processing

Some table-derived metrics are manually extracted.
Future versions should include:

* automated table schema parsing
* structured dataframe queries

---

### Scalability

The current implementation operates in-memory for a single document.
Production systems would require:

* persistent vector storage
* distributed task execution
* caching layers

---

### Query Planning

The planner currently uses rule-based logic.
Future improvements may include:

* LLM-based planners
* tool routing frameworks (LangGraph)

---

# Future Improvements

Potential enhancements include:

* vector search retrieval
* multi-document ingestion
* automatic table reasoning
* real-time document updates
* distributed agent orchestration

---

# Conclusion

This project demonstrates a **lightweight autonomous intelligence backend** capable of transforming static documents into structured knowledge through an agent-based architecture.

Key capabilities include:

* ETL processing of unstructured PDFs
* multi-agent query planning
* reliable computation tools
* verification mechanisms to prevent hallucination
* reasoning trace logging for transparency

The system satisfies the core requirements of the assignment while providing a scalable foundation for more advanced document intelligence systems.
