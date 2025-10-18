# 🤖 Generative AI for Developers – Complete Guide with Hands-on Projects 🚀

Welcome to the **Generative AI for Developers** repository — your **one-stop learning resource** to understand, build, and deploy real-world applications using Generative AI.

Whether you're a **Python developer**, **JavaScript enthusiast**, or an **AI hobbyist**, this repo will guide you step-by-step to **integrate, fine-tune, and leverage AI models** effectively in your projects.

---

## 🧭 Table of Contents

1. [📚 What You’ll Learn](#-what-youll-learn)
2. [📘 Chapter 1: Introduction to Generative AI](#-chapter-1-introduction-to-generative-ai)
3. [⚙️ Chapter 2: Prompt Engineering](#️-chapter-2-prompt-engineering)
4. [🤖 Chapter 3: AI Agents & Agentic AI](#-chapter-3-ai-agents--agentic-ai)
5. [📚 Chapter 4: Retrieval Augmented Generation (RAG)](#-chapter-4-retrieval-augmented-generation-rag)
6. [🔁 Chapter 5: LangGraph & LangSmith](#-chapter-5-langgraph--langsmith)
7. [💾 Chapter 6: Checkpointing](#-chapter-6-checkpointing)
8. [🧰 Chapter 7: LangChain Tools](#-chapter-7-langchain-tools)
9. [🧍‍♂️ Chapter 8: Human in the Loop (HITL)](#️-chapter-8-human-in-the-loop-hitl)
10. [🧠 Chapter 9: AI Memory](#-chapter-9-ai-memory)
11. [🧩 Chapter 10: Guardrails in AI](#-chapter-10-guardrails-in-ai)
12. [🔍 Chapter 11: RAG System Design (Advanced)](#-chapter-11-rag-system-design-advanced)
13. [🎙️ Chapter 12: Voice Agent](#️-chapter-12-voice-agent)
14. [🎨 Chapter 13: AI Image Generation](#-chapter-13-ai-image-generation)
15. [⚙️ Chapter 14 (Final): Model Context Protocol (MCP)](#️-chapter-14-final-model-context-protocol-mcp)
16. [🔥 Bonus Video – Projects & Career Guide](#-bonus-video--projects--career-guide)
17. [🧠 Tech Stack](#-tech-stack)
18. [⚙️ Setup Instructions](#️-setup-instructions)
    - [1️⃣ Clone the Repository](#1️⃣-clone-the-repository)
    - [2️⃣ Create and Activate Virtual Environment](#2️⃣-create-and-activate-virtual-environment)
    - [3️⃣ Install Dependencies](#3️⃣-install-dependencies)
    - [4️⃣ Set Environment Variables](#4️⃣-set-environment-variables)
    - [5️⃣ Run Examples](#5️⃣-run-examples)
    - [6️⃣ Run Streamlit Applications](#6️⃣-run-streamlit-applications)
19. [📺 Watch the Full YouTube Series](#-watch-the-full-youtube-series)
20. [🤙 Connect Community](#-connect-community)

## 📚 What You’ll Learn

This repository is organized into **14 in-depth chapters**, each designed to help developers build **practical AI applications** — from **Prompt Engineering** to **Voice Agents**, **LangGraph workflows**, **Guardrails**, and more.

---

### 📘 Chapter 1: Introduction to Generative AI

- What is Generative AI?
- Types of Generative AI Models (Text, Image, Audio, Code, etc.)
- Understanding LLMs (Large Language Models)
- Prompting basics with hands-on examples

---

### ⚙️ Chapter 2: Prompt Engineering

- Why Prompt Engineering matters
- Zero-shot, Few-shot, Chain-of-Thought (CoT), and Persona-based prompting
- Self-consistency prompting explained
- Practical examples and real-world prompt design

---

### 🤖 Chapter 3: AI Agents & Agentic AI

- What is an AI Agent and how it works
- Building a CoPilot / Cursor-style code generator
- Understanding Agentic AI & autonomous decision-making
- Live coding project with demonstration

---

### 📚 Chapter 4: Retrieval Augmented Generation (RAG)

- What is RAG and its importance
- Limitations & optimization techniques
- Building RAG pipelines using LangChain + Qdrant DB
- Practical coding with example queries

---

### 🔁 Chapter 5: LangGraph & LangSmith

- What is LangGraph and its use cases
- Creating simple and complex AI workflows
- Streaming outputs & structured outputs explained
- Workflow monitoring using LangSmith
- Comparison with LangFlow and n8n

---

### 💾 Chapter 6: Checkpointing

- Why Checkpointing is essential in AI workflows
- Understanding Thread IDs and state management
- Implementing checkpointing with MongoDB + LangGraph
- Chatbot example using LangChain chat_models

---

### 🧰 Chapter 7: LangChain Tools

- Why LangChain Tools are crucial for production
- Tool creation, binding, calling, and execution
- Building custom tools in LangGraph
- Practical chatbot project with multiple tools

---

### 🧍‍♂️ Chapter 8: Human in the Loop (HITL)

- What is Human in the Loop & why it’s important
- Workflow types: Automated, Controlled, Hybrid
- Using LangGraph’s HITL features
- Real-life examples: Email approval & chatbot escalation

---

### 🧠 Chapter 9: AI Memory

- Why Memory is critical for Generative AI
- Comparing Human Brain vs AI Memory
- Implementing memory using Mem0, Qdrant, and Neo4j
- Real-world context handling in AI chat systems

---

### 🧩 Chapter 10: Guardrails in AI

- What are Guardrails and why we need them
- Implementing Guardrails using OpenAI LLM
- Risks of relying on private LLMs (OpenAI, Gemini, etc.)
- Practical example with Guardrails AI Library

---

### 🔍 Chapter 11: RAG System Design (Advanced)

- Deep dive into advanced RAG architecture
- Query transformation: Multi-query, Decomposition, Step-back Prompting, RAG-Fusion
- Using Message Queues to prevent rate limiting
- Designing scalable RAG systems

---

### 🎙️ Chapter 12: Voice Agent

- Building a Voice Agent from scratch
- Understanding Speech-to-Speech architecture
- Exploring GPT Realtime Model
- Why GPT-4.1 / 4.1-mini can’t be used for voice
- Practical implementation using OpenAI.fm

---

### 🎨 Chapter 13: AI Image Generation

- Text-to-Image & Voice-to-Image generation explained
- Choosing the right image model
- Hands-on image generation with code
- System design and best practices
- Homework: Combine LangChain + LangGraph + Voice Agent

---

### ⚙️ Chapter 14 (Final): Model Context Protocol (MCP)

- Why MCP was introduced
- Understanding MCP architecture: Host, Client, Server
- Layers: Data layer, Transport layer (stdio & Streamable HTTP)
- Full setup: Claude Desktop + MCP Server
- Hands-on tools: Weather & Todo
- Final wrap-up of the Generative AI series

### 🔥 Bonus Video – Projects & Career Guide

Don’t miss the Bonus Chapter, where we discuss:

- Real-world Generative AI project ideas
- Job roles from Entry-level to Expert

---

## 🧠 Tech Stack

- **Language:** Python 3
- **AI APIs:** OpenAI (can extend to Claude, Gemini, etc.)
- **Libraries:** LangChain, LangGraph, Guardrails AI, Mem0, Streamlit

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/LoopKaka/generative-ai.git
cd generative-ai
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables

```bash
OPENAI_API_KEY=your_api_key_here
```

### 5️⃣ Run Examples

```bash
python chapter_1_example.py
```

### 6️⃣ Run Streamlit Applications

```bash
streamlit run chapter_1_app.py
```

## 📺 Watch the Full YouTube Series

🎥 Learn step-by-step with the complete Generative AI for Developers [playlist on YouTube](https://www.youtube.com/playlist?list=PLJlUSSYHG1wbEj9uiMYTmGBAel5Wm2sf4) — including theory, live coding, and project demos.
👉 Subscribe to [Loop Kaka YouTube Channel](https://www.youtube.com/@LoopKaka)

## 🤙 Connect Community

💬 Join the LoopKaka Discord Community!
Got questions, doubts, or want to discuss topics from my videos?
Join our friendly Discord server to connect, learn, and grow together 👉 [https://discord.gg/BZwkqTsbND](https://discord.gg/BZwkqTsbND)
