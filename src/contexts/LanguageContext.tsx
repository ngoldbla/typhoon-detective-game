'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

type Language = 'en';

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Translation dictionaries
const translations: Record<Language, Record<string, string>> = {
    en: {
        // Common
        'app.title': 'Emerson\'s Detective',
        'app.subtitle': 'Solve the case!',
        'app.loading': 'Loading...',
        'app.error': 'An error occurred',

        // Error messages
        'error.page_not_found': "We couldn't find the page you're looking for.",
        'error.return_home': 'Return to home page',

        // Progress indicators
        'progress.discovery': 'Discovery',
        'progress.analysis': 'Analysis',
        'progress.interview': 'Interview',
        'progress.solution': 'Solution',
        'progress.just_started': 'Just started',
        'progress.investigating': 'Investigating',
        'progress.making_progress': 'Making progress',
        'progress.almost_there': 'Almost there',
        'progress.complete': 'Complete',

        // Button labels
        'button.submit': 'Submit',
        'button.cancel': 'Cancel',
        'button.confirm': 'Confirm',
        'button.save': 'Save',
        'button.delete': 'Delete',
        'button.back': 'Back',
        'button.next': 'Next',
        'button.continue': 'Continue',
        'button.try_again': 'Try Again',
        'button.collect': 'Collect',
        'button.analyze': 'Analyze',
        'button.examine': 'Examine',
        'button.interview': 'Interview',
        'button.search': 'Search',
        'button.filter': 'Filter',

        // Navigation
        'nav.home': 'Home',
        'nav.cases': 'Cases',
        'nav.clues': 'Clues',
        'nav.suspects': 'Suspects',
        'nav.settings': 'Settings',
        'nav.back': 'Back',
        'nav.howToPlay': 'How to Play',
        'nav.howItWorks': 'How It Works',

        // Game
        'game.start': 'Start Investigation',
        'game.continue': 'Continue Investigation',
        'game.new_case': 'New Case',
        'game.collect_clue': 'Collect Clue',
        'game.examine_evidence': 'Examine Evidence',
        'game.interview_suspect': 'Interview Suspect',
        'game.solve_case': 'Solve Case',
        'game.reset': 'Reset Game',
        'game.reset_confirm': 'Confirm Reset Game',
        'game.reset_warning': 'Warning: This will delete all your progress and start over with sample cases.',

        // How to Play
        'howToPlay.title': 'How to Play',
        'howToPlay.basics.title': 'How The Game Works',
        'howToPlay.clues.title': 'Finding Clues',
        'howToPlay.suspects.title': 'Talking to People',
        'howToPlay.deduction.title': 'Solving the Mystery',
        'howToPlay.tips.title': 'Tips to Help You Win',

        'howToPlay.basics.intro': 'Welcome! This is a fun game where you solve mysteries by finding clues and talking to people.',
        'howToPlay.basics.item1': 'Pick a mystery from the list',
        'howToPlay.basics.item2': 'Read about what happened',
        'howToPlay.basics.item3': 'Look for clues that help you figure it out',
        'howToPlay.basics.item4': 'Talk to people to learn more',
        'howToPlay.basics.item5': 'Guess who did it when you\'re ready!',

        'howToPlay.clues.intro': 'Clues help you solve the mystery! Look for them as you play.',
        'howToPlay.clues.item1': 'Read the story carefully',
        'howToPlay.clues.item2': 'Some clues are hidden - keep looking!',
        'howToPlay.clues.item3': 'Think about how clues fit together',
        'howToPlay.clues.item4': 'Check your clues often',

        'howToPlay.suspects.intro': 'Talking to people helps you learn what happened.',
        'howToPlay.suspects.item1': 'Think about what to ask',
        'howToPlay.suspects.item2': 'Listen to what they say',
        'howToPlay.suspects.item3': 'Use clues to ask better questions',
        'howToPlay.suspects.item4': 'Remember what each person tells you',

        'howToPlay.deduction.intro': 'When you think you know who did it, make your guess!',
        'howToPlay.deduction.item1': 'Pick the person you think did it',
        'howToPlay.deduction.item2': 'Choose clues that prove it',
        'howToPlay.deduction.item3': 'Tell us why they did it',
        'howToPlay.deduction.item4': 'If you\'re right, you win!',

        'howToPlay.tips.item1': 'Take your time',
        'howToPlay.tips.item2': 'Don\'t guess too fast',
        'howToPlay.tips.item3': 'Think about all the people before you pick',
        'howToPlay.tips.item4': 'Think about when things happened',
        'howToPlay.tips.item5': 'See how clues and stories fit together',
        'howToPlay.tips.item6': 'You can do it!',

        // How It Works
        'howItWorks.title': 'How It Works',
        'howItWorks.intro': 'Emerson\'s Detective Game uses advanced AI technology to create an immersive detective experience. Learn about the underlying technology and algorithms that power the game.',

        'howItWorks.typhoonLLM.title': 'AI Technology',
        'howItWorks.typhoonLLM.intro': 'The game is powered by Emerson\'s AI, a powerful large language model (LLM) designed for complex reasoning and creative content generation.',
        'howItWorks.typhoonLLM.item1': 'Emerson\'s AI handles natural language understanding and generation throughout the game',
        'howItWorks.typhoonLLM.item2': 'The model can process context-rich information to create coherent narratives',
        'howItWorks.typhoonLLM.item3': 'It utilizes advanced prompting techniques to maintain consistent game elements',
        'howItWorks.typhoonLLM.item4': 'The system uses different model variants optimized for different tasks',

        'howItWorks.caseGeneration.title': 'Dynamic Case Generation',
        'howItWorks.caseGeneration.intro': 'Each case in the game is uniquely generated using AI algorithms, creating endless possibilities for investigation.',
        'howItWorks.caseGeneration.item1': 'Cases are created by providing structured prompts to Emerson\'s AI',
        'howItWorks.caseGeneration.item2': 'The system ensures logical consistency between clues, suspects, and the solution',
        'howItWorks.caseGeneration.item3': 'Case parameters like theme, location, and difficulty level influence the generation process',
        'howItWorks.caseGeneration.item4': 'The AI generates case details, clue descriptions, suspect profiles, and a coherent solution',
        
        'howItWorks.clueAnalysis.title': 'Intelligent Clue Analysis',
        'howItWorks.clueAnalysis.intro': 'The game features a sophisticated clue analysis system that helps players investigate evidence.',
        'howItWorks.clueAnalysis.item1': 'Each clue is analyzed within the context of the current case and discovered evidence',
        'howItWorks.clueAnalysis.item2': 'The system identifies potential connections between clues and suspects',
        'howItWorks.clueAnalysis.item3': 'Analysis includes determining the significance of each piece of evidence',
        'howItWorks.clueAnalysis.item4': 'The AI suggests logical next investigative steps based on the current state of the case',
        
        'howItWorks.suspectInterviews.title': 'Dynamic Suspect Interviews',
        'howItWorks.suspectInterviews.intro': 'Interviews with suspects are powered by AI to create realistic and responsive questioning experiences.',
        'howItWorks.suspectInterviews.item1': 'Suspects respond based on their character profile, alibi, and relation to the case',
        'howItWorks.suspectInterviews.item2': 'The LLM maintains consistent character behavior throughout multiple interactions',
        'howItWorks.suspectInterviews.item3': 'Guilty suspects subtly behave differently than innocent ones, providing challenge for players',
        'howItWorks.suspectInterviews.item4': 'The system analyzes interview history to generate coherent follow-up responses',
        
        'howItWorks.caseSolving.title': 'Adaptive Solution Evaluation',
        'howItWorks.caseSolving.intro': 'The game evaluates player solutions using a comprehensive reasoning system.',
        'howItWorks.caseSolving.item1': 'The AI assesses whether the player correctly identified the culprit',
        'howItWorks.caseSolving.item2': 'It evaluates how well the selected evidence supports the player\'s reasoning',
        'howItWorks.caseSolving.item3': 'The system checks the logical consistency of the proposed solution',
        'howItWorks.caseSolving.item4': 'Players receive detailed feedback based on their solution attempt',

        // Cases
        'case.difficulty': 'Difficulty',
        'case.easy': 'Easy',
        'case.medium': 'Medium',
        'case.hard': 'Hard',
        'case.location': 'Location',
        'case.date': 'Date',
        'case.time': 'Time',
        'case.clues': 'Clues',
        'case.suspects': 'Suspects',
        'case.solution': 'Solution',
        'case.solved': 'Case Solved!',
        'case.unsolved': 'Case Unsolved',
        'case.progress': 'Progress',
        'case.search_placeholder': 'Search cases',
        'case.not_found': 'No cases found',
        'case.try_different_search': 'Try a different search term or create a new case.',
        'case.create_first': 'Start by creating your first case.',

        // Clues
        'clue.title': 'Clue',
        'clue.location': 'Found at',
        'clue.type': 'Type',
        'clue.relevance': 'Relevance',
        'clue.physical': 'Physical',
        'clue.digital': 'Digital',
        'clue.testimonial': 'Testimonial',
        'clue.critical': 'Critical',
        'clue.important': 'Important',
        'clue.minor': 'Minor',
        'clue.examine': 'Examine Clue',
        'clue.analysis': 'Analysis',
        'clue.connections': 'Connections',
        'clue.next_steps': 'Next Steps',
        'clue.not_found': 'Clue Not Found',
        'clue.does_not_exist': 'The clue you are looking for does not exist.',
        'clue.analysis_failed': 'Failed to analyze the clue. Please try again.',
        'clue.analyze': 'Analyze Clue',
        'clue.significance': 'Significance',
        'clue.possibleConnections': 'Possible Connections',
        'clue.questions': 'Questions to Consider',
        'clue.relatedCase': 'Related Case',
        'clue.relatedSuspects': 'Related Suspects',
        'clue.description': 'Description',
        'clue.condition': 'Condition',
        'clue.keywords': 'Keywords',
        'nav.back_to_cases': 'Back to Cases',
        'case.view': 'View Case',
        'suspect.view': 'View Suspect',

        // Suspects
        'suspect.name': 'Name',
        'suspect.description': 'About Them',
        'suspect.background': 'What We Know',
        'suspect.motive': 'Why They Might Have Done It',
        'suspect.alibi': 'Their Story',
        'suspect.interview': 'Talk To Them',
        'suspect.ask_question': 'Ask a Question',
        'suspect.custom_question': 'Your Own Question',
        'suspect.suggested_questions': 'Questions You Could Ask',
        'suspect.trust_level': 'Can We Trust Them?',
        'suspect.inconsistencies': 'Things That Don\'t Match',

        // Case Solving
        'solve.title': 'Solve the Mystery',
        'solve.instructions': 'Pick who did it, choose clues that prove it, and explain why you think so',
        'solve.select_suspect': 'Who Do You Think Did It?',
        'solve.select_evidence': 'Pick Your Clues',
        'solve.reasoning': 'Why Do You Think So?',
        'solve.min_evidence': 'Pick at least 2 clues',
        'solve.min_reasoning': 'Tell us more about why you think this (at least 50 letters)',
        'solve.submit': 'Submit Your Answer',
        'solve.analyzing': 'Checking your answer...',
        'solve.success': 'Great job! You solved it!',
        'solve.failure': 'Not quite right. Try again!',
        'solve.return_to_case': 'Go Back to Mystery',

        // Settings
        'settings.language': 'Language',
        'settings.english': 'English',
        'settings.thai': 'Thai',
        'settings.theme': 'Theme',
        'settings.light': 'Light',
        'settings.dark': 'Dark',
        'settings.system': 'System',

        // Scene Investigation
        'scene.investigation': 'Scene Investigation',
        'scene.investigate': 'Investigate',
        'scene.instructions': 'Click on different areas of the scene to search for clues.',
        'scene.desk': 'Desk',
        'scene.window': 'Window',
        'scene.floor': 'Floor',
        'scene.bookshelf': 'Bookshelf',
        'scene.table': 'Table',
        'scene.found_clue': 'You found a clue!',
        'scene.clue_description': 'Examine this clue to learn more about the case.',
        'scene.nothing_found': 'You found nothing of interest here.',
        'scene.continue_search': 'Continue Searching',
        'case.does_not_exist': 'The case you are looking for does not exist.',
    }
};

export function LanguageProvider({ children }: { children: ReactNode }) {
    // Language is always English
    const [language, setLanguage] = useState<Language>('en');

    // Set document language on mount
    useEffect(() => {
        document.documentElement.lang = 'en';
    }, []);

    // Translation function
    const t = (key: string): string => {
        return translations[language][key] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
} 