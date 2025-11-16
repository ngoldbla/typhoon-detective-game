"""
Sample question generator for suspect interviews.
Provides contextual question suggestions based on suspect information.
"""

from typing import List, Dict, Any


def get_sample_questions_for_suspect(suspect: Dict[str, Any], case: Dict[str, Any]) -> List[str]:
    """
    Generate contextual sample questions for interviewing a suspect.

    Args:
        suspect: Dictionary containing suspect information
        case: Dictionary containing case information

    Returns:
        List of suggested questions to ask the suspect
    """
    questions = []

    # Basic questions
    questions.append(f"Where were you when {case.get('title', 'the incident')} occurred?")
    questions.append("Can you tell me about your relationship with the victim?")

    # Questions based on alibi
    if suspect.get('alibi'):
        questions.append("Can anyone verify your alibi?")
        questions.append("What were you doing before and after the incident?")

    # Questions based on motive
    if suspect.get('motive'):
        questions.append("What do you know about the incident?")
        questions.append("Did you have any reason to be involved in this?")

    # Questions based on background
    if suspect.get('background'):
        questions.append(f"How long have you been at {case.get('location', 'this location')}?")
        questions.append("Have you noticed anything unusual recently?")

    # Specific probing questions
    questions.extend([
        "Is there anything you're not telling me?",
        "Have you seen or heard anything suspicious?",
        "Do you know anyone who might want this to happen?",
        "What's your opinion about the other suspects?",
        "Can you walk me through your activities that day?"
    ])

    # Add suspect-specific questions based on name/role
    name = suspect.get('name', '').lower()

    # Teacher-specific
    if any(word in name for word in ['teacher', 'mr.', 'ms.', 'mrs.', 'professor']):
        questions.append("How well do you know your students?")
        questions.append("Have you noticed any behavioral changes in anyone?")

    # Student-specific
    if any(word in name for word in ['student', 'kid', 'child']):
        questions.append("Do you get along with your classmates?")
        questions.append("Have you been having any problems at school?")

    # Staff-specific
    if any(word in name for word in ['janitor', 'custodian', 'guard', 'security', 'cook', 'chef']):
        questions.append("Do you have access to all areas?")
        questions.append("What do you usually see during your rounds?")

    # Return unique questions (in case of duplicates)
    return list(dict.fromkeys(questions))[:8]  # Limit to 8 questions
