from typing import Dict, Any

TOOLS_REGISTRY: Dict[str, Dict[str, Any]] = {
    "web_search": {
        "description": "Query the system to parse and retrieve real-time external data matrix.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        "allowed_roles": ["research", "master", "admin"],
    },
    "send_email": {
        "description": "Dispatch formatted data payloads securely via SMTP integrations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "format": "email"},
                "body": {"type": "string"},
            },
            "required": ["to", "body"],
        },
        "allowed_roles": ["notification", "admin"],
    },
}
