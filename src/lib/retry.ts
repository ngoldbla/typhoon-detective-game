/**
 * Retry utility for handling transient failures in API calls
 */

export interface RetryOptions {
  maxAttempts?: number
  delayMs?: number
  backoffMultiplier?: number
  maxDelayMs?: number
  retryableStatuses?: number[]
  onRetry?: (attempt: number, error: Error) => void
}

const DEFAULT_OPTIONS: Required<RetryOptions> = {
  maxAttempts: 3,
  delayMs: 1000,
  backoffMultiplier: 2,
  maxDelayMs: 10000,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  onRetry: () => {},
}

/**
 * Sleeps for a specified number of milliseconds
 */
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Determines if an error is retryable
 */
function isRetryableError(error: unknown, retryableStatuses: number[]): boolean {
  // Network errors are retryable
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return true
  }

  // Timeout errors are retryable
  if (error instanceof DOMException && error.name === 'AbortError') {
    return true
  }

  // Check for HTTP status errors
  if (error instanceof Error && error.message.includes('OpenAI API error')) {
    const statusMatch = error.message.match(/\((\d+)\)/)
    if (statusMatch) {
      const status = parseInt(statusMatch[1], 10)
      return retryableStatuses.includes(status)
    }
  }

  return false
}

/**
 * Retries an async function with exponential backoff
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const opts = { ...DEFAULT_OPTIONS, ...options }
  let lastError: Error | unknown

  for (let attempt = 1; attempt <= opts.maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error

      // Don't retry if this is the last attempt
      if (attempt === opts.maxAttempts) {
        break
      }

      // Don't retry if error is not retryable
      if (!isRetryableError(error, opts.retryableStatuses)) {
        break
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        opts.delayMs * Math.pow(opts.backoffMultiplier, attempt - 1),
        opts.maxDelayMs
      )

      // Notify about retry
      opts.onRetry(
        attempt,
        error instanceof Error ? error : new Error(String(error))
      )

      console.log(`Retrying after ${delay}ms (attempt ${attempt}/${opts.maxAttempts})...`)

      // Wait before retrying
      await sleep(delay)
    }
  }

  // All retries exhausted
  throw lastError
}

/**
 * Wraps a fetch call with retry logic
 */
export async function fetchWithRetry(
  url: string,
  init?: RequestInit,
  options?: RetryOptions
): Promise<Response> {
  return withRetry(
    async () => {
      const response = await fetch(url, init)

      // Check if response status is retryable
      const retryableStatuses = options?.retryableStatuses || DEFAULT_OPTIONS.retryableStatuses
      if (!response.ok && retryableStatuses.includes(response.status)) {
        const errorText = await response.text().catch(() => 'Unknown error')
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }

      return response
    },
    {
      ...options,
      onRetry: (attempt, error) => {
        console.warn(`Fetch request failed (attempt ${attempt}):`, error.message)
        options?.onRetry?.(attempt, error)
      },
    }
  )
}

/**
 * Creates a timeout promise that rejects after specified milliseconds
 */
export function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutMessage = 'Operation timed out'
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new DOMException(timeoutMessage, 'AbortError')), timeoutMs)
    ),
  ])
}

/**
 * Circuit breaker pattern for preventing cascading failures
 */
export class CircuitBreaker {
  private failureCount = 0
  private lastFailureTime: number | null = null
  private state: 'closed' | 'open' | 'half-open' = 'closed'

  constructor(
    private failureThreshold: number = 5,
    private resetTimeoutMs: number = 60000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (this.lastFailureTime && Date.now() - this.lastFailureTime > this.resetTimeoutMs) {
        console.log('Circuit breaker: Transitioning to half-open state')
        this.state = 'half-open'
      } else {
        throw new Error('Circuit breaker is open. Service is temporarily unavailable.')
      }
    }

    try {
      const result = await fn()

      // Success - reset circuit breaker
      if (this.state === 'half-open') {
        console.log('Circuit breaker: Transitioning to closed state')
        this.state = 'closed'
      }
      this.failureCount = 0
      this.lastFailureTime = null

      return result
    } catch (error) {
      this.failureCount++
      this.lastFailureTime = Date.now()

      if (this.failureCount >= this.failureThreshold) {
        console.error('Circuit breaker: Opening circuit due to repeated failures')
        this.state = 'open'
      }

      throw error
    }
  }

  getState(): 'closed' | 'open' | 'half-open' {
    return this.state
  }

  reset(): void {
    this.failureCount = 0
    this.lastFailureTime = null
    this.state = 'closed'
  }
}
