# DocuFill-MCP-Decoupled-Data-Retrieval-Form-Automation
A lightweight, enterprise-grade proof-of-concept demonstrating how to decouple LLM reasoning from secure data retrieval. This project uses the Model Context Protocol (MCP) and LangGraph to automatically fill parsed document structures (like OCR outputs) by securely querying structured SQL databases and performing RAG on unstructured policy documents, utilizing cost-effective open-source models via OpenRouter.

# 🏗️ Architecture Overview
To avoid context-window bloat and hardcoded tool integrations, this architecture is split into two distinct parts:
The MCP Server (Data Layer): A local Python server exposing secure tools to fetch structured client financials and unstructured banking policies (RAG).
The LangGraph Client (Reasoning Layer): An AI agent powered by OpenRouter (e.g., Llama 3) that takes an empty JSON schema, queries the MCP server for necessary context, and outputs a strictly typed, fully populated JSON.

# 📂 Repository Structure
Use this as your weekend checklist to ensure you have every piece in place:

Plaintext
docufill-mcp/
├── mcp_server/
│   ├── server.py              # The MCP server script exposing the SQL and RAG tools
│   ├── mock_bank.sqlite       # Dummy database with client financials (SQL)
│   └── bank_policies.txt      # Dummy text file with loan approval rules (RAG)
├── client_agent/
│   ├── agent.py               # LangGraph workflow connecting to MCP and OpenRouter
│   ├── unfilled_sheet.json    # Mock OCR output (Input: empty fields)
│   └── filled_sheet.json      # Final agent output (Output: populated fields)
├── requirements.txt           # mcp, langgraph, langchain-openai, pydantic, sqlite3
└── README.md                  # This file

⚙️ Development Checklist & Implementation Steps
Phase 1: Environment & Setup
[ ] Create a virtual environment (python -m venv venv).

[ ] Install dependencies: pip install mcp langgraph langchain-openai pydantic.

[ ] Get a free OpenRouter API key and set it in your .env file (OPENROUTER_API_KEY=your_key_here).

Phase 2: The Data Layer (MCP Server)
[ ] Create mock_bank.sqlite and insert 2-3 rows of fake client data (e.g., Client #101: John Doe, Balance: $4000).

[ ] Create bank_policies.txt and write 2-3 simple rules (e.g., "Clients with balances under $5000 are denied loans").

[ ] Write server.py using the Anthropic MCP SDK.

[ ] Expose Tool 1: get_client_financials(client_id) -> Queries the SQLite DB.

[ ] Expose Tool 2: search_policies(query) -> Performs a basic text search/RAG on the text file.

Phase 3: The Reasoning Layer (LangGraph Client)
[ ] Create unfilled_sheet.json (e.g., asking for Name, Balance, Loan Approved [null], Reason [null]).

[ ] Write agent.py to initialize a LangGraph agent.

[ ] Configure the LLM to use OpenRouter. (Note: You use ChatOpenAI from LangChain, but point the base_url to OpenRouter's endpoint and pass your OpenRouter key).

[ ] Connect the agent to the local MCP server so it inherits the two tools.

[ ] Write the system prompt instructing the agent to read unfilled_sheet.json, use its tools to find the data and evaluate the rules, and save the result to filled_sheet.json.

🚀 How to Run Locally
Start the MCP Server:

Bash
python mcp_server/server.py
Run the Agent Workflow:
(In a separate terminal)

Bash
python client_agent/agent.py
Check the Output:
Inspect filled_sheet.json to see the securely populated banking data.
