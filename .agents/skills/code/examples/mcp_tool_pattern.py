"""
Reference Pattern: How to implement a standard MCP tool in this project.

This example demonstrates the canonical structure for adding a new
Redmine MCP tool, following <verb>_redmine_<noun> naming convention.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("redmine")


@mcp.tool()
async def get_redmine_example(
    example_id: int,
    include_details: bool = True,
) -> dict:
    """Get example resource from Redmine.

    Args:
        example_id: The resource ID to retrieve
        include_details: Whether to include extended details

    Returns:
        Dictionary containing resource data
    """
    # 1. Always use environment variables for credentials
    # api_key = os.environ["REDMINE_API_KEY"]

    # 2. Always use parameterized queries for database access
    # row = await db.fetchone(
    #     "SELECT * FROM ods.issues WHERE id = %(issue_id)s",
    #     {"issue_id": example_id},
    # )

    # 3. Always use dict-style access (RealDictCursor), NEVER row[0]
    # result = row["subject"]

    # 4. Return structured dict
    return {"id": example_id, "status": "ok"}
