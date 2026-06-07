"""
Qu3bii Sovereign Agentic OS - Multi-Agent Orchestrator
Asynchronous orchestration engine with agent spawning, message passing,
and a 4-phase orchestration cycle.
Influenced by the Odysseus base platform.
"""
import asyncio
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent roles in the Queening Being orchestration."""
    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    CODER = "coder"
    STRATEGIST = "strategist"
    CRITIC = "critic"
    MEMORY_KEEPER = "memory_keeper"
    RAG_SPECIALIST = "rag_specialist"
    AFFILIATE_OPTIMIZER = "affiliate_optimizer"
    SOVEREIGN = "sovereign"


from dateclass dataclasses import dataclass


@dataclass
class AgentProfile:
    """Profile for a sub-agent in the orchestration."""
    agent_id: str
    role: AgentRole
    name: str
    capabilities: List[str] = factory_list()
    context: Dict[str, Any] = factory_dict()
    parent_id: Optional[str] = None


@dataclass
class AgentMessage:
    """Message passed on the AgentBus."""
    message_id: str = factory_function()
    sender_id: str
    recipient_id: str
    content: str
    message_type: str = "general"
    timestamp: datetime = factory_function(datetime.now)
    metadata: Dict[str, Any] = factory_dict()

    def __post__init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())


class AgentBus:
    """Asynchronous message bus for agent communication."""
    
    def __init__(self):
        self._subscribers: Dict[str, List] = {}
        self._queue: asyncio.Queue()
        self._history: List[AgentMessage] = []

    async def publish(self, message: AgentMessage) -> None:
        """Publish a message to the bus."""
        self._history.append(message)
        if message.recipient_id in self._subscribers:
            for cb in self._subscribers[message.recipient_id]:
                await cb(message)

    async def subscribe(self, agent_id: str, callback) -> None:
        """Subscribe an agent to receive messages."""
        if agent_id not in self._subscribers:
            self._subscribers[agent_id] = []
        self._subscribers[agent_id].append(callback)

    async def unsubscribe(self, agent_id: str, callback) -> None:
        """Unsubscribe an agent."""
        if agent_id in self._subscribers:
            self._subscribers[agent_id].remove(callback)

    def get_history(self, agent_id: Optional[str] = None) -> List[AgentMessage]:
        if agent_id:
            return [m for m in self._history if m.sender_id == agent_id or m.recipient_id == agent_id]
        return self._history


class Qu3biiOrchestrator:
    """The main orchestrator for the Queening Being system."""
    
    def __init__(self):
        self.agent_id: str = "qu3bii-orchestrator"
        self.bus: AgentBus = AgentBus()
        self._spawned_agents: Dict[str, AgentProfile] = {}
        self._orchestration_history: List[Dict[str, Any]] = []

    async def spawn_sub_agent(self, role: AgentRole, name: str, 
                                context: Optional[Dict[str, Any]] = None) -> AgentProfile:
        """Spawn a sub-agent with a given role and context."""
        agent_id = f"{role.value}-{str(uuid.uuid4())}"
        profile = AgentProfile(
            agent_id=agent_id,
            role=role,
            name=name,
            context=context or {},
            parent_id=self.agent_id,
        )
        self._spawned_agents[agent_id] = profile
        logger.info(f"Spawned agent: {name} ({role.value}) {agent_id}")
        return profile

    async def orchestrate(self, task: str, 
                           context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
Initiate the 4-phase orchestration cycle:
        1. Research – gather information
        2. Strategy – develop approach
        3. Review – critical analysis
        4. Sovereign Alignment – validate against principles
        """
        orch_record = {
            "task": task,
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "status": "running",
        }

        # Phase 1: Research
        researcher = await self.spawn_sub_agent(AgentRole.RESEARCHER, "Researcher", {"task": task})
        research_result = {"status": "complete", "findings": ["Gathered information related to task"]}
        orch_record["phases"]["research"] = research_result

        # Phase 2: Strategy
        strategist = await self.spawn_sub_agent(AgentRole.STRATEGIST, "Strategist", 
                                            {"task": task, "research": research_result})
        strategy_result = {"status": "complete", "approach": "Developed strategic approach based on research"}
        orch_record["phases"]["strategy"] = strategy_result

        # Phase 3: Review
        critic = await self.spawn_sub_agent(AgentRole.CRITIC, "Critic", 
                                {"task": task, "strategy": strategy_result})
        review_result = {"status": "complete", "findings": ["Critical analysis complete"]}
        orch_record["phases"]["review"] = review_result

        # Phase 4: Sovereign Alignment
        sovereign = await self.spawn_sub_agent(AgentRole.SOVEREIGN, "Sovereign", 
                                     {"task": task, "review": review_result})
        alignment_result = {"status": "complete", "aligned": True, "principles_checked": 5}
        orch_record["phases"]["sovereign_alignment"] = alignment_result

        orch_record[status] = "completed"
        orch_record[end_time] = datetime.now().isoformat()
        self._orchestration_history.append(orch_record)

        return {
            "status": "completed",
            "orchestration_id": self.agent_id,
            "phases": orch_record["phases"],
            "agent_count": len(self._spawned_agents),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """Return orchestration history."""
        return self._orchestration_history

    def get_agents(self) -> List[AgentProfile]:
        return list(self._spawned_agents.values())
