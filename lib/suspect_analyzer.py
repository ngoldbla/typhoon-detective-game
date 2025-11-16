"""Suspect analysis and interview using OpenAI"""

import json
import re
from typing import List, Dict, Any, Optional
from lib.types import Suspect, Clue, Case, Interview, SuspectAnalysis, SuspectAnalysisConnection
from lib.openai_client import fetch_openai_completion


# System prompts for suspect analysis
SUSPECT_ANALYSIS_PROMPT_EN = """You are helping a 7-year-old child solve a fun mystery!
Look at this person and the clues to help figure out what happened.

Remember: Use SIMPLE words a 2nd or 3rd grader can read. Keep it FUN and friendly!

Tell me:
1. Can we believe what this person says? (Give a number from 0 to 100)
2. Are there things that don't match up?
3. Which clues connect to this person?
4. What questions should we ask next?

Respond in valid JSON format."""

SUSPECT_ANALYSIS_PROMPT_TH = """คุณกำลังช่วยเด็กอายุ 7 ขวบแก้ปริศนาสนุกๆ!
ดูคนนี้และเบาะแส

ตอบในรูปแบบ JSON"""


def analyze_suspect(
    suspect: Suspect,
    clues: List[Clue],
    case_data: Case,
    interview: Optional[Interview] = None,
    language: str = 'en'
) -> SuspectAnalysis:
    """Analyze a suspect in the context of a case

    Args:
        suspect: The suspect to analyze
        clues: List of discovered clues
        case_data: The case information
        interview: Optional interview data
        language: Language code

    Returns:
        SuspectAnalysis with trustworthiness, inconsistencies, etc.
    """
    # Choose prompt based on language
    system_prompt = SUSPECT_ANALYSIS_PROMPT_TH if language == 'th' else SUSPECT_ANALYSIS_PROMPT_EN

    # Create user prompt
    if language == 'th':
        user_prompt = f"""ข้อมูลคดี:
ชื่อคดี: {case_data.title}
สรุป: {case_data.summary}

ผู้ต้องสงสัย:
ชื่อ: {suspect.name}
คำอธิบาย: {suspect.description}
ประวัติ: {suspect.background}
ข้ออ้าง: {suspect.alibi}

หลักฐาน:
{chr(10).join([f'{c.title}: {c.description}' for c in clues])}

กรุณาวิเคราะห์ผู้ต้องสงสัย"""
    else:
        user_prompt = f"""Case Information:
Title: {case_data.title}
Summary: {case_data.summary}

Suspect to Analyze:
Name: {suspect.name}
Description: {suspect.description}
Background: {suspect.background}
Alibi: {suspect.alibi}

Discovered Clues:
{chr(10).join([f'{c.title}: {c.description}' for c in clues])}

Please analyze this suspect."""

    # Add interview data if available
    if interview and any(q.asked for q in interview.questions):
        asked_questions = [q for q in interview.questions if q.asked]
        interview_text = chr(10).join([f"Q: {q.question}\nA: {q.answer}" for q in asked_questions])
        user_prompt += f"\n\nInterview Records:\n{interview_text}"

    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        # Call OpenAI API
        response = fetch_openai_completion(
            messages,
            temperature=0.7,
            max_tokens=2048
        )

        # Parse JSON response
        parsed_data = parse_json_response(response)

        # Format the analysis
        return format_suspect_analysis(parsed_data, clues, suspect.id)

    except Exception as e:
        print(f"Suspect analysis error: {e}")
        # Return fallback analysis
        return SuspectAnalysis(
            suspectId=suspect.id,
            trustworthiness=50,
            inconsistencies=[],
            connections=[],
            suggestedQuestions=["What were you doing?", "Did you see anything?"]
        )


def process_interview_question(
    question: str,
    suspect: Suspect,
    clues: List[Clue],
    case_data: Case,
    previous_questions: List[Dict[str, str]],
    language: str = 'en'
) -> str:
    """Process an interview question and generate a response

    Args:
        question: The question to ask
        suspect: The suspect being interviewed
        clues: List of clues
        case_data: Case information
        previous_questions: Previous Q&A pairs
        language: Language code

    Returns:
        The suspect's answer
    """
    # Create system prompt for the suspect's character
    if language == 'th':
        system_prompt = f"""คุณเป็น {suspect.name} ในเรื่อง "{case_data.title}"

ข้อมูลของคุณ:
- คำอธิบาย: {suspect.description}
- ประวัติ: {suspect.background}
- เรื่องราวของคุณ: {suspect.alibi}

{'- คุณทำสิ่งนี้จริง แต่คุณไม่ได้ตั้งใจทำผิด' if suspect.isGuilty else '- คุณไม่ได้ทำ'}

ตอบคำถามด้วยคำง่ายๆ ที่เด็ก 7 ขวบเข้าใจได้
ใช้ประโยคสั้นๆ (ไม่เกิน 15 คำ)
ตอบแค่ 2-3 ประโยค"""
    else:
        guilty_text = "- You DID do this thing, but you didn't mean to do anything wrong." if suspect.isGuilty else "- You DIDN'T do it."
        system_prompt = f"""You are {suspect.name} in the mystery "{case_data.title}".

Your information:
- Description: {suspect.description}
- Background: {suspect.background}
- Your story: {suspect.alibi}

{guilty_text}

Answer questions using simple words that a 7-year-old can understand.
Use SHORT sentences (under 15 words each).
Keep your answer to 2-3 sentences only."""

    # Prepare messages with conversation history
    messages = [{"role": "system", "content": system_prompt}]

    # Add previous Q&A
    for prev_q in previous_questions:
        messages.append({"role": "user", "content": prev_q['question']})
        messages.append({"role": "assistant", "content": prev_q['answer']})

    # Add current question
    messages.append({"role": "user", "content": question})

    # Get response
    response = fetch_openai_completion(
        messages,
        temperature=0.7,
        max_tokens=2048
    )

    return response


def parse_json_response(response: str) -> Dict[str, Any]:
    """Parse JSON from OpenAI response"""
    json_match = (
        re.search(r'```json\n([\s\S]*?)\n```', response) or
        re.search(r'```([\s\S]*?)```', response) or
        re.search(r'({[\s\S]*})', response)
    )

    json_content = json_match.group(1) if json_match else response

    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        return {
            "trustworthiness": 50,
            "inconsistencies": [],
            "connections": [],
            "suggestedQuestions": []
        }


def format_suspect_analysis(
    data: Dict[str, Any],
    clues: List[Clue],
    suspect_id: str
) -> SuspectAnalysis:
    """Format raw analysis data into SuspectAnalysis structure"""
    # Get trustworthiness
    trustworthiness = data.get('trustworthiness', 50)
    if isinstance(trustworthiness, str):
        try:
            trustworthiness = int(trustworthiness)
        except ValueError:
            trustworthiness = 50

    trustworthiness = max(0, min(100, trustworthiness))

    # Process inconsistencies
    inconsistencies = data.get('inconsistencies', [])
    if not isinstance(inconsistencies, list):
        inconsistencies = [inconsistencies] if inconsistencies else []

    # Process connections
    connections = []
    connections_data = data.get('connections', [])

    if isinstance(connections_data, list):
        for conn in connections_data:
            clue_title = conn.get('clue', conn.get('clueTitle', ''))

            # Find matching clue
            matched_clue = next(
                (c for c in clues if c.title.lower() in clue_title.lower() or clue_title.lower() in c.title.lower()),
                None
            )

            if matched_clue:
                connections.append(SuspectAnalysisConnection(
                    clueId=matched_clue.id,
                    connectionType=conn.get('type', conn.get('connectionType', 'related')),
                    description=conn.get('description', '')
                ))

    # Process suggested questions
    suggested_questions = data.get('suggestedQuestions', [])
    if not isinstance(suggested_questions, list):
        suggested_questions = [suggested_questions] if suggested_questions else []

    if not suggested_questions:
        suggested_questions = ["What were you doing?", "Did you see anything unusual?"]

    return SuspectAnalysis(
        suspectId=suspect_id,
        trustworthiness=trustworthiness,
        inconsistencies=inconsistencies,
        connections=connections,
        suggestedQuestions=suggested_questions
    )
