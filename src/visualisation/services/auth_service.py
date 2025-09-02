"""
services/auth_service.py - Modified to prevent automatic logout
Replace services/auth_service.py with this version
"""

import secrets
from datetime import datetime
from typing import Dict, Any, Optional


class SessionManager:
    """Keeps persistent local sessions - NO AUTOMATIC EXPIRATION"""

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def authenticate_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a persistent session that doesn't expire automatically"""
        local_token = secrets.token_urlsafe(32)
        user_id = user_data["id"]

        self.active_sessions[user_id] = {
            "user_data": user_data,
            "local_token": local_token,
            "authenticated_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "persistent": True  # Mark as persistent session
        }
        
        print(f"User {user_data.get('first_name', 'Unknown')} authenticated - Session will persist")
        return {"user_data": user_data, "local_token": local_token, "success": True}

    def get_current_user(self, local_token: str) -> Optional[Dict[str, Any]]:
        """Get user data - NO expiration check, session persists until manual logout"""
        for user_id, session in self.active_sessions.items():
            if session["local_token"] == local_token:
                # Update last activity but don't check expiration
                session["last_activity"] = datetime.utcnow()
                print(f"Session found for token, returning user data")
                return session["user_data"]
        
        print(f"No session found for token")
        return None

    def logout_user(self, user_id: str) -> None:
        """Manual logout only - removes the session"""
        if user_id in self.active_sessions:
            user_name = self.active_sessions[user_id]["user_data"].get("first_name", "User")
            self.active_sessions.pop(user_id, None)
            print(f"User {user_name} manually logged out")
        else:
            print(f"No session found for user_id: {user_id}")

    def logout_by_token(self, local_token: str) -> None:
        """Logout by token"""
        for user_id, session in list(self.active_sessions.items()):
            if session["local_token"] == local_token:
                user_name = session["user_data"].get("first_name", "User")
                del self.active_sessions[user_id]
                print(f"User {user_name} logged out by token")
                return
        print(f"No session found for token during logout")

    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all active sessions for debugging"""
        return self.active_sessions.copy()

    def clear_all_sessions(self) -> None:
        """Clear all sessions (for testing/debugging)"""
        session_count = len(self.active_sessions)
        self.active_sessions.clear()
        print(f"Cleared {session_count} sessions")


# Singleton instance
_session_manager = SessionManager()

def get_session_manager() -> SessionManager:
    return _session_manager