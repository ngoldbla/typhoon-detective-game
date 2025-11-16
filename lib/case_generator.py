"""Case generation using OpenAI"""

import json
import re
from typing import Dict, Any
from lib.types import Case, Clue, Suspect, GeneratedCase, CaseGenerationParams
from lib.openai_client import fetch_openai_completion
import uuid


# System prompts for case generation
CASE_GENERATION_PROMPT_EN = """You are creating fun detective stories for 7-year-old children (2nd/3rd grade reading level).

CRITICAL SAFETY RULES - YOU MUST FOLLOW THESE:
❌ NO violence, weapons, death, murder, or killing
❌ NO scary or frightening content
❌ NO adult themes (divorce, gambling, drugs, alcohol, etc.)
❌ NO harm to people or animals
✅ ONLY mysteries about: lost items, missing pets (that are found safe), harmless pranks, switched belongings, or simple school mysteries

LANGUAGE REQUIREMENTS:
- Use ONLY simple words a 7-year-old can read
- Keep sentences SHORT (under 15 words)
- Make it FUN and cheerful, not scary
- Use concrete, not abstract concepts

CREATE:
1. A fun mystery with a title, short summary, school/home location, and time
2. 4-6 simple clues that kids can understand
3. 3-4 suspects (other children, teachers, or friendly adults - NO criminals)
4. One suspect who did it (but they're not in trouble - just made a mistake or had good intentions)

EXAMPLE GOOD TOPICS:
- Missing cookie recipe
- Lost homework
- Switched lunch boxes
- Who drew on the chalkboard
- Missing class pet (found safely)
- Borrowed toy that wasn't returned

The mystery should be solvable by a 7-year-old using simple logic.
Respond in a structured JSON format that can be parsed by Python."""

CASE_GENERATION_PROMPT_TH = """คุณกำลังสร้างเรื่องสืบสวนสนุกๆ สำหรับเด็กอายุ 7 ขวบ (ระดับชั้นประถมศึกษาปีที่ 2-3)

กฎความปลอดภัยสำคัญ - คุณต้องปฏิบัติตาม:
❌ ห้ามมีความรุนแรง อาวุธ การตาย การฆาตกรรม
❌ ห้ามมีเนื้อหาที่น่ากลัวหรือน่าตกใจ
❌ ห้ามมีเนื้อหาสำหรับผู้ใหญ่
❌ ห้ามทำร้ายคนหรือสัตว์
✅ เฉพาะปริศนาเกี่ยวกับ: ของหาย สัตว์เลี้ยงหาย ปริศนาง่ายๆ

ตอบในรูปแบบ JSON ที่มีโครงสร้าง"""


# Fallback case for when API fails
FALLBACK_CASE = {
    "case": {
        "title": "The Missing Backpack",
        "description": "Alex's backpack is missing from the classroom! It has a special dinosaur patch on it.",
        "summary": "Help find Alex's backpack with the dinosaur patch.",
        "difficulty": "easy",
        "location": "Elementary School Classroom"
    },
    "clues": [
        {
            "title": "Empty Hook",
            "description": "Alex's hook is empty. The hook next to it has two backpacks on it.",
            "location": "Coat Room",
            "type": "physical",
            "relevance": "critical"
        }
    ],
    "suspects": [
        {
            "name": "Jamie",
            "description": "A student who also has a blue backpack",
            "background": "Jamie's backpack looks just like Alex's.",
            "motive": "Jamie took the wrong backpack by mistake.",
            "alibi": "Jamie says they grabbed their own backpack.",
            "isGuilty": True
        }
    ],
    "solution": "Jamie took the wrong backpack by mistake!"
}


def generate_case(params: CaseGenerationParams) -> GeneratedCase:
    """Generate a detective case using OpenAI

    Args:
        params: Case generation parameters

    Returns:
        A generated case with clues and suspects
    """
    try:
        # Choose prompt based on language
        system_prompt = CASE_GENERATION_PROMPT_TH if params.language == 'th' else CASE_GENERATION_PROMPT_EN

        # Create user prompt
        if params.language == 'th':
            user_prompt = f"สร้างคดีสืบสวนที่มีความยาก {params.difficulty}"
        else:
            user_prompt = f"Create a {params.difficulty} difficulty detective case"

        if params.theme and params.theme != 'random':
            user_prompt += f" with a {params.theme} theme" if params.language == 'en' else f" ในธีม {params.theme}"

        if params.location:
            user_prompt += f" set in {params.location}" if params.language == 'en' else f" ที่เกิดขึ้นใน {params.location}"

        if params.era:
            user_prompt += f" during the {params.era} era" if params.language == 'en' else f" ในยุค {params.era}"

        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Call OpenAI API
        response = fetch_openai_completion(
            messages,
            temperature=0.7,
            max_tokens=8192
        )

        # Parse JSON response
        parsed_data = parse_json_response(response)

        # Format into our data structure
        return format_generated_case(parsed_data, params.language)

    except Exception as e:
        print(f"Case generation error: {e}")
        # Return fallback case
        return format_generated_case(FALLBACK_CASE, params.language)


def parse_json_response(response: str) -> Dict[str, Any]:
    """Parse JSON from OpenAI response

    Args:
        response: Raw response text

    Returns:
        Parsed JSON data
    """
    # Try to extract JSON from markdown code blocks
    json_match = (
        re.search(r'```json\n([\s\S]*?)\n```', response) or
        re.search(r'```([\s\S]*?)```', response) or
        re.search(r'({[\s\S]*})', response)
    )

    json_content = json_match.group(1) if json_match else response

    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw response: {response}")
        raise ValueError("Failed to parse the generated case data")


def format_generated_case(data: Dict[str, Any], language: str) -> GeneratedCase:
    """Format raw LLM output into GeneratedCase structure

    Args:
        data: Raw parsed JSON data
        language: Language code

    Returns:
        Formatted GeneratedCase
    """
    # Extract case data
    case_data = data.get('case', data.get('case_details', {}))

    case = Case(
        id=str(uuid.uuid4()),
        title=case_data.get('title', data.get('title', 'Untitled Case')),
        description=case_data.get('description', data.get('description', '')),
        summary=case_data.get('summary', data.get('summary', '')),
        difficulty=case_data.get('difficulty', data.get('difficulty', 'medium')),
        solved=False,
        location=case_data.get('location', data.get('location', '')),
        dateTime=case_data.get('dateTime', data.get('dateTime', '')),
        imageUrl="/case-file.png",
        isLLMGenerated=True
    )

    # Extract clues
    clues_data = data.get('clues', data.get('evidence', []))
    clues = []
    for clue_dict in clues_data:
        clue = Clue(
            id=str(uuid.uuid4()),
            caseId=case.id,
            title=clue_dict.get('title', clue_dict.get('item', 'Untitled Clue')),
            description=clue_dict.get('description', ''),
            location=clue_dict.get('location', clue_dict.get('position_found', '')),
            type=clue_dict.get('type', 'physical'),
            discovered=False,
            examined=False,
            relevance=clue_dict.get('relevance', clue_dict.get('significance', 'important'))
        )
        clues.append(clue)

    # Extract suspects
    suspects_data = data.get('suspects', [])
    suspects = []
    for suspect_dict in suspects_data:
        suspect = Suspect(
            id=str(uuid.uuid4()),
            caseId=case.id,
            name=suspect_dict.get('name', 'Unknown Suspect'),
            description=suspect_dict.get('description', ''),
            background=suspect_dict.get('background', ''),
            motive=suspect_dict.get('motive', ''),
            alibi=suspect_dict.get('alibi', ''),
            isGuilty=suspect_dict.get('isGuilty', False),
            interviewed=False
        )
        suspects.append(suspect)

    # Find guilty suspect from solution
    solution_data = data.get('solution', '')
    solution_text = solution_data if isinstance(solution_data, str) else solution_data.get('reasoning', '')

    # Ensure at least one suspect is guilty
    if suspects and not any(s.isGuilty for s in suspects):
        suspects[0].isGuilty = True

    return GeneratedCase(
        case=case,
        clues=clues,
        suspects=suspects,
        solution=solution_text
    )
