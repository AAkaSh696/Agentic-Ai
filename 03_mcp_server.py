from fastmcp import FastMCP
import subprocess

mcp=FastMCP("Docker MCP Server")

@mcp.tool
def show_running_containers() -> str:
    """Show all currently running Docker containers."""
    result = subprocess.run(
        ["docker", "ps"],
        capture_output=True,
        text=True,
    )
    return result.stdout or result.stderr or "No running containers."


@mcp.tool
def show_container_logs_by_name(container_name: str) -> str:
    """Show the last 50 log lines of a Docker container using its name."""
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", container_name],
        capture_output=True,
        text=True,
    )
    return (result.stdout + result.stderr) or "No logs found."

if __name__ == "__main__":
    mcp.run()