import { OpenAIResponse, OpenAIMessage } from '@/lib/typhoon'

/**
 * Mock OpenAI API response builder
 */
export function createMockOpenAIResponse(content: string, model = 'gpt-5'): OpenAIResponse {
  return {
    id: 'chatcmpl-mock123',
    object: 'chat.completion',
    created: Date.now(),
    model,
    choices: [
      {
        index: 0,
        message: {
          role: 'assistant',
          content,
        },
        finish_reason: 'stop',
      },
    ],
    usage: {
      prompt_tokens: 100,
      completion_tokens: 50,
      total_tokens: 150,
    },
  }
}

/**
 * Mock fetch response for successful API calls to /api/typhoon
 * Returns the format expected by the client library: {response: string}
 */
export function mockSuccessfulFetch(content: string, model = 'gpt-5') {
  ;(global.fetch as jest.Mock).mockResolvedValueOnce({
    ok: true,
    status: 200,
    json: async () => ({ response: content }),
  })
}

/**
 * Mock fetch response for successful direct OpenAI API calls
 * Returns the full OpenAI response format
 */
export function mockSuccessfulOpenAIFetch(content: string, model = 'gpt-5') {
  const mockResponse = createMockOpenAIResponse(content, model)
  ;(global.fetch as jest.Mock).mockResolvedValueOnce({
    ok: true,
    status: 200,
    json: async () => mockResponse,
  })
}

/**
 * Mock fetch response for failed OpenAI API calls
 * For retryable errors (429, 500, 502, 503, 504), mocks 3 attempts to match retry logic
 */
export function mockFailedFetch(status: number, errorMessage: string) {
  const retryableStatuses = [408, 429, 500, 502, 503, 504]
  const isRetryable = retryableStatuses.includes(status)
  const attempts = isRetryable ? 3 : 1

  for (let i = 0; i < attempts; i++) {
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status,
      text: async () => JSON.stringify({ error: { message: errorMessage } }),
    })
  }
}

/**
 * Mock fetch response for network errors
 */
export function mockNetworkError(errorMessage = 'Network request failed') {
  ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error(errorMessage))
}

/**
 * Mock fetch response for timeout errors
 * Mocks 3 attempts to match retry logic for retryable errors
 */
export function mockTimeoutError() {
  const error = new DOMException('The operation was aborted', 'AbortError')
  for (let i = 0; i < 3; i++) {
    ;(global.fetch as jest.Mock).mockRejectedValueOnce(error)
  }
}

/**
 * Create a mock case generation response
 */
export function createMockCaseResponse() {
  const caseData = {
    case: {
      title: 'The Stolen Diamond',
      summary: 'A valuable diamond has been stolen from the museum',
      location: 'City Museum',
      date: '2025-01-15',
      time: '10:30 PM',
    },
    clues: [
      {
        id: 'clue1',
        description: 'Broken window glass',
        location: 'Display room',
        relevance: 'Point of entry',
        discovered: false,
      },
      {
        id: 'clue2',
        description: 'Muddy footprints',
        location: 'Hallway',
        relevance: 'Trail of suspect',
        discovered: false,
      },
    ],
    suspects: [
      {
        id: 'suspect1',
        name: 'John Smith',
        description: 'Museum security guard',
        background: 'Worked at museum for 5 years',
        motive: 'Financial troubles',
        alibi: 'Claims to be on patrol',
        isGuilty: true,
      },
      {
        id: 'suspect2',
        name: 'Jane Doe',
        description: 'Museum curator',
        background: 'Art history professor',
        motive: 'None apparent',
        alibi: 'At home sleeping',
        isGuilty: false,
      },
    ],
    solution: {
      culpritId: 'suspect1',
      narrative: 'John Smith used his access to bypass security',
      keyEvidence: ['clue1', 'clue2'],
    },
  }

  return JSON.stringify(caseData)
}

/**
 * Create a mock suspect analysis response
 */
export function createMockSuspectAnalysisResponse() {
  const analysis = {
    suspectId: 'suspect1',
    trustworthiness: 45,
    inconsistencies: [
      'Alibi lacks specific details',
      'Nervous demeanor during questioning',
    ],
    connections: [
      {
        clueId: 'clue1',
        connectionType: 'direct',
        description: 'Has access to the area',
      },
    ],
    suggestedQuestions: [
      'Where exactly were you during the theft?',
      'Can anyone verify your alibi?',
    ],
  }

  return JSON.stringify(analysis)
}

/**
 * Create a mock clue analysis response
 */
export function createMockClueAnalysisResponse() {
  const analysis = {
    summary: 'This clue suggests forced entry through the window',
    connections: [
      {
        suspectId: 'suspect1',
        connectionType: 'direct',
        description: 'Has the physical ability to break the window',
      },
    ],
    nextSteps: [
      'Check for fingerprints on the glass',
      'Review security camera footage',
    ],
  }

  return JSON.stringify(analysis)
}

/**
 * Create a mock solution validation response
 */
export function createMockSolutionResponse(correct: boolean) {
  const solution = {
    solved: correct,
    correct,
    culpritId: 'suspect1',
    reasoning: correct
      ? 'Your deduction is correct based on the evidence'
      : 'The evidence does not fully support your conclusion',
    evidenceIds: ['clue1', 'clue2'],
    narrative: 'The suspect used insider knowledge to commit the crime',
  }

  return JSON.stringify(solution)
}

/**
 * Create a mock interview response
 */
export function createMockInterviewResponse(question: string) {
  return `I understand you're asking about "${question}". As I mentioned, I was on my regular patrol route that evening.`
}

/**
 * Create a mock translation response
 */
export function createMockTranslationResponse(originalText: string, targetLang: string) {
  if (targetLang === 'th') {
    return 'ข้อความแปลเป็นภาษาไทย'
  }
  return 'Translated text to English'
}

/**
 * Helper to verify fetch was called with correct parameters
 */
export function expectFetchCalledWith(
  url: string,
  messages: OpenAIMessage[],
  model?: string,
  temperature?: number,
  maxTokens?: number
) {
  expect(global.fetch).toHaveBeenCalledWith(
    url,
    expect.objectContaining({
      method: 'POST',
      headers: expect.objectContaining({
        'Content-Type': 'application/json',
        'Authorization': expect.stringContaining('Bearer'),
      }),
      body: expect.stringContaining(messages[0].content),
    })
  )
}
