# Sentinel AI — Intelligence API

## Overview

The Intelligence API powers Sentinel AI's on-chain intelligence engine.

It provides:

- Wallet Intelligence
- Wallet DNA
- Funding Chain Analysis
- Bundle Detection
- Deployer Intelligence
- Wallet Clustering
- Graph Intelligence
- Search Engine
- Statistics Engine
- AI Scores
- WebSocket Streaming
- Administrative Operations

---

# Architecture

```
app/
├── routers/
├── websocket/
├── repositories/
├── validators/
├── models/
├── docs/
```

---

# Technologies

- FastAPI
- PostgreSQL
- ClickHouse
- Neo4j
- Redis
- WebSockets
- Pydantic
- SQLAlchemy

---

# Repository Layer

The Repository layer abstracts every storage backend.

Supported repositories:

- PostgreSQL
- ClickHouse
- Neo4j
- Redis

Entity repositories:

- Wallet
- Token
- Funding
- Bundle
- Deployer
- Cluster
- Graph
- Wallet DNA
- Statistics
- Search
- Export

---

# API Modules

## Wallet

Wallet analytics

## Token

Token intelligence

## Funding

Funding chain analysis

## Bundle

Bundle detection

## Deployer

Deployer intelligence

## Cluster

Wallet clustering

## Graph

Relationship visualization

## Wallet DNA

AI scoring engine

## Statistics

Analytics engine

## Search

Global search

## Health

Runtime status

## Admin

Administrative endpoints

---

# WebSocket Streams

- Wallet Stream
- Funding Stream
- Graph Stream
- Statistics Stream
- Alerts Stream

---

# Validation Layer

Input validation

- Wallet
- Token
- Funding
- Graph
- Query

---

# Documentation

OpenAPI

Examples

Tags

---

# Features

- AI Wallet Scoring
- Conviction Score
- Narrative Score
- Rug Detection
- Wallet Graph
- Funding Chain
- Bundle Detection
- Wallet Clustering
- Real-time Streams
- Global Search
- Export Engine

---

# Version

Current Version

```
v1.0.0
```

---

# Author

Sentinel AI

Intelligence Layer