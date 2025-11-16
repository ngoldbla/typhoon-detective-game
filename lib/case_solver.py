"""Case solution analysis using OpenAI"""

import json
import re
from typing import List, Dict, Any
from lib.types import Case, Suspect, Clue, CaseSolution
from lib.openai_client import fetch_openai_completion


# System prompts for solution analysis
CASE_SOLUTION_PROMPT_EN = """You are a brilliant detective evaluating a case solution.
Given details about a case, the evidence collected, and a proposed solution, evaluate whether:
1. The solution correctly identifies the culprit
2. The evidence supports the reasoning
3. The narrative is logical and consistent

Be fair but rigorous in your assessment."""

CASE_SOLUTION_PROMPT_TH = """คุณเป็นนักสืบผู้เชี่ยวชาญที่กำลังประเมินการแก้คดี
ประเมินอย่างยุติธรรมและอธิบายเหตุผล"""


def analyze_solution(
    case_data: Case,
    suspects: List[Suspect],
    clues: List[Clue],
    accused_suspect_id: str,
    evidence_ids: List[str],
    reasoning: str,
    language: str = 'en'
) -> CaseSolution:
    """Analyze a player's solution to a case

    Args:
        case_data: The case information
        suspects: List of suspects
        clues: List of clues
        accused_suspect_id: ID of accused suspect
        evidence_ids: IDs of evidence used
        reasoning: Player's reasoning
        language: Language code

    Returns:
        CaseSolution with verdict and feedback
    """
    # Find the accused suspect
    accused_suspect = next((s for s in suspects if s.id == accused_suspect_id), None)
    if not accused_suspect:
        raise ValueError("Accused suspect not found")

    # Find the guilty suspect
    guilty_suspect = next((s for s in suspects if s.isGuilty), None)
    if not guilty_suspect:
        raise ValueError("No guilty suspect found")

    # Get selected evidence
    selected_evidence = [c for c in clues if c.id in evidence_ids]

    # Choose prompt based on language
    system_prompt = CASE_SOLUTION_PROMPT_TH if language == 'th' else CASE_SOLUTION_PROMPT_EN

    # Create user prompt
    if language == 'th':
        user_prompt = f"""ข้อมูลคดี:
ชื่อคดี: {case_data.title}
คำอธิบาย: {case_data.description}

ผู้ต้องสงสัย:
{chr(10).join([f'- {s.name}: {s.description}' for s in suspects])}

หลักฐาน:
{chr(10).join([f'- {c.title}: {c.description}' for c in clues])}

คำตอบที่เสนอ:
ผู้ต้องสงสัย: {accused_suspect.name}
หลักฐาน: {', '.join([e.title for e in selected_evidence])}
เหตุผล: {reasoning}

ผู้กระทำผิดจริง: {guilty_suspect.name}

กรุณาประเมินคำตอบ"""
    else:
        user_prompt = f"""Case Information:
Title: {case_data.title}
Description: {case_data.description}

All Suspects:
{chr(10).join([f'- {s.name}: {s.description}' for s in suspects])}

Discovered Clues:
{chr(10).join([f'- {c.title}: {c.description}' for c in clues])}

Proposed Solution:
Accused Suspect: {accused_suspect.name}
Evidence Used: {', '.join([e.title for e in selected_evidence])}
Reasoning: {reasoning}

Actual Culprit: {guilty_suspect.name}

Please evaluate the proposed solution."""

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

        # Format the solution
        is_correct = accused_suspect.id == guilty_suspect.id
        return format_case_solution(
            parsed_data,
            accused_suspect_id,
            evidence_ids,
            reasoning,
            is_correct,
            language
        )

    except Exception as e:
        print(f"Solution analysis error: {e}")
        # Return fallback solution
        is_correct = accused_suspect.id == guilty_suspect.id
        return create_fallback_solution(
            accused_suspect_id,
            evidence_ids,
            reasoning,
            is_correct,
            language
        )


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
        return {"narrative": response}


def format_case_solution(
    data: Dict[str, Any],
    culprit_id: str,
    evidence_ids: List[str],
    reasoning: str,
    is_correct: bool,
    language: str
) -> CaseSolution:
    """Format raw solution data into CaseSolution structure"""
    narrative = data.get('narrative', data.get('explanation', data.get('description', '')))

    if not narrative:
        narrative = create_fallback_narrative(is_correct, language)

    return CaseSolution(
        solved=is_correct,
        culpritId=culprit_id,
        reasoning=reasoning,
        evidenceIds=evidence_ids,
        narrative=narrative
    )


def create_fallback_solution(
    culprit_id: str,
    evidence_ids: List[str],
    reasoning: str,
    is_correct: bool,
    language: str
) -> CaseSolution:
    """Create a fallback solution when API fails"""
    narrative = create_fallback_narrative(is_correct, language)

    return CaseSolution(
        solved=is_correct,
        culpritId=culprit_id,
        reasoning=reasoning,
        evidenceIds=evidence_ids,
        narrative=narrative
    )


def create_fallback_narrative(is_correct: bool, language: str) -> str:
    """Create fallback narrative based on correctness"""
    if language == 'th':
        if is_correct:
            return "การวิเคราะห์ของคุณถูกต้อง! คุณได้ระบุผู้กระทำผิดและมีเหตุผลที่ดี คุณแก้คดีสำเร็จแล้ว!"
        else:
            return "การวิเคราะห์ของคุณมีจุดที่น่าสนใจ แต่ผู้ต้องสงสัยที่คุณเลือกไม่ใช่ผู้กระทำผิดจริง ลองตรวจสอบหลักฐานอีกครั้ง"
    else:
        if is_correct:
            return "Your analysis is correct! You identified the true culprit and provided good reasoning. You successfully solved this case!"
        else:
            return "Your analysis has interesting points, but the suspect you chose is not the actual culprit. Try reviewing the evidence again and reconsider the other suspects."
