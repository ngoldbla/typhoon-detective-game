/**
 * Environment variable validation utility
 * Ensures all required environment variables are present and valid
 */

export interface EnvValidationResult {
  isValid: boolean
  errors: string[]
  warnings: string[]
}

/**
 * Validates that required environment variables are set
 */
export function validateEnvironment(): EnvValidationResult {
  const errors: string[] = []
  const warnings: string[] = []

  // Check for OPENAI_API_KEY (server-side only)
  if (typeof window === 'undefined') {
    if (!process.env.OPENAI_API_KEY) {
      errors.push('OPENAI_API_KEY is not set. This is required for the application to function.')
    } else if (process.env.OPENAI_API_KEY.length < 10) {
      errors.push('OPENAI_API_KEY appears to be invalid (too short).')
    } else if (process.env.OPENAI_API_KEY === 'your_api_key_here') {
      errors.push('OPENAI_API_KEY is still set to the placeholder value. Please set a valid API key.')
    }
  }

  // Check OPENAI_BASE_URL
  const baseUrl = process.env.OPENAI_BASE_URL
  if (baseUrl) {
    try {
      new URL(baseUrl)
    } catch {
      errors.push(`OPENAI_BASE_URL is not a valid URL: ${baseUrl}`)
    }

    if (!baseUrl.startsWith('https://') && !baseUrl.startsWith('http://localhost')) {
      warnings.push('OPENAI_BASE_URL should use HTTPS in production environments.')
    }
  }

  // Check OPENAI_MODEL
  const model = process.env.OPENAI_MODEL
  if (model) {
    const validModels = [
      'gpt-5',
      'gpt-4o',
      'gpt-4o-mini',
      'gpt-4-turbo',
      'gpt-4',
      'gpt-3.5-turbo',
      'o1-preview',
      'o1-mini',
    ]

    // Only warn if using standard OpenAI endpoint
    const usingStandardEndpoint = !baseUrl || baseUrl === 'https://api.openai.com/v1'
    if (usingStandardEndpoint && !validModels.includes(model)) {
      warnings.push(
        `OPENAI_MODEL is set to "${model}" which is not a standard OpenAI model. ` +
          `Valid models: ${validModels.join(', ')}`
      )
    }
  }

  // Check NODE_ENV
  if (!process.env.NODE_ENV) {
    warnings.push('NODE_ENV is not set. Defaulting to development mode.')
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
  }
}

/**
 * Validates environment and logs results
 * Throws an error if validation fails
 */
export function validateAndLogEnvironment(): void {
  const result = validateEnvironment()

  if (result.warnings.length > 0) {
    console.warn('Environment variable warnings:')
    result.warnings.forEach(warning => console.warn(`  - ${warning}`))
  }

  if (!result.isValid) {
    console.error('Environment variable validation failed:')
    result.errors.forEach(error => console.error(`  - ${error}`))
    throw new Error(
      'Environment validation failed. Please check your .env file and ensure all required variables are set.'
    )
  }

  console.log('✓ Environment variables validated successfully')
}

/**
 * Gets the current environment configuration
 */
export function getEnvironmentConfig() {
  return {
    apiKey: process.env.OPENAI_API_KEY,
    baseUrl: process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1',
    model: process.env.OPENAI_MODEL || 'gpt-5',
    nodeEnv: process.env.NODE_ENV || 'development',
  }
}

/**
 * Checks if the app is running in production mode
 */
export function isProduction(): boolean {
  return process.env.NODE_ENV === 'production'
}

/**
 * Checks if the app is running in development mode
 */
export function isDevelopment(): boolean {
  return process.env.NODE_ENV === 'development' || !process.env.NODE_ENV
}
