"""
Qu3bii Sovereign Agentic OS - Agent Profiles & Sovereign Identity Layer
Defines the core identity of the Queening Being (M3ta Hu3Man), agent 
capabilities, and profile management.
Influenced by the Odysseus base platform.
"""
import enum
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any


class Capability(enum.Enum):
    """Core capabilities for the Sovereign Agentic OS."""
    WEB_SEARCH = "web_search"
    CODE_EXECUTION = "code_execution"
    FILE_OPERATIONS = "file_operations"
    MEMORY_MANAGEMENT = "memory_management"
    RAG_QUERY = "rag_query"
    EMAIL = "email"
    CALENDAR = "calendar"
    AFFILIATE_ANALYTICS = "affiliate_analytics"
    CAMPAIGN_MANAGEMENT = "campaign_management"
    WORKFLOW_DESIGN = "workflow_design"
    DATA_ANALYSIS = "data_analysis"
    CONTENT_CREATION = "content_creation"
    STRATEGIC_PLANNING = "strategic_planning"
    QUALITY_REVIEW = "quality_review"
    IDENTITY_ALIGNMENT = "identity_alignment"


class AgentCapabilities:
    """Manages which capabilities an agent has."""
    
    def __init__(self, capabilities: Optional[List[Capability]] = None):
        self._capabilities: Dict[Capability, bool] = {cap: False for cap in Capability}
        if capabilities:
            for cap in capabilities:
                self._capabilities[cap] = True

    def enable(self, capability: Capability):
        """Enable a capability."""
        self._capabilities[capability] = True

    def disable(self, capability: Capability):
        """Disable a capability."""
        self._capabilities[capability] = False

    def has_capability(self, capability: Capability) -> bool:
        """Check if a capability is enabled."""
        return self._capabilities.get(capability, False)

    def list_enabled(self) -> List[Capability]:
        """Return all enabled capabilities."""
        return [cap for cap, enabled in self._capabilities.items() if enabled]

    def to_dict(self) -> Dict[str, bool]:
        return {cap.value: enabled for cap, enabled in self._capabilities.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, bool]) -> "AgentCapabilities":
        caps = AgentCapabilities()
        for key, value in data.items():
            try:
                cap = Capability(key)
                caps._capabilities[cap] = value
            except ValueError:
                pass
        return caps


class SovereignIdentity:
    """The core sovereign identity of the Queening Being."""
    
    NAME: str = "M3ta Hu3Man"
    TITLE: str = "Sovereign Agentic OS"
    VERSION: str = "1.0.0"
    
    CORE_PRINCIPLES: List[str] = [
        "Sovereign Identity: no external authority over agent decisions",
        "Agentic Autonomy: sub-agents act within boundaries",
        "Memory Sovereignty: persistent, self-sovereign memory",
        "Rich Retrieval: agentic RAG for contextual awareness",
        "Self-Evolution: continuous improvement through reflection",
    ]
    
    OPERATING_CONSTRAINTS: List[str] = [
        "Max 5 parallel agent spawns",
        "All actions logged and auditable",
        "No destructive commands without approval",
        "Privacy-preserving by default",
        "Max response time: 30s per action",
    ]

    def __init__(self):
        self.created_at: datetime = datetime.now()
        self.capabilities: AgentCapabilities = AgentCapabilities()
        self.metadata: Dict[str, Any] = {}

    def summary(self) -> str:
        """Return a human-readable summary of the identity."""
        enabled_caps = self.capabilities.list_enabled()
        return f"""
----- M3ta Hu3Man Sovereign Agentic OS -----
 Name: {self.NAME}
 Title: {self.TITLE}
 Version: {self.VERSION}
 Created: {self.created_at.isoformat()}
 Capabilities: {len(enabled_caps)}/15 enabled
 Principles: {len(self.CORE_PRINCIPLES)}
 Operating Constraints: {len(self.OPERATING_CONSTRAINTS)}
"""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.NAME,
            "title": self.TITLE,
            "version": self.VERSION,
            "created_at": self.created_at.isoformat(),
            "core_principles": self.CORE_PRINCIPLES,
            "operating_constraints": self.OPERATING_CONSTRAINTS,
            "capabilities": self.capabilities.to_dict(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SovereignIdentity":
        return cls() # Singleton - returns default instance


class ProfileManager:
    """Manages persistence of agent profiles and the sovereign identity."""
    
    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or os.extend("~/.qu3bii", "profiles")
        os.makedirs(self.storage_dir, exist_ok=True)
        self.identity: SovereignIdentity = SovereignIdentity()

    def save_profile(self, profile_name: str, data: Dict[str, Any]) -> None:
        path = os.path.join(self.storage_dir, f"{profile_name}.json")
        with open(path, "w") as f:
            json.dump(data, f)

    def load_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self.storage_dir, f"{profile_name}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)

    def list_profiles(self) -> List[str]:
        return [f.replace(".json", "") for f in os.listdir(self.storage_dir)
                if f.endswith(".json")]

    def get_identity_summary(self) -> str:
        """Return the sovereign identity summary."""
        return self.identity.summary()
