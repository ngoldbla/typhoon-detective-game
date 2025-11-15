import { generateCase } from '../caseGenerator'
import { mockSuccessfulFetch, createMockCaseResponse } from '@/test-utils/mockOpenAI'
import { CaseGenerationParams } from '@/types/game'

describe('generateCase', () => {
  const defaultParams: CaseGenerationParams = {
    difficulty: 'medium',
    language: 'en',
  }

  beforeEach(() => {
    jest.clearAllMocks()
    Object.defineProperty(window, 'location', {
      value: { origin: 'http://localhost:3000' },
      writable: true,
    })
  })

  describe('Successful Case Generation', () => {
    it('should generate a case with default parameters', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      expect(result).toBeDefined()
      expect(result.case).toBeDefined()
      expect(result.clues).toBeDefined()
      expect(result.suspects).toBeDefined()
      expect(result.case.id).toBeDefined()
      expect(result.case.isLLMGenerated).toBe(true)
    })

    it('should generate a case with all parameters', async () => {
      const params: CaseGenerationParams = {
        difficulty: 'hard',
        theme: 'noir',
        location: 'New York',
        era: '1920s',
        language: 'en',
      }

      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(params)

      expect(result).toBeDefined()
      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      const userPrompt = body.messages[1].content

      expect(userPrompt).toContain('hard')
      expect(userPrompt).toContain('noir')
      expect(userPrompt).toContain('New York')
      expect(userPrompt).toContain('1920s')
    })

    it('should use Thai language prompts when language is th', async () => {
      const params: CaseGenerationParams = {
        difficulty: 'easy',
        language: 'th',
      }

      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      await generateCase(params)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      const systemPrompt = body.messages[0].content

      expect(systemPrompt).toContain('คดีสืบสวน')
    })

    it('should correctly mark one suspect as guilty', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      const guiltySuspects = result.suspects.filter(s => s.isGuilty)
      expect(guiltySuspects.length).toBe(1)
      expect(guiltySuspects[0].id).toBeDefined()
    })

    it('should assign unique IDs to all entities', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      expect(result.case.id).toBeDefined()
      result.clues.forEach(clue => {
        expect(clue.id).toBeDefined()
        expect(clue.caseId).toBe(result.case.id)
      })
      result.suspects.forEach(suspect => {
        expect(suspect.id).toBeDefined()
        expect(suspect.caseId).toBe(result.case.id)
      })
    })

    it('should set all clues as not discovered initially', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      result.clues.forEach(clue => {
        expect(clue.discovered).toBe(false)
        expect(clue.examined).toBe(false)
      })
    })

    it('should set all suspects as not interviewed initially', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      result.suspects.forEach(suspect => {
        expect(suspect.interviewed).toBe(false)
      })
    })
  })

  describe('JSON Parsing', () => {
    it('should parse JSON wrapped in markdown code blocks', async () => {
      const caseData = JSON.parse(createMockCaseResponse())
      const markdownResponse = '```json\n' + JSON.stringify(caseData) + '\n```'

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: markdownResponse }),
      })

      const result = await generateCase(defaultParams)

      expect(result).toBeDefined()
      expect(result.case.title).toBe('The Stolen Diamond')
    })

    it('should parse JSON without code blocks', async () => {
      const mockResponse = createMockCaseResponse()

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      const result = await generateCase(defaultParams)

      expect(result).toBeDefined()
      expect(result.case.title).toBe('The Stolen Diamond')
    })

    it('should handle alternative field names in response', async () => {
      const alternativeFormat = JSON.stringify({
        case_details: {
          title: 'Alternative Case',
          synopsis: 'Alternative description',
          location: 'Alternative location',
          date: '2025-01-15',
          time: '10:30 PM',
        },
        evidence: [
          {
            item: 'Broken window',
            description: 'Evidence description',
            position_found: 'Display room',
            significance: 'High',
          },
        ],
        suspects: [
          {
            name: 'John Doe',
            description: 'Suspect description',
            background: 'Background info',
            motive: 'Motive',
            alibi: 'Alibi',
            isGuilty: true,
          },
        ],
        solution: {
          culprit: 'John Doe',
          reasoning: 'Solution reasoning',
        },
      })

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: alternativeFormat }),
      })

      const result = await generateCase(defaultParams)

      expect(result.case.title).toBe('Alternative Case')
      expect(result.case.summary).toBe('Alternative description')
      expect(result.clues[0].title).toBe('Broken window')
      expect(result.suspects[0].name).toBe('John Doe')
      expect(result.suspects[0].isGuilty).toBe(true)
    })
  })

  describe('Error Handling', () => {
    it('should return fallback case in development mode on API error', async () => {
      const originalEnv = process.env.NODE_ENV
      process.env.NODE_ENV = 'development'

      ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'))

      const result = await generateCase(defaultParams)

      expect(result).toBeDefined()
      expect(result.case.title).toBe('The Missing Artifact')

      process.env.NODE_ENV = originalEnv
    })

    it('should throw error in production mode on API error', async () => {
      const originalEnv = process.env.NODE_ENV
      process.env.NODE_ENV = 'production'

      ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'))

      await expect(generateCase(defaultParams)).rejects.toThrow()

      process.env.NODE_ENV = originalEnv
    })

    it('should throw error on invalid JSON response', async () => {
      const originalEnv = process.env.NODE_ENV
      process.env.NODE_ENV = 'production'

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'This is not valid JSON' }),
      })

      await expect(generateCase(defaultParams)).rejects.toThrow(
        'Failed to parse the generated case data'
      )

      process.env.NODE_ENV = originalEnv
    })

    it('should handle HTTP error responses', async () => {
      const originalEnv = process.env.NODE_ENV
      process.env.NODE_ENV = 'production'

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ error: 'Server error' }),
      })

      await expect(generateCase(defaultParams)).rejects.toThrow()

      process.env.NODE_ENV = originalEnv
    })
  })

  describe('Request Parameters', () => {
    it('should use correct API endpoint', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      await generateCase(defaultParams)

      expect(global.fetch).toHaveBeenCalledWith(
        '/api/typhoon',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        })
      )
    })

    it('should send correct parameters in request body', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      await generateCase(defaultParams)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)

      expect(body.messages).toHaveLength(2)
      expect(body.messages[0].role).toBe('system')
      expect(body.messages[1].role).toBe('user')
      expect(body.temperature).toBe(0.7)
      expect(body.max_tokens).toBe(8192)
    })

    it('should use high max_tokens for case generation', async () => {
      const mockResponse = createMockCaseResponse()
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: mockResponse }),
      })

      await generateCase(defaultParams)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)

      expect(body.max_tokens).toBe(8192)
    })
  })

  describe('Difficulty Levels', () => {
    it.each(['easy', 'medium', 'hard'] as const)(
      'should generate case with %s difficulty',
      async difficulty => {
        const params: CaseGenerationParams = {
          difficulty,
          language: 'en',
        }

        const mockResponse = createMockCaseResponse()
        ;(global.fetch as jest.Mock).mockResolvedValueOnce({
          ok: true,
          json: async () => ({ response: mockResponse }),
        })

        const result = await generateCase(params)

        expect(result).toBeDefined()
        const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
        const body = JSON.parse(fetchCall[1].body)
        expect(body.messages[1].content).toContain(difficulty)
      }
    )
  })
})
