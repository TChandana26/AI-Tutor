from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid

# ── 1. PDF Document ──────────────────────────────────
@dataclass
class PDFDocument:
    filename:     str
    filepath:     str
    text_content: str
    pages:        int
    doc_id:       str  = field(default_factory=lambda: str(uuid.uuid4()))
    uploaded_at:  str  = field(default_factory=lambda: datetime.now().isoformat())

# ── 2. Chat Message ──────────────────────────────────
@dataclass
class ChatMessage:
    role:        str          # "user" or "assistant"
    content:     str
    tts_enabled: bool         = False
    message_id:  str          = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp:   str          = field(default_factory=lambda: datetime.now().isoformat())

# ── 3. Chat Session ──────────────────────────────────
@dataclass
class ChatSession:
    document:   PDFDocument
    messages:   List[ChatMessage] = field(default_factory=list)
    active:     bool              = True
    session_id: str               = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str               = field(default_factory=lambda: datetime.now().isoformat())

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

# ── 4. AI Request ────────────────────────────────────
@dataclass
class AIRequest:
    question:   str
    context:    str
    model:      str  = "gemini-pro"
    max_tokens: int  = 512
    answer:     str  = ""