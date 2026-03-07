# DocuFill-MCP: Decoupled Data Retrieval & Form Automation

## Overview
A lightweight, enterprise-grade proof-of-concept demonstrating how to decouple LLM reasoning from secure data retrieval. 

This project uses the Model Context Protocol (MCP) and LangGraph to automatically fill parsed document structures (e.g., empty OCR JSON outputs). It securely queries structured SQL databases for client financials and performs RAG (Retrieval-Augmented Generation) on unstructured policy documents to make approval decisions, utilizing cost-effective open-source models via OpenRouter.

## 🏗️ Architecture

To avoid context-window bloat and hardcoded tool integrations, this architecture is split into two distinct layers:

1. **The MCP Server (Data Layer):** A local Python server exposing secure tools to fetch structured client financials and unstructured banking policies.
2. **The LangGraph Client (Reasoning Layer):** An AI agent powered by an open-source model via OpenRouter. It reads an empty JSON schema, dynamically queries the MCP server for necessary context, and outputs a strictly typed, fully populated JSON.

## 📂 Repository Structure

```text
docufill-mcp/
├── mcp_server/
│   ├── server.py              # The MCP server script exposing SQL and RAG tools
│   ├── mock_bank.sqlite       # Dummy database with client financials (SQL)
│   └── bank_policies.txt      # Dummy text file with loan approval rules (RAG)
├── client_agent/
│   ├── agent.py               # LangGraph workflow connecting to MCP and OpenRouter
│   ├── unfilled_sheet.json    # Mock OCR output (Input: empty fields)
│   └── filled_sheet.json      # Final agent output (Output: populated fields)
├── requirements.txt           # dependencies
└── README.md                  # This documentation
```

## ⚙️ Prerequisites & Setup

**1. Clone and setup the environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

**2. Environment Variables:**
Create a `.env` file in the root directory and add your free OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

## 🚀 Execution

The system requires both the server and the client to run concurrently.

**Step 1: Start the MCP Server**
In your first terminal, boot up the data layer:
```bash
python mcp_server/server.py
```

**Step 2: Run the Agent Workflow**
In a separate terminal, trigger the LangGraph client to process the document:
```bash
python client_agent/agent.py
```

**Step 3: Review Output**
Inspect `client_agent/filled_sheet.json` to view the securely populated banking data and the RAG-driven approval reasoning.
