#!/usr/bin/env python3
"""
Obsidian MCP Server - Interact with Obsidian vault via Local REST API
"""

import os
import sys
import logging
import json
import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("obsidian-server")

mcp = FastMCP("obsidian-mcp")

API_KEY = os.environ.get("API_KEY", os.environ.get("OBSIDIAN_API_KEY", ""))
HOST = os.environ.get("HOST", os.environ.get("OBSIDIAN_HOST", "127.0.0.1"))
PORT = os.environ.get("PORT", os.environ.get("OBSIDIAN_PORT", "27124"))
PROTOCOL = os.environ.get("PROTOCOL", os.environ.get("OBSIDIAN_PROTOCOL", "https"))

def get_base_url():
    """Return base URL for Obsidian REST API."""
    return f"{PROTOCOL}://{HOST}:{PORT}"

def get_headers():
    """Return auth headers."""
    return {"Authorization": f"Bearer {API_KEY}"}

def get_client():
    """Return httpx client with SSL verification disabled."""
    return httpx.AsyncClient(verify=False, timeout=15)


@mcp.tool()
async def obsidian_list_vault() -> str:
    """List all files and folders in the root of the Obsidian vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    try:
        async with get_client() as client:
            response = await client.get(f"{get_base_url()}/vault/", headers=get_headers())
            response.raise_for_status()
            data = response.json()
            files = data.get("files", [])
            if not files:
                return "📁 Vault is empty"
            return "📁 Vault contents:\n" + "\n".join(f"  - {f}" for f in files)
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_list_dir(dirpath: str = "") -> str:
    """List files and folders in a specific directory of the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not dirpath.strip():
        return "❌ Error: dirpath is required"
    try:
        path = dirpath.strip().strip("/")
        async with get_client() as client:
            response = await client.get(f"{get_base_url()}/vault/{path}/", headers=get_headers())
            response.raise_for_status()
            data = response.json()
            files = data.get("files", [])
            if not files:
                return f"📁 Directory '{dirpath}' is empty"
            return f"📁 Contents of '{dirpath}':\n" + "\n".join(f"  - {f}" for f in files)
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_read_file(filepath: str = "") -> str:
    """Read the contents of a file in the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    try:
        path = filepath.strip().strip("/")
        async with get_client() as client:
            response = await client.get(f"{get_base_url()}/vault/{path}", headers=get_headers())
            response.raise_for_status()
            return f"📄 Contents of '{filepath}':\n\n{response.text}"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_create_file(filepath: str = "", content: str = "") -> str:
    """Create a new file in the vault with the given content."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    try:
        path = filepath.strip().strip("/")
        headers = get_headers()
        headers["Content-Type"] = "text/markdown"
        async with get_client() as client:
            response = await client.put(
                f"{get_base_url()}/vault/{path}",
                headers=headers,
                content=content.encode("utf-8")
            )
            response.raise_for_status()
            return f"✅ Created file: '{filepath}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_update_file(filepath: str = "", content: str = "") -> str:
    """Overwrite an existing file in the vault with new content."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    try:
        path = filepath.strip().strip("/")
        headers = get_headers()
        headers["Content-Type"] = "text/markdown"
        async with get_client() as client:
            response = await client.put(
                f"{get_base_url()}/vault/{path}",
                headers=headers,
                content=content.encode("utf-8")
            )
            response.raise_for_status()
            return f"✅ Updated file: '{filepath}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_append_file(filepath: str = "", content: str = "") -> str:
    """Append content to the end of an existing file in the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    try:
        path = filepath.strip().strip("/")
        headers = get_headers()
        headers["Content-Type"] = "text/markdown"
        async with get_client() as client:
            response = await client.post(
                f"{get_base_url()}/vault/{path}",
                headers=headers,
                content=content.encode("utf-8")
            )
            response.raise_for_status()
            return f"✅ Appended content to: '{filepath}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_delete_file(filepath: str = "") -> str:
    """Delete a file from the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    try:
        path = filepath.strip().strip("/")
        async with get_client() as client:
            response = await client.delete(f"{get_base_url()}/vault/{path}", headers=get_headers())
            response.raise_for_status()
            return f"✅ Deleted file: '{filepath}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_search(query: str = "", context_length: str = "100") -> str:
    """Search for text across all files in the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not query.strip():
        return "❌ Error: query is required"
    try:
        ctx_len = int(context_length.strip()) if context_length.strip() else 100
        async with get_client() as client:
            response = await client.post(
                f"{get_base_url()}/search/simple/",
                headers=get_headers(),
                params={"query": query, "contextLength": ctx_len}
            )
            response.raise_for_status()
            results = response.json()
            if not results:
                return f"🔍 No results found for: '{query}'"
            output = [f"🔍 Search results for '{query}' ({len(results)} files):\n"]
            for r in results:
                output.append(f"📄 {r.get('filename', 'unknown')} (score: {r.get('score', 0):.2f})")
                for match in r.get("matches", []):
                    output.append(f"   ...{match.get('context', '')}...")
            return "\n".join(output)
    except ValueError:
        return f"❌ Error: Invalid context_length value: {context_length}"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_move_file(source: str = "", destination: str = "") -> str:
    """Move a file from source path to destination path in the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not source.strip():
        return "❌ Error: source filepath is required"
    if not destination.strip():
        return "❌ Error: destination filepath is required"
    try:
        src = source.strip().strip("/")
        dst = destination.strip().strip("/")
        async with get_client() as client:
            # Read source file
            read_resp = await client.get(f"{get_base_url()}/vault/{src}", headers=get_headers())
            read_resp.raise_for_status()
            content = read_resp.content

            # Write to destination
            headers = get_headers()
            headers["Content-Type"] = "text/markdown"
            write_resp = await client.put(
                f"{get_base_url()}/vault/{dst}",
                headers=headers,
                content=content
            )
            write_resp.raise_for_status()

            # Delete source
            del_resp = await client.delete(f"{get_base_url()}/vault/{src}", headers=get_headers())
            del_resp.raise_for_status()

            return f"✅ Moved '{source}' → '{destination}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_copy_file(source: str = "", destination: str = "") -> str:
    """Copy a file from source path to destination path in the vault."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not source.strip():
        return "❌ Error: source filepath is required"
    if not destination.strip():
        return "❌ Error: destination filepath is required"
    try:
        src = source.strip().strip("/")
        dst = destination.strip().strip("/")
        async with get_client() as client:
            # Read source
            read_resp = await client.get(f"{get_base_url()}/vault/{src}", headers=get_headers())
            read_resp.raise_for_status()
            content = read_resp.content

            # Write to destination
            headers = get_headers()
            headers["Content-Type"] = "text/markdown"
            write_resp = await client.put(
                f"{get_base_url()}/vault/{dst}",
                headers=headers,
                content=content
            )
            write_resp.raise_for_status()

            return f"✅ Copied '{source}' → '{destination}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_patch_file(filepath: str = "", operation: str = "append", target_type: str = "heading", target: str = "", content: str = "") -> str:
    """Patch a file by inserting content relative to a heading, block, or frontmatter field."""
    if not API_KEY.strip():
        return "❌ Error: OBSIDIAN_API_KEY environment variable not set"
    if not filepath.strip():
        return "❌ Error: filepath is required"
    if not target.strip():
        return "❌ Error: target is required"
    try:
        path = filepath.strip().strip("/")
        import urllib.parse
        headers = get_headers()
        headers["Content-Type"] = "text/markdown"
        headers["Operation"] = operation
        headers["Target-Type"] = target_type
        headers["Target"] = urllib.parse.quote(target)
        async with get_client() as client:
            response = await client.patch(
                f"{get_base_url()}/vault/{path}",
                headers=headers,
                content=content.encode("utf-8")
            )
            response.raise_for_status()
            return f"✅ Patched '{filepath}' at {target_type} '{target}' with operation '{operation}'"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def obsidian_get_status() -> str:
    """Check Obsidian REST API connection status and authentication."""
    try:
        async with get_client() as client:
            response = await client.get(f"{get_base_url()}/", headers=get_headers())
            data = response.json()
            auth = data.get("authenticated", False)
            version = data.get("versions", {})
            return f"""✅ Obsidian REST API Status:
- Service: {data.get('service', 'unknown')}
- Authenticated: {auth}
- Obsidian version: {version.get('obsidian', 'unknown')}
- Plugin version: {version.get('self', 'unknown')}
- Host: {HOST}:{PORT}"""
    except Exception as e:
        return f"❌ Error connecting to Obsidian: {str(e)}"


if __name__ == "__main__":
    logger.info("Starting Obsidian MCP server...")
    if not API_KEY:
        logger.warning("OBSIDIAN_API_KEY not set")
    logger.info(f"Connecting to Obsidian at {PROTOCOL}://{HOST}:{PORT}")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)