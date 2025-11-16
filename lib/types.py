"""Type definitions for the Emerson Detective Game"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Case:
    """Represents a detective case"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    summary: str = ""
    difficulty: str = "medium"
    solved: bool = False
    location: str = ""
    dateTime: str = field(default_factory=lambda: datetime.now().isoformat())
    imageUrl: str = "/case-file.png"
    isLLMGenerated: bool = False


@dataclass
class Clue:
    """Represents a clue in a case"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    caseId: str = ""
    title: str = ""
    description: str = ""
    location: str = ""
    type: str = "physical"
    discovered: bool = False
    examined: bool = False
    relevance: str = "important"
    emoji: str = "🔍"


@dataclass
class Suspect:
    """Represents a suspect in a case"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    caseId: str = ""
    name: str = ""
    description: str = ""
    background: str = ""
    motive: str = ""
    alibi: str = ""
    isGuilty: bool = False
    interviewed: bool = False
    emoji: str = "👤"


@dataclass
class InterviewQuestion:
    """Represents an interview question and answer"""
    question: str
    answer: str = ""
    asked: bool = False


@dataclass
class Interview:
    """Represents an interview with a suspect"""
    suspectId: str
    questions: List[InterviewQuestion] = field(default_factory=list)


@dataclass
class ClueAnalysisConnection:
    """Connection between a clue and a suspect"""
    suspectId: str
    connectionType: str
    description: str


@dataclass
class ClueAnalysis:
    """Analysis of a clue"""
    summary: str
    connections: List[ClueAnalysisConnection] = field(default_factory=list)
    nextSteps: List[str] = field(default_factory=list)


@dataclass
class SuspectAnalysisConnection:
    """Connection between a suspect and a clue"""
    clueId: str
    connectionType: str
    description: str


@dataclass
class SuspectAnalysis:
    """Analysis of a suspect"""
    suspectId: str
    trustworthiness: int
    inconsistencies: List[str] = field(default_factory=list)
    connections: List[SuspectAnalysisConnection] = field(default_factory=list)
    suggestedQuestions: List[str] = field(default_factory=list)


@dataclass
class CaseSolution:
    """Solution to a case"""
    solved: bool
    culpritId: str
    reasoning: str
    evidenceIds: List[str]
    narrative: str


@dataclass
class GeneratedCase:
    """A complete generated case with clues and suspects"""
    case: Case
    clues: List[Clue]
    suspects: List[Suspect]
    solution: str


@dataclass
class CaseGenerationParams:
    """Parameters for case generation"""
    difficulty: str = "easy"
    theme: str = "random"
    location: str = ""
    era: str = ""
    language: str = "en"
    custom_scenario: str = ""
