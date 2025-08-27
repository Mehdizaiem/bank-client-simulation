"""
services/auth_service.py — minimal local session manager for Auth0 flow
Drop this into src/visualisation/services/auth_service.py
"""

import secrets
from datetime import datetime
from typing import Dict, Any, Optional


class SessionManager:
    """Keeps lightweight local sessions keyed by a local_token stored in dcc.Store (and Flask session)."""

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def authenticate_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        local_token = secrets.token_urlsafe(32)
        user_id = user_data["id"]

        self.active_sessions[user_id] = {
            "user_data": user_data,
            "local_token": local_token,
            "authenticated_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
        }
        return {"user_data": user_data, "local_token": local_token, "success": True}

    def get_current_user(self, local_token: str) -> Optional[Dict[str, Any]]:
        for session in self.active_sessions.values():
            if session["local_token"] == local_token:
                return session["user_data"]
        return None

    def logout_user(self, user_id: str) -> None:
        self.active_sessions.pop(user_id, None)


# Singletons
_session_manager = SessionManager()

def get_session_manager() -> SessionManager:
    return _session_manager
