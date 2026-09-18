"""Conversational State Machine and Multi-Turn Memory for Darukaa.Earth."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from darukaa.engine.metrics import EnvironmentalState


class ConversationTurn(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str = Field(description="'user' or 'assistant'")
    content: str
    extracted_params: dict[str, Any] = Field(default_factory=dict)
    clarifying_questions: list[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class DialogueSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    turns: list[ConversationTurn] = Field(default_factory=list)
    accumulated_state: EnvironmentalState = Field(default_factory=EnvironmentalState)
    pending_clarifications: list[str] = Field(default_factory=list)
    diagnostic_count: int = 0

    def add_user_turn(
        self, content: str, extracted_params: dict[str, Any]
    ) -> ConversationTurn:
        turn = ConversationTurn(
            role="user",
            content=content,
            extracted_params=extracted_params,
        )
        self.turns.append(turn)
        return turn

    def add_assistant_turn(
        self,
        content: str,
        clarifying_questions: list[str] | None = None,
    ) -> ConversationTurn:
        turn = ConversationTurn(
            role="assistant",
            content=content,
            clarifying_questions=clarifying_questions or [],
        )
        self.turns.append(turn)
        return turn

    def is_diagnostic_ready(self) -> bool:
        """Determines if enough environmental dimensions (at least 3) are populated."""
        return self.accumulated_state.count_active_variables() >= 3


class SessionStore:
    """In-memory thread-safe session manager."""

    def __init__(self) -> None:
        self._sessions: dict[str, DialogueSession] = {}

    def get_or_create(self, session_id: str | None = None) -> DialogueSession:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]

        new_session = DialogueSession(session_id=session_id or str(uuid.uuid4()))
        self._sessions[new_session.session_id] = new_session
        return new_session

    def get(self, session_id: str) -> DialogueSession | None:
        return self._sessions.get(session_id)

    def reset(self, session_id: str) -> DialogueSession:
        new_session = DialogueSession(session_id=session_id)
        self._sessions[session_id] = new_session
        return new_session
