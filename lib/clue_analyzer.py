"""Clue analysis using OpenAI"""

import json
import re
from typing import List, Dict, Any
from lib.types import Clue, Suspect, Case, ClueAnalysis, ClueAnalysisConnection
from lib.openai_client import fetch_openai_completion


# System prompts for clue analysis
CLUE_ANALYSIS_PROMPT_EN = """You are a helpful detective friend helping a 7-year-old child understand clues!

Use SIMPLE words that a 2nd or 3rd grader can read. Make it FUN and easy to understand!

Look at the clue and tell me:
1. What does this clue tell us? (Keep it simple!)
2. How does this clue connect to the people we're asking about?
3. What should we look at next? (Give simple steps)

Remember: Use SHORT sentences and EASY words that kids can read!

IMPORTANT: You must respond in valid JSON format with the following structure:
{
  "summary": "A simple explanation of what this clue means",
  "connections": [
    {
      "suspect": "Name of person",
      "connectionType": "How they're connected",
      "description": "How this clue connects to this person"
    }
  ],
  "nextSteps": [
    "First thing we should check next",
    "Second thing we should check next"
  ]
}"""

CLUE_ANALYSIS_PROMPT_TH = """คุณเป็นเพื่อนนักสืบที่ช่วยเด็กอายุ 7 ขวบทำความเข้าใจเบาะแส!

ใช้คำง่ายๆ ที่เด็กป.2-ป.3 อ่านได้ ทำให้สนุกและเข้าใจง่าย!

ตอบในรูปแบบ JSON"""


def analyze_clue(
    clue: Clue,
    suspects: List[Suspect],
    case_data: Case,
    discovered_clues: List[Clue],
    language: str = 'en'
) -> ClueAnalysis:
    """Analyze a clue in the context of a case

    Args:
        clue: The clue to analyze
        suspects: List of suspects
        case_data: The case information
        discovered_clues: Other discovered clues
        language: Language code ('en' or 'th')

    Returns:
        ClueAnalysis with summary, connections, and next steps
    """
    # Choose prompt based on language
    system_prompt = CLUE_ANALYSIS_PROMPT_TH if language == 'th' else CLUE_ANALYSIS_PROMPT_EN

    # Create user prompt
    if language == 'th':
        user_prompt = f"""ข้อมูลคดี:
ชื่อคดี: {case_data.title}
สรุป: {case_data.summary}
สถานที่: {case_data.location}

หลักฐานที่ต้องการวิเคราะห์:
ชื่อ: {clue.title}
คำอธิบาย: {clue.description}
สถานที่พบ: {clue.location}

ผู้ต้องสงสัย:
{chr(10).join([f'{s.name}: {s.description}' for s in suspects])}

กรุณาวิเคราะห์หลักฐานนี้"""
    else:
        user_prompt = f"""Case Information:
Title: {case_data.title}
Summary: {case_data.summary}
Location: {case_data.location}

Clue to Analyze:
Title: {clue.title}
Description: {clue.description}
Location Found: {clue.location}

Suspects:
{chr(10).join([f'{s.name}: {s.description}' for s in suspects])}

Please analyze this clue and provide connections to suspects."""

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
        return format_clue_analysis(parsed_data, suspects)

    except Exception as e:
        print(f"Clue analysis error: {e}")
        # Return fallback analysis
        return ClueAnalysis(
            summary="This is an important clue that can help solve the mystery.",
            connections=[],
            nextSteps=["Continue investigating", "Look for more clues"]
        )


def parse_json_response(response: str) -> Dict[str, Any]:
    """Parse JSON from OpenAI response"""
    # Try to extract JSON from markdown code blocks
    json_match = (
        re.search(r'```json\n([\s\S]*?)\n```', response) or
        re.search(r'```([\s\S]*?)```', response) or
        re.search(r'({[\s\S]*})', response)
    )

    json_content = json_match.group(1) if json_match else response

    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return empty structure
        return {"summary": response, "connections": [], "nextSteps": []}


def format_clue_analysis(data: Dict[str, Any], suspects: List[Suspect]) -> ClueAnalysis:
    """Format raw analysis data into ClueAnalysis structure"""
    summary = data.get('summary', 'No analysis available')

    # Process connections
    connections = []
    connections_data = data.get('connections', [])

    if isinstance(connections_data, list):
        for conn in connections_data:
            suspect_name = conn.get('suspect', conn.get('suspectName', ''))

            # Find matching suspect
            matched_suspect = next(
                (s for s in suspects if s.name.lower() in suspect_name.lower() or suspect_name.lower() in s.name.lower()),
                None
            )

            if matched_suspect:
                connections.append(ClueAnalysisConnection(
                    suspectId=matched_suspect.id,
                    connectionType=conn.get('connectionType', conn.get('type', 'related')),
                    description=conn.get('description', '')
                ))

    # Process next steps
    next_steps = data.get('nextSteps', [])
    if not isinstance(next_steps, list):
        next_steps = [next_steps] if next_steps else []

    if not next_steps:
        next_steps = ["Continue investigating"]

    return ClueAnalysis(
        summary=summary,
        connections=connections,
        nextSteps=next_steps
    )
