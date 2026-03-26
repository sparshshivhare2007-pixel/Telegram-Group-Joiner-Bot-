import json
import os
from typing import Dict, List

class Database:
    def __init__(self, db_file="data.json"):
        self.db_file = db_file
        self.data = self.load()
    
    def load(self):
        """Load database from file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save(self):
        """Save database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_user_links(self, user_id: int) -> List[str]:
        """Get user's group links"""
        return self.data.get(str(user_id), {}).get("links", [])
    
    def add_links(self, user_id: int, links: List[str]) -> int:
        """Add links for user"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {"links": [], "session": None}
        
        existing_links = set(self.data[user_id_str]["links"])
        new_links = [link for link in links if link not in existing_links]
        
        self.data[user_id_str]["links"].extend(new_links)
        self.save()
        return len(new_links)
    
    def clear_links(self, user_id: int):
        """Clear user's links"""
        user_id_str = str(user_id)
        if user_id_str in self.data:
            self.data[user_id_str]["links"] = []
            self.save()
    
    def set_session(self, user_id: int, session_file: str):
        """Set user's session file"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {"links": [], "session": None}
        
        self.data[user_id_str]["session"] = session_file
        self.save()
    
    def get_session(self, user_id: int) -> str:
        """Get user's session file"""
        return self.data.get(str(user_id), {}).get("session")
    
    def has_session(self, user_id: int) -> bool:
        """Check if user has session"""
        session = self.get_session(user_id)
        return session is not None and os.path.exists(session)
    
    def remove_session(self, user_id: int):
        """Remove user's session"""
        user_id_str = str(user_id)
        if user_id_str in self.data:
            session = self.data[user_id_str].get("session")
            if session and os.path.exists(session):
                os.remove(session)
            self.data[user_id_str]["session"] = None
            self.save()
