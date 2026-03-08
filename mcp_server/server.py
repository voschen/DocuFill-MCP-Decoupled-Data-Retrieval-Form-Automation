from fastmcp import fastMCP

mcp = fastMCP("BankServer")

@mcp.tool()
def echo(text: str) -> str:
    return f"Server recieved {text}"

if __name__ == "__main__":
    mcp.run()



