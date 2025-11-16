"""
Database module for persisting detective game data using SQLite.
Stores cases, clues, suspects, images, and user progress.
"""

import sqlite3
import json
import os
from typing import List, Dict, Optional, Any
from pathlib import Path
from contextlib import contextmanager

# Database file path - use /data volume on Railway, fallback to local for development
DB_PATH = os.getenv('DATABASE_PATH', '/data/detective_game.db')

# Ensure directory exists
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Initialize database with required tables"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Cases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                summary TEXT,
                difficulty TEXT DEFAULT 'medium',
                solved INTEGER DEFAULT 0,
                archived INTEGER DEFAULT 0,
                location TEXT,
                dateTime TEXT,
                imageUrl TEXT,
                isLLMGenerated INTEGER DEFAULT 0,
                solution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Clues table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clues (
                id TEXT PRIMARY KEY,
                caseId TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT,
                type TEXT DEFAULT 'physical',
                discovered INTEGER DEFAULT 1,
                examined INTEGER DEFAULT 0,
                relevance TEXT DEFAULT 'important',
                emoji TEXT DEFAULT '🔍',
                imageUrl TEXT,
                FOREIGN KEY (caseId) REFERENCES cases(id) ON DELETE CASCADE
            )
        """)

        # Suspects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suspects (
                id TEXT PRIMARY KEY,
                caseId TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                background TEXT,
                motive TEXT,
                alibi TEXT,
                isGuilty INTEGER DEFAULT 0,
                interviewed INTEGER DEFAULT 0,
                emoji TEXT DEFAULT '👤',
                imageUrl TEXT,
                FOREIGN KEY (caseId) REFERENCES cases(id) ON DELETE CASCADE
            )
        """)

        # Images table (store downloaded images as binary data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                url TEXT PRIMARY KEY,
                data BLOB NOT NULL,
                content_type TEXT DEFAULT 'image/png',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Clue analyses table (cache AI analyses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clue_analyses (
                clue_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                summary TEXT NOT NULL,
                connections TEXT,
                nextSteps TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
            )
        """)

        # Suspect interviews table (cache interview history)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suspect_interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suspect_id TEXT NOT NULL,
                case_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
            )
        """)

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clues_case ON clues(caseId)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_suspects_case ON suspects(caseId)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interviews_suspect ON suspect_interviews(suspect_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interviews_case ON suspect_interviews(case_id)")


# Initialize database on module import
init_database()


# ===== CASE FUNCTIONS =====

def save_case(case_data: Dict[str, Any]) -> str:
    """Save a complete case with clues and suspects"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Extract case, clues, suspects from the case_data
        case = case_data.get('case', {})
        clues = case_data.get('clues', [])
        suspects = case_data.get('suspects', [])
        solution = case_data.get('solution', '')

        # Insert case
        cursor.execute("""
            INSERT OR REPLACE INTO cases
            (id, title, description, summary, difficulty, solved, archived, location,
             dateTime, imageUrl, isLLMGenerated, solution)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case.get('id'),
            case.get('title'),
            case.get('description'),
            case.get('summary', ''),
            case.get('difficulty', 'medium'),
            1 if case.get('solved') else 0,
            1 if case.get('archived') else 0,
            case.get('location', ''),
            case.get('dateTime', ''),
            case.get('imageUrl', ''),
            1 if case.get('isLLMGenerated') else 0,
            solution
        ))

        # Insert clues
        for clue in clues:
            cursor.execute("""
                INSERT OR REPLACE INTO clues
                (id, caseId, title, description, location, type, discovered, examined,
                 relevance, emoji, imageUrl)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clue.get('id'),
                case.get('id'),
                clue.get('title'),
                clue.get('description'),
                clue.get('location', ''),
                clue.get('type', 'physical'),
                1 if clue.get('discovered', True) else 0,
                1 if clue.get('examined') else 0,
                clue.get('relevance', 'important'),
                clue.get('emoji', '🔍'),
                clue.get('imageUrl')
            ))

        # Insert suspects
        for suspect in suspects:
            cursor.execute("""
                INSERT OR REPLACE INTO suspects
                (id, caseId, name, description, background, motive, alibi, isGuilty,
                 interviewed, emoji, imageUrl)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                suspect.get('id'),
                case.get('id'),
                suspect.get('name'),
                suspect.get('description'),
                suspect.get('background', ''),
                suspect.get('motive', ''),
                suspect.get('alibi', ''),
                1 if suspect.get('isGuilty') else 0,
                1 if suspect.get('interviewed') else 0,
                suspect.get('emoji', '👤'),
                suspect.get('imageUrl')
            ))

        return case.get('id')


def get_all_cases() -> List[Dict[str, Any]]:
    """Get all cases from the database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM cases
            ORDER BY created_at DESC
        """)

        cases = []
        for row in cursor.fetchall():
            case = dict(row)
            # Convert integer booleans to actual booleans
            case['solved'] = bool(case['solved'])
            case['archived'] = bool(case['archived'])
            case['isLLMGenerated'] = bool(case['isLLMGenerated'])

            # Load clues and suspects
            case['clues'] = get_case_clues(case['id'])
            case['suspects'] = get_case_suspects(case['id'])

            cases.append(case)

        return cases


def get_case_by_id(case_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific case by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
        row = cursor.fetchone()

        if not row:
            return None

        case = dict(row)
        case['solved'] = bool(case['solved'])
        case['archived'] = bool(case['archived'])
        case['isLLMGenerated'] = bool(case['isLLMGenerated'])

        # Load clues and suspects
        case['clues'] = get_case_clues(case_id)
        case['suspects'] = get_case_suspects(case_id)

        return case


def get_case_clues(case_id: str) -> List[Dict[str, Any]]:
    """Get all clues for a case"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clues WHERE caseId = ?", (case_id,))

        clues = []
        for row in cursor.fetchall():
            clue = dict(row)
            clue['discovered'] = bool(clue['discovered'])
            clue['examined'] = bool(clue['examined'])
            clues.append(clue)

        return clues


def get_case_suspects(case_id: str) -> List[Dict[str, Any]]:
    """Get all suspects for a case"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suspects WHERE caseId = ?", (case_id,))

        suspects = []
        for row in cursor.fetchall():
            suspect = dict(row)
            suspect['isGuilty'] = bool(suspect['isGuilty'])
            suspect['interviewed'] = bool(suspect['interviewed'])
            suspects.append(suspect)

        return suspects


def update_case_status(case_id: str, solved: Optional[bool] = None, archived: Optional[bool] = None):
    """Update case status"""
    with get_db() as conn:
        cursor = conn.cursor()

        if solved is not None:
            cursor.execute("UPDATE cases SET solved = ? WHERE id = ?", (1 if solved else 0, case_id))

        if archived is not None:
            cursor.execute("UPDATE cases SET archived = ? WHERE id = ?", (1 if archived else 0, case_id))


def delete_case(case_id: str):
    """Delete a case and all related data"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Foreign key constraints will cascade the deletion
        cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))


# ===== CLUE FUNCTIONS =====

def get_examined_clues(case_id: str) -> List[str]:
    """Get list of examined clue IDs for a case"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clues WHERE caseId = ? AND examined = 1", (case_id,))
        return [row[0] for row in cursor.fetchall()]


def mark_clue_examined(clue_id: str):
    """Mark a clue as examined"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE clues SET examined = 1 WHERE id = ?", (clue_id,))


def save_clue_analysis(clue_id: str, case_id: str, analysis: Dict[str, Any]):
    """Save AI analysis of a clue"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO clue_analyses
            (clue_id, case_id, summary, connections, nextSteps)
            VALUES (?, ?, ?, ?, ?)
        """, (
            clue_id,
            case_id,
            analysis.get('summary', ''),
            json.dumps(analysis.get('connections', [])),
            json.dumps(analysis.get('nextSteps', []))
        ))


def get_clue_analysis(clue_id: str) -> Optional[Dict[str, Any]]:
    """Get cached analysis for a clue"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clue_analyses WHERE clue_id = ?", (clue_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return {
            'summary': row['summary'],
            'connections': json.loads(row['connections']),
            'nextSteps': json.loads(row['nextSteps'])
        }


# ===== SUSPECT FUNCTIONS =====

def get_interviewed_suspects(case_id: str) -> List[str]:
    """Get list of interviewed suspect IDs for a case"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM suspects WHERE caseId = ? AND interviewed = 1", (case_id,))
        return [row[0] for row in cursor.fetchall()]


def mark_suspect_interviewed(suspect_id: str):
    """Mark a suspect as interviewed"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE suspects SET interviewed = 1 WHERE id = ?", (suspect_id,))


def save_interview(suspect_id: str, case_id: str, question: str, answer: str):
    """Save an interview question and answer"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO suspect_interviews (suspect_id, case_id, question, answer)
            VALUES (?, ?, ?, ?)
        """, (suspect_id, case_id, question, answer))


def get_suspect_interviews(suspect_id: str) -> List[Dict[str, str]]:
    """Get all interview history for a suspect"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, answer, created_at
            FROM suspect_interviews
            WHERE suspect_id = ?
            ORDER BY created_at ASC
        """, (suspect_id,))

        return [
            {'question': row['question'], 'answer': row['answer']}
            for row in cursor.fetchall()
        ]


# ===== IMAGE FUNCTIONS =====

def save_image_data(url: str, data: bytes, content_type: str = 'image/png'):
    """Save image binary data to database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO images (url, data, content_type)
            VALUES (?, ?, ?)
        """, (url, data, content_type))


def get_image_data(url: str) -> Optional[Dict[str, Any]]:
    """Get image binary data from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data, content_type FROM images WHERE url = ?", (url,))
        row = cursor.fetchone()

        if not row:
            return None

        return {
            'data': row['data'],
            'content_type': row['content_type']
        }
