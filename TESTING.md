# Testing Guide

This document describes the testing infrastructure and practices for the Detective Game application.

## Overview

The application includes comprehensive test coverage for all LLM-related functionality, ensuring robustness and reliability of the OpenAI API integrations.

## Test Infrastructure

- **Test Framework**: Jest 29
- **React Testing**: @testing-library/react
- **Environment**: jsdom (for browser simulation)
- **Coverage Tool**: Jest built-in coverage reporter

## Running Tests

```bash
# Run tests in watch mode (for development)
npm test

# Run tests once (for CI/CD)
npm run test:ci

# Run tests with coverage report
npm run test:coverage
```

## Test Structure

```
src/
├── __tests__/
│   └── utils/
│       └── mockOpenAI.ts         # Mock utilities for OpenAI responses
├── lib/
│   ├── __tests__/
│   │   ├── typhoon.test.ts       # Core API client tests
│   │   └── caseGenerator.test.ts # Case generation tests
│   ├── typhoon.ts                # Core OpenAI API client
│   ├── caseGenerator.ts          # Case generation logic
│   ├── env-validator.ts          # Environment validation
│   └── retry.ts                  # Retry logic for API calls
└── app/
    └── api/
        └── typhoon/
            └── __tests__/
                └── route.test.ts # API route tests
```

## Coverage Goals

The project maintains the following coverage thresholds:

- **Branches**: 70%
- **Functions**: 70%
- **Lines**: 70%
- **Statements**: 70%

## Test Categories

### 1. Unit Tests

#### Core Library (`lib/typhoon.test.ts`)
Tests for the main OpenAI API client:
- ✅ Successful API calls with various parameters
- ✅ Error handling (400, 401, 429, 500 errors)
- ✅ Network timeout handling
- ✅ Different model types (gpt-5, gpt-4o, o1-preview, etc.)
- ✅ Request parameter validation
- ✅ URL construction (client vs server)
- ✅ Retry logic with exponential backoff

#### Case Generator (`lib/caseGenerator.test.ts`)
Tests for detective case generation:
- ✅ Case generation with different parameters
- ✅ JSON parsing (with/without markdown code blocks)
- ✅ Fallback case in development mode
- ✅ Error handling and validation
- ✅ Alternative field name handling
- ✅ Suspect guilt assignment
- ✅ Unique ID generation

### 2. API Route Tests

#### `/api/typhoon` Route (`api/typhoon/__tests__/route.test.ts`)
Tests for the Next.js API route:
- ✅ Request validation (messages, model)
- ✅ Model-specific parameter handling:
  - o1 models: `max_completion_tokens` only
  - gpt-5 models: `max_completion_tokens` + `temperature=1.0`
  - Standard models: `max_tokens` + custom `temperature`
- ✅ OpenAI API error forwarding
- ✅ Environment variable handling
- ✅ Custom endpoint configuration
- ✅ Timeout handling

### 3. Utilities

#### Environment Validator (`lib/env-validator.ts`)
Validates environment configuration:
- Checks for required `OPENAI_API_KEY`
- Validates `OPENAI_BASE_URL` format
- Warns about non-standard models
- Provides environment configuration getters

#### Retry Logic (`lib/retry.ts`)
Handles transient failures:
- Exponential backoff retry strategy
- Configurable retry attempts and delays
- Circuit breaker pattern for cascading failure prevention
- Timeout utilities

## Mock Utilities

The `mockOpenAI.ts` file provides helpers for testing:

```typescript
import {
  mockSuccessfulFetch,
  mockFailedFetch,
  createMockCaseResponse
} from '@/__tests__/utils/mockOpenAI'

// Mock a successful API call
mockSuccessfulFetch('Hello! How can I help?')

// Mock a failed API call
mockFailedFetch(500, 'Server error')

// Create a complete mock case
const caseData = createMockCaseResponse()
```

## Writing New Tests

### Example Test Structure

```typescript
import { yourFunction } from '../yourFile'
import { mockSuccessfulFetch } from '@/__tests__/utils/mockOpenAI'

describe('yourFunction', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('Successful Operations', () => {
    it('should perform expected operation', async () => {
      mockSuccessfulFetch('Expected response')

      const result = await yourFunction(params)

      expect(result).toBe('Expected response')
    })
  })

  describe('Error Handling', () => {
    it('should handle errors gracefully', async () => {
      mockFailedFetch(500, 'Server error')

      await expect(yourFunction(params)).rejects.toThrow()
    })
  })
})
```

## CI/CD Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: npm run test:ci

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/lcov.info
```

## Key Testing Principles

1. **Isolation**: Each test is independent and doesn't rely on others
2. **Mocking**: External API calls are mocked to avoid real API usage
3. **Coverage**: Aim for high coverage of critical LLM functionality
4. **Clarity**: Test names clearly describe what they test
5. **Robustness**: Tests check both happy paths and error conditions

## LLM-Specific Testing Considerations

### Model Parameter Handling
Different models require different parameters:
- **o1 models**: Use `max_completion_tokens`, no `temperature`
- **gpt-5**: Use `max_completion_tokens`, force `temperature=1.0`
- **Standard models**: Use `max_tokens` and custom `temperature`

Tests verify that the correct parameters are sent for each model type.

### JSON Response Parsing
LLM responses may be formatted differently:
- Plain JSON
- JSON wrapped in markdown code blocks (```json...```)
- Alternative field names

Tests verify parsing works for all formats.

### Retry Logic
LLM APIs can be unreliable:
- Network timeouts
- Rate limiting (429)
- Server errors (500-504)

Tests verify retry logic with exponential backoff.

## Troubleshooting

### Tests Failing Locally

1. **Clear Jest cache**:
   ```bash
   npx jest --clearCache
   npm test
   ```

2. **Check environment variables**:
   Ensure `.env` is set up (tests use mock values from `jest.setup.js`)

3. **Check Node version**:
   The project requires Node 20+

### Coverage Below Threshold

Run coverage report to identify untested code:
```bash
npm run test:coverage
```

Check the HTML report in `coverage/lcov-report/index.html`

## Future Improvements

- [ ] Add tests for suspectAnalyzer.ts
- [ ] Add tests for clueAnalyzer.ts
- [ ] Add tests for caseSolver.ts
- [ ] Add tests for translator.ts
- [ ] Add tests for useTyphoon hook
- [ ] Add E2E tests with Playwright
- [ ] Add performance benchmarks
- [ ] Add visual regression tests

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Testing Library](https://testing-library.com/)
- [Next.js Testing](https://nextjs.org/docs/testing)
