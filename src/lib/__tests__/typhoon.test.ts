import { fetchOpenAICompletion } from '../typhoon'
import { mockSuccessfulFetch, mockFailedFetch, mockNetworkError, mockTimeoutError } from '@/test-utils/mockOpenAI'

describe('fetchOpenAICompletion', () => {
  const testMessages = [
    { role: 'system' as const, content: 'You are a helpful assistant' },
    { role: 'user' as const, content: 'Hello' },
  ]

  beforeEach(() => {
    jest.clearAllMocks()
    // Mock window.location for client-side calls
    if (typeof window !== 'undefined') {
      Object.defineProperty(window, 'location', {
        value: { origin: 'http://localhost:3000' },
        writable: true,
      })
    } else {
      // In Node environment, create a global window mock
      ;(global as any).window = {
        location: { origin: 'http://localhost:3000' },
      }
    }
  })

  afterEach(() => {
    // Clean up global window mock if we created it
    if (typeof window === 'undefined' && (global as any).window) {
      delete (global as any).window
    }
  })

  describe('Successful API Calls', () => {
    it('should successfully fetch completion with default parameters', async () => {
      const mockContent = 'Hello! How can I help you today?'
      mockSuccessfulFetch(mockContent)

      const result = await fetchOpenAICompletion(testMessages)

      expect(result).toBe(mockContent)
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:3000/api/typhoon',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        })
      )
    })

    it('should successfully fetch completion with custom model', async () => {
      const mockContent = 'Response from GPT-4'
      mockSuccessfulFetch(mockContent, 'gpt-4')

      const result = await fetchOpenAICompletion(testMessages, 'gpt-4')

      expect(result).toBe(mockContent)
      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.model).toBe('gpt-4')
    })

    it('should successfully fetch completion with custom temperature', async () => {
      const mockContent = 'Creative response'
      mockSuccessfulFetch(mockContent)

      const result = await fetchOpenAICompletion(testMessages, 'gpt-5', 0.9)

      expect(result).toBe(mockContent)
      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.temperature).toBe(0.9)
    })

    it('should successfully fetch completion with custom max_tokens', async () => {
      const mockContent = 'Long response'
      mockSuccessfulFetch(mockContent)

      const result = await fetchOpenAICompletion(testMessages, 'gpt-5', 0.7, 2000)

      expect(result).toBe(mockContent)
      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.max_tokens).toBe(2000)
    })

    it('should send all messages in the request', async () => {
      const mockContent = 'Response'
      mockSuccessfulFetch(mockContent)

      const multiMessages = [
        { role: 'system' as const, content: 'System prompt' },
        { role: 'user' as const, content: 'User message 1' },
        { role: 'assistant' as const, content: 'Assistant response' },
        { role: 'user' as const, content: 'User message 2' },
      ]

      await fetchOpenAICompletion(multiMessages)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.messages).toEqual(multiMessages)
    })
  })

  describe('Error Handling', () => {
    it('should throw error on 400 bad request', async () => {
      mockFailedFetch(400, 'Invalid request format')

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('OpenAI API error (400)')
    })

    it('should throw error on 401 unauthorized', async () => {
      mockFailedFetch(401, 'Invalid API key')

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('OpenAI API error (401)')
    })

    it('should throw error on 429 rate limit', async () => {
      mockFailedFetch(429, 'Rate limit exceeded')

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('OpenAI API error (429)')
    })

    it('should throw error on 500 server error', async () => {
      mockFailedFetch(500, 'Internal server error')

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('OpenAI API error (500)')
    })

    it('should throw error on network failure', async () => {
      mockNetworkError('Network request failed')

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('Network request failed')
    })

    it('should throw specific error on timeout', async () => {
      mockTimeoutError()

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('Request timed out')
    })

    it('should throw error when response has no data', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({}),
      })

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('Received invalid response from server')
    })

    it('should throw error when response.response is undefined', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ data: 'invalid' }),
      })

      await expect(
        fetchOpenAICompletion(testMessages)
      ).rejects.toThrow('Received invalid response from server')
    })
  })

  describe('Different Model Types', () => {
    it('should work with gpt-5 model', async () => {
      const mockContent = 'GPT-5 response'
      mockSuccessfulFetch(mockContent, 'gpt-5')

      const result = await fetchOpenAICompletion(testMessages, 'gpt-5')

      expect(result).toBe(mockContent)
      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.model).toBe('gpt-5')
    })

    it('should work with gpt-4o model', async () => {
      const mockContent = 'GPT-4o response'
      mockSuccessfulFetch(mockContent, 'gpt-4o')

      const result = await fetchOpenAICompletion(testMessages, 'gpt-4o')

      expect(result).toBe(mockContent)
    })

    it('should work with o1-preview model', async () => {
      const mockContent = 'O1 preview response'
      mockSuccessfulFetch(mockContent, 'o1-preview')

      const result = await fetchOpenAICompletion(testMessages, 'o1-preview')

      expect(result).toBe(mockContent)
    })

    it('should work with custom model string', async () => {
      const mockContent = 'Custom model response'
      mockSuccessfulFetch(mockContent, 'custom-model-v1')

      const result = await fetchOpenAICompletion(testMessages, 'custom-model-v1')

      expect(result).toBe(mockContent)
    })
  })

  describe('URL Construction', () => {
    it('should use window.location.origin in browser environment', async () => {
      mockSuccessfulFetch('Response')

      await fetchOpenAICompletion(testMessages)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:3000/api/typhoon',
        expect.any(Object)
      )
    })

    it('should handle NEXT_PUBLIC_BASE_URL in server environment', async () => {
      // Temporarily remove window
      const originalWindow = global.window
      // @ts-ignore
      delete global.window
      process.env.NEXT_PUBLIC_BASE_URL = 'https://example.com'

      mockSuccessfulFetch('Response')

      await fetchOpenAICompletion(testMessages)

      expect(global.fetch).toHaveBeenCalledWith(
        'https://example.com/api/typhoon',
        expect.any(Object)
      )

      // Restore window
      global.window = originalWindow
      delete process.env.NEXT_PUBLIC_BASE_URL
    })
  })

  describe('Request Parameters', () => {
    it('should include abort signal in request', async () => {
      mockSuccessfulFetch('Response')

      await fetchOpenAICompletion(testMessages)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      expect(fetchCall[1].signal).toBeInstanceOf(AbortSignal)
    })

    it('should use default temperature of 0.7', async () => {
      mockSuccessfulFetch('Response')

      await fetchOpenAICompletion(testMessages)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.temperature).toBe(0.7)
    })

    it('should use default max_tokens of 800', async () => {
      mockSuccessfulFetch('Response')

      await fetchOpenAICompletion(testMessages)

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0]
      const body = JSON.parse(fetchCall[1].body)
      expect(body.max_tokens).toBe(800)
    })
  })
})
