// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom'

// Mock environment variables for tests
process.env.OPENAI_API_KEY = 'test-api-key'
process.env.OPENAI_BASE_URL = 'https://api.openai.com/v1'
process.env.OPENAI_MODEL = 'gpt-5'

// Mock fetch globally for tests
global.fetch = jest.fn()

// Reset all mocks after each test
afterEach(() => {
  jest.clearAllMocks()
})
