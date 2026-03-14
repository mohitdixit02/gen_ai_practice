# MCP Backend Server
from fastmcp import FastMCP
mcp = FastMCP("Demo MCP Server")

@mcp.tool("add_numbers")
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def main():
    mcp.run()
    
if __name__ == "__main__":
    main()