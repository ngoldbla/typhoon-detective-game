'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { FaArrowLeft, FaCheck, FaTimes, FaExclamationTriangle, FaMedal } from 'react-icons/fa';
import Layout from '@/components/Layout';
import Button from '@/components/Button';
import AIDisclaimer from '@/components/AIDisclaimer';
import { useLanguage } from '@/contexts/LanguageContext';
import { useGame } from '@/contexts/GameContext';
import { useTyphoon } from '@/hooks/useTyphoon';
import { OpenAIMessage } from '@/lib/typhoon';
import { CaseSolution } from '@/types/game';

interface SolveCasePageProps {
    params: Promise<{
        id: string;
    }>;
}

export default function SolveCasePage({ params }: SolveCasePageProps) {
    const router = useRouter();
    const { language } = useLanguage();
    const { state, dispatch } = useGame();
    const { cases, clues, suspects, gameState } = state;
    const { sendMessage, loading: isAnalyzing } = useTyphoon();

    const [selectedSuspect, setSelectedSuspect] = useState<string | null>(null);
    const [selectedClues, setSelectedClues] = useState<string[]>([]);
    const [reasoning, setReasoning] = useState('');
    const [solution, setSolution] = useState<CaseSolution | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [caseId, setCaseId] = useState<string>('');
    const redirectActionDispatched = useRef(false);

    // Update params.id to use state with async/await approach
    useEffect(() => {
        const fetchCaseId = async () => {
            setCaseId((await params).id);
        };
        fetchCaseId();
    }, [params]);

    // Find the case by ID
    const caseData = cases.find(c => c.id === caseId);

    // Get related clues and suspects
    const caseClues = clues.filter(c => c.caseId === caseId);
    const caseSuspects = suspects.filter(s => s.caseId === caseId);

    // Filter to include both discovered and examined clues
    const discoveredClues = caseClues.filter(c => gameState.discoveredClues.includes(c.id));
    const examinedClues = caseClues.filter(c => gameState.examinedClues.includes(c.id));
    const availableClues = [...examinedClues];

    // Add any discovered clues that aren't already examined
    discoveredClues.forEach(clue => {
        if (!examinedClues.some(c => c.id === clue.id)) {
            availableClues.push(clue);
        }
    });

    // Get interviewed suspects
    const interviewedSuspects = caseSuspects.filter(s => gameState.interviewedSuspects.includes(s.id));

    // Always define this useEffect, but conditionally check inside it
    useEffect(() => {
        if (caseData?.solved && !redirectActionDispatched.current) {
            redirectActionDispatched.current = true;
            router.push(`/cases/${caseId}`);
        }
    }, [caseData?.solved, caseId, router]);

    // Toggle clue selection
    const toggleClueSelection = (clueId: string) => {
        setSelectedClues(prev =>
            prev.includes(clueId)
                ? prev.filter(id => id !== clueId)
                : [...prev, clueId]
        );
    };

    // Handle solving the case
    const handleSolveCase = async () => {
        // Validation checks
        if (!selectedSuspect) {
            setError('You must select a suspect as the culprit.');
            return;
        }

        if (selectedClues.length < 2) {
            setError('You must select at least 2 pieces of evidence to support your conclusion.');
            return;
        }

        if (reasoning.trim().length < 20) {
            setError('Please provide a more detailed reasoning for your conclusion.');
            return;
        }

        setIsSubmitting(true);
        setError(null);

        try {
            // Make sure caseData exists
            if (!caseData) {
                throw new Error('Case not found');
            }

            // Prepare data for LLM
            const selectedSuspectData = caseSuspects.find(s => s.id === selectedSuspect);
            const selectedCluesData = caseClues.filter(c => selectedClues.includes(c.id));

            if (!selectedSuspectData) {
                throw new Error('Selected suspect not found');
            }

            // Prepare the prompt for the LLM
            const systemPrompt = `You are helping a 7-year-old child check their answer in a mystery game. Use simple words kids can read. Be encouraging and friendly!
Correct answer: ${caseSuspects.find(s => s.isGuilty)?.name} did it
Look at the child's answer and tell them if they're right. Use simple words!`;

            const userPrompt = `Case: ${caseData.title}
Case Details: ${caseData.summary}

Player's Selected Suspect: ${selectedSuspectData.name}
Suspect Details: ${selectedSuspectData.description}
Background: ${selectedSuspectData.background}
Motive: ${selectedSuspectData.motive}
Alibi: ${selectedSuspectData.alibi}

Player's Selected Evidence:
${selectedCluesData.map(c => `- ${c.title}: ${c.description}`).join('\n')}

Player's Reasoning:
${reasoning}

Please analyze the player's solution and include this JSON format in your response:
\`\`\`json
{
  "solved": boolean, // whether the player correctly identified the culprit
  "culpritId": "string", // the ID of the actual culprit
  "reasoning": "string", // analysis of whether the player's reasoning is sound
  "evidenceIds": ["string"], // IDs of key evidence pieces linked to the culprit
  "narrative": "string" // a narrative summary of what actually happened in the case
}
\`\`\``;

            const messages: OpenAIMessage[] = [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userPrompt }
            ];

            // Get the response from the LLM
            const response = await sendMessage(messages);

            // Extract JSON solution
            const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/) ||
                response.match(/```([\s\S]*?)```/) ||
                response.match(/({[\s\S]*})/);

            if (jsonMatch) {
                const solution = JSON.parse(jsonMatch[1]) as CaseSolution;
                setSolution(solution);

                // Mark case as solved regardless of player's accuracy
                dispatch({ type: 'SOLVE_CASE', payload: caseId });
            } else {
                throw new Error('Could not parse solution from LLM response');
            }
        } catch (err) {
            console.error('Error solving case:', err);
            setError(language === 'en'
                ? 'Failed to analyze your solution. Please try again.'
                : 'การวิเคราะห์คำตอบล้มเหลว โปรดลองอีกครั้ง');
        } finally {
            setIsSubmitting(false);
        }
    };

    // Render "Case Not Found" if caseData is undefined
    if (!caseData) {
        return (
            <Layout>
                <div className="text-center py-12">
                    <h1 className="text-2xl font-bold mb-4">Case Not Found</h1>
                    <p className="mb-6">The case you are looking for does not exist.</p>
                    <Button
                        variant="primary"
                        onClick={() => router.push('/cases')}
                    >
                        Back to Cases
                    </Button>
                </div>
            </Layout>
        );
    }

    // Solution result page
    if (solution) {
        // Find the actual culprit
        const actualCulprit = caseSuspects.find(s => s.id === solution.culpritId);
        const isCorrect = solution.solved;

        return (
            <Layout title={`Case Solved: ${caseData.title}`}>
                <div className="mb-8">
                    <div className="flex items-center mb-6">
                        <button
                            onClick={() => router.push(`/cases/${caseId}`)}
                            className="mr-4 p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
                        >
                            <FaArrowLeft />
                        </button>
                        <h1 className="text-2xl font-bold">Case Conclusion</h1>
                    </div>

                    <AIDisclaimer className="mb-4" />

                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
                        <div className="text-center mb-8">
                            {isCorrect ? (
                                <div className="mb-6">
                                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-200 mb-4">
                                        <FaCheck size={32} />
                                    </div>
                                    <h2 className="text-2xl font-bold text-green-600 dark:text-green-200">You Got It Right!</h2>
                                    <p className="text-gray-600 dark:text-gray-400 mt-2">
                                        Great job! You solved the mystery!
                                    </p>
                                </div>
                            ) : (
                                <div className="mb-6">
                                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-200 mb-4">
                                        <FaTimes size={32} />
                                    </div>
                                    <h2 className="text-2xl font-bold text-red-600 dark:text-red-200">Not Quite Right</h2>
                                    <p className="text-gray-600 dark:text-gray-400 mt-2">
                                        That's okay! You can try again or see the answer.
                                    </p>
                                </div>
                            )}

                            <div className="max-w-lg mx-auto">
                                <div className="flex items-center bg-gray-100 dark:bg-gray-700 rounded-lg p-4 mb-4">
                                    <FaMedal className="text-accent mr-3" size={24} />
                                    <div>
                                        <div className="text-sm text-gray-600 dark:text-gray-400">Who did it:</div>
                                        <div className="font-bold">{actualCulprit?.name}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <h3 className="font-semibold text-xl mb-3">What Really Happened</h3>
                        <p className="whitespace-pre-wrap mb-6">{solution.narrative}</p>

                        <h3 className="font-semibold text-xl mb-3">About Your Answer</h3>
                        <p className="whitespace-pre-wrap mb-6">{solution.reasoning}</p>

                        <h3 className="font-semibold text-xl mb-3">Important Clues</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                            {solution.evidenceIds.map(id => {
                                const evidence = clues.find(c => c.id === id);
                                if (!evidence) return null;

                                return (
                                    <div key={id} className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                                        <h4 className="font-medium mb-1">{evidence.title}</h4>
                                        <p className="text-sm">{evidence.description.substring(0, 100)}...</p>
                                    </div>
                                );
                            })}
                        </div>

                        <div className="flex gap-4 mt-8">
                            <Button
                                variant="primary"
                                fullWidth
                                onClick={() => router.push(`/cases/${caseId}`)}
                            >
                                Back to Case
                            </Button>
                            <Button
                                variant="outline"
                                fullWidth
                                onClick={() => router.push('/cases')}
                            >
                                Browse Other Cases
                            </Button>
                        </div>
                    </div>
                </div>
            </Layout>
        );
    }

    // Check if enough evidence is available
    const hasEnoughEvidence =
        examinedClues.length >= Math.ceil(caseClues.length * 0.7) &&
        interviewedSuspects.length === caseSuspects.length;

    return (
        <Layout title={`Solve Case: ${caseData.title}`}>
            <div className="mb-8">
                {/* Header */}
                <div className="flex items-center mb-6">
                    <button
                        onClick={() => router.push(`/cases/${caseId}`)}
                        className="mr-4 p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
                    >
                        <FaArrowLeft />
                    </button>
                    <h1 className="text-2xl font-bold">Solve the Mystery</h1>
                </div>

                {!hasEnoughEvidence && (
                    <div className="bg-yellow-100 dark:bg-yellow-900 border-l-4 border-yellow-500 p-4 mb-6">
                        <div className="flex">
                            <FaExclamationTriangle className="text-yellow-600 dark:text-yellow-400 mt-0.5 mr-3" />
                            <div>
                                <h3 className="text-lg font-semibold text-yellow-800 dark:text-yellow-300">
                                    You Might Need More Clues
                                </h3>
                                <p className="text-yellow-700 dark:text-yellow-200">
                                    You haven't looked at all the clues or talked to everyone yet.
                                    Finding more clues will help you solve this mystery!
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 space-y-6">
                        {/* Case summary */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h2 className="text-xl font-semibold mb-4">About This Mystery</h2>
                            <p className="mb-4">{caseData.summary}</p>
                            <div className="grid grid-cols-2 gap-x-4 gap-y-2">
                                <span className="text-gray-600 dark:text-gray-400">Where:</span>
                                <span>{caseData.location}</span>
                                <span className="text-gray-600 dark:text-gray-400">When:</span>
                                <span>{new Date(caseData.dateTime).toLocaleString()}</span>
                            </div>
                        </div>

                        {/* Select the culprit */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h2 className="text-xl font-semibold mb-4">Who Do You Think Did It?</h2>
                            <p className="mb-4">Pick the person you think did it:</p>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                                {caseSuspects.map(suspect => (
                                    <div
                                        key={suspect.id}
                                        className={`p-4 rounded-lg cursor-pointer border-2 transition-colors ${selectedSuspect === suspect.id
                                            ? 'border-accent bg-accent/10'
                                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                                            }`}
                                        onClick={() => setSelectedSuspect(suspect.id)}
                                    >
                                        <div className="font-semibold mb-1">{suspect.name}</div>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            {suspect.description.substring(0, 100)}...
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Select evidence */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h2 className="text-xl font-semibold mb-4">Pick Your Clues</h2>
                            <p className="mb-4">Pick the clues that show this person did it:</p>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                                {availableClues.map(clue => (
                                    <div
                                        key={clue.id}
                                        className={`p-4 rounded-lg cursor-pointer border-2 transition-colors ${selectedClues.includes(clue.id)
                                            ? 'border-accent bg-accent/10'
                                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                                            }`}
                                        onClick={() => toggleClueSelection(clue.id)}
                                    >
                                        <div className="font-semibold mb-1">{clue.title}</div>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            {clue.description.substring(0, 100)}...
                                        </p>
                                    </div>
                                ))}
                            </div>

                            {availableClues.length === 0 && (
                                <div className="text-center py-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
                                    <p className="text-gray-600 dark:text-gray-400">
                                        You haven't examined any clues yet. Go back and examine some clues first.
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Reasoning */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h2 className="text-xl font-semibold mb-4">Why Do You Think So?</h2>
                            <p className="mb-4">Tell us why you think this person did it:</p>

                            <textarea
                                value={reasoning}
                                onChange={(e) => setReasoning(e.target.value)}
                                className="w-full h-40 p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-transparent"
                                placeholder="Write why you think this person did it. Tell us how the clues prove it."
                            />
                        </div>
                    </div>

                    {/* Side panel */}
                    <div className="space-y-6">
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h2 className="text-xl font-semibold mb-4">Case Solution</h2>
                            <p className="mb-6">
                                Once you've made your selections and provided your reasoning, submit your solution.
                                Our AI detective will analyze your conclusion and determine if you correctly solved the case.
                            </p>

                            <Button
                                variant="accent"
                                fullWidth
                                onClick={handleSolveCase}
                                isLoading={isSubmitting || isAnalyzing}
                                isDisabled={!selectedSuspect || selectedClues.length < 2 || reasoning.trim().length < 20}
                            >
                                {isSubmitting || isAnalyzing ? 'Analyzing...' : 'Submit Solution'}
                            </Button>

                            {error && (
                                <div className="mt-4 p-3 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-md">
                                    {error}
                                </div>
                            )}

                            {/* Requirements checklist */}
                            {!isSubmitting && !isAnalyzing && (
                                <div className="mt-4 text-sm">
                                    <p className="mb-2 text-gray-600 dark:text-gray-400">To submit your solution:</p>
                                    <ul className="space-y-1 pl-5 list-disc text-gray-600 dark:text-gray-400">
                                        <li className={selectedSuspect ? "text-green-600 dark:text-green-400" : ""}>
                                            Select a suspect as the culprit
                                        </li>
                                        <li className={selectedClues.length >= 2 ? "text-green-600 dark:text-green-400" : ""}>
                                            Select at least 2 pieces of evidence ({selectedClues.length}/2)
                                        </li>
                                        <li className={reasoning.trim().length >= 20 ? "text-green-600 dark:text-green-400" : ""}>
                                            Provide reasoning (at least 20 characters, current: {reasoning.trim().length})
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </div>

                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                            <h3 className="font-semibold text-lg mb-3">Your Selections</h3>

                            <div className="mb-4">
                                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Selected Culprit:</div>
                                {selectedSuspect ? (
                                    <div className="font-medium">
                                        {caseSuspects.find(s => s.id === selectedSuspect)?.name || 'None'}
                                    </div>
                                ) : (
                                    <div className="text-gray-500 italic">None selected</div>
                                )}
                            </div>

                            <div className="mb-4">
                                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                    Evidence Selected: {selectedClues.length}
                                </div>
                                {selectedClues.length > 0 ? (
                                    <ul className="list-disc list-inside text-sm">
                                        {selectedClues.map(id => (
                                            <li key={id}>
                                                {clues.find(c => c.id === id)?.title || 'Unknown Evidence'}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <div className="text-gray-500 italic">None selected</div>
                                )}
                            </div>

                            <div>
                                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Reasoning:</div>
                                {reasoning.trim() ? (
                                    <div className="text-sm">
                                        {reasoning.length > 100
                                            ? `${reasoning.substring(0, 100)}...`
                                            : reasoning}
                                    </div>
                                ) : (
                                    <div className="text-gray-500 italic">Not provided</div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
} 