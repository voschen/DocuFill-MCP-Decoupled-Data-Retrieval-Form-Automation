from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
from dotenv import load_dotenv
import asyncio
import os

# Initiate API Key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Inititate MCP
client = MultiServerMCPClient({
    "bank_server": {
        "command": "python",
        "args": ["/absolute/path/to/your/mcp_server/server.py"], # Use absolute path!
        "transport": "stdio"
    }
})

# Initiate Agent
model = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct:free",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key= OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Initiate State

class AgentState(TypedDict):
    messages: Annotated[list, add_messages] # a list of message OBJECTS not messages, so meta data is included
    unfilled_sheet: dict
    client_financials: dict
    decision_reasoning: str


##################################################
############## Lang Graph Workflow ###############
##################################################

async def call_model(state: AgentState) -> str:
    instructions = SystemMessage(content=(
        "You are a Senior Loan Officer at a bank. Your goal is to fill out the "
        "provided JSON sheet using the tools at your disposal. "
        "1. First, fetch client financials using their ID. "
        "2. Second, check bank policies to see if they are eligible. "
        "3. Once you have both, fill the sheet and explain your reasoning."
    ))


##################################################
################# MAIN PROGRAM ###################
##################################################



async def main():
    async with MultiServerMCPClient({
        "bank_server": {
            "command": "python",
            "args": ["/absolute/path/to/server.py"],
            "transport": "stdio"
        }
    }) as client:

        tools = await client.get_tools()

        llm_with_tools = model.bind_tools(tools)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Added this to make shutting ddown my agent with ctrl+c more gracious
        print("\nAgent shut down manually.")