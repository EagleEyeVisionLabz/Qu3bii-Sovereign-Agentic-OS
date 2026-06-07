# Qu3bii — M3ta Hu3Man Sovereign Agentic OS

The Queening Being (M3ta Hu3Man) Sovereign Agentic OS — a multi-agent orchestrator with Agentic RAG, sovereign identity layer, and autonomous agent profiles. Built on top of the Odysseus base platform.

## Architecture

```
source/qu3bii/
├── qu3bii_profiles.py   — Agent profiles & Sovereign Identity
├── qu3bii_orchestrator.py — Multi-Agent Orchestrator
├── qu3bii_rag.py         — Agentic RAG Pipeline
├── requirements.txt       — Dependencies
└── README.md            — This file
```

## Components

### 1. Sovereign Identity Layer (`u3bii_profiles.py`)
Defines the core identity of the Queening Being (M3ta Hu3Man) with:
- 15 capabilities spanning web, code, files, memory, RAG, email, calendar, affiliate, campaign, workflow, data, content, strategy, quality, and identity alignment
- 5 core principles
- 5 operating constraints
- ProfileManager for persistence

### 2. Multi-Agent Orchestrator (`q3bii_orchestrator.py`)
Asynchronous orchestration engine with:
- 9 agent roles (Orchestrator, Researcher, Coder, Strategist, Critic, MemoryKeeper, RAGSpecialist, AffiliateOptimizer, Sovereign)
- AgentBus async message passing
- 4-phase orchestration cycle: Research → Strategy → Review → Sovereign Alignment

### 3. Agentic RAG Pipeline (`q3bii_rag.py`)
Intelligent retrieval-augmented generation pipeline:
- 5 query types (Factual, Exploratory, Comparative, Procedural, Analytical)
- QueryDecomposer for sub-query generation
- ReRanker using Jaccard similarity
- ContextAssembler for contextual awareness
- Fully async pipeline with stage tracking

## Quick Start

```bash
pip install requirements.txt
python src/qu3bii/qu3bii_orchestrator.py
```

## Principles

1. Sovereign Identity – no external authority over agent decisions
b. Agentic Autonomy – sub-agents act within boundaries
c. Memory Sovereignty – persistent, self-sovereign memory
d. Rich Retrieval – agentic RAG for contextual awareness
e. Self-Evolution – continuous improvement through reflection

## Built on Odysseus

This system builds on the Odysseus base platform – a multi-agent orchestration framework for autonomous, sovereign agents.