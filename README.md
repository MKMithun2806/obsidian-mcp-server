# Obsidian MCP Server

A Model Context Protocol (MCP) server for interacting with your Obsidian vault via the Local REST API plugin.

## Tools

- `obsidian_list_vault` - List all files/folders in vault root
- `obsidian_list_dir` - List files in a specific directory
- `obsidian_read_file` - Read a file's contents
- `obsidian_create_file` - Create a new file
- `obsidian_update_file` - Overwrite a file with new content
- `obsidian_append_file` - Append content to a file
- `obsidian_delete_file` - Delete a file
- `obsidian_search` - Search across all vault files
- `obsidian_move_file` - Move a file to a new path
- `obsidian_copy_file` - Copy a file to a new path
- `obsidian_patch_file` - Insert content at a heading/block/frontmatter
- `obsidian_get_status` - Check API connection status

## Prerequisites

- Obsidian with Local REST API plugin installed and enabled
- Docker Desktop with MCP Toolkit
- Obsidian bound to 0.0.0.0 (not just localhost)

## Setup

### 1. Build the image
```powershell
cd C:\Projects\obsidian-mcp
docker build -t obsidian-mcp-server:latest .
```

### 2. Set the secret
```powershell
docker mcp secret set obsidian-mcp.api_key=YOUR_API_KEY_HERE
```

### 3. Set host config (in config.yaml)
```yaml
obsidian-mcp:
  host: 192.168.1.16
  port: "27124"
```

### 4. Add catalog entry to custom.yaml
Paste the contents of catalog-entry.yaml under the `registry:` key in:
`C:\Users\mmith\.docker\mcp\catalogs\custom.yaml`

### 5. Add to registry.yaml
```yaml
  obsidian-mcp:
    ref: ""
```

### 6. Restart Claude Desktop

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| OBSIDIAN_API_KEY | Yes | - | API key from Obsidian Local REST API plugin |
| OBSIDIAN_HOST | No | 127.0.0.1 | Host where Obsidian is running |
| OBSIDIAN_PORT | No | 27124 | Port for Obsidian REST API |
| OBSIDIAN_PROTOCOL | No | https | Protocol (https or http) |

## Architecture

```
Claude Desktop → MCP Gateway → obsidian-mcp-server → Obsidian Local REST API
                      ↓
              Docker Desktop Secrets
              (obsidian-mcp.api_key)
```
