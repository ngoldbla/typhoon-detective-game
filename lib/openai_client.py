"""OpenAI client for Emerson Detective Game"""

import os
from typing import List, Dict, Optional
from openai import OpenAI
import streamlit as st
import httpx


# Valid OpenAI model names (as of January 2025)
VALID_MODELS = {
    'gpt-4o',
    'gpt-4o-mini',
    'gpt-4-turbo',
    'gpt-4-turbo-preview',
    'gpt-4',
    'gpt-3.5-turbo',
    'o1-preview',
    'o1-mini',
    'o1',
    # Add common variants/aliases
    'gpt-4-turbo-2024-04-09',
    'gpt-4-0125-preview',
    'gpt-4-1106-preview',
    'gpt-3.5-turbo-0125',
}


def validate_model_name(model: str) -> tuple[bool, str]:
    """Validate if a model name is valid

    Args:
        model: The model name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not model:
        return False, "Model name cannot be empty"

    # Check if it's a known valid model
    if model in VALID_MODELS:
        return True, ""

    # Check for common mistakes
    if 'gpt-5' in model.lower():
        return False, (
            f"Invalid model '{model}': GPT-5 does not exist yet. "
            f"Did you mean 'gpt-4o' (GPT-4 optimized) or 'gpt-4-turbo'?"
        )

    if 'gpt-4.1' in model.lower():
        return False, (
            f"Invalid model '{model}': Model names use hyphens, not dots. "
            f"Did you mean 'gpt-4o', 'gpt-4-turbo', or 'gpt-4'?"
        )

    # Check if it starts with a known prefix (might be a newer model)
    known_prefixes = ('gpt-4o', 'gpt-4', 'gpt-3.5', 'o1')
    if any(model.startswith(prefix) for prefix in known_prefixes):
        # Might be a valid newer model, allow it but warn
        return True, f"Warning: Model '{model}' is not in the known list but has a valid prefix. Proceeding anyway."

    # Unknown model
    return False, (
        f"Invalid model '{model}': Not a recognized OpenAI model. "
        f"Valid models include: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, o1-preview, o1-mini. "
        f"Check your OPENAI_MODEL environment variable."
    )


class OpenAIClient:
    """Client for interacting with OpenAI API"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize OpenAI client

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: Optional custom API base URL
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL')

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Initialize OpenAI client with explicit parameters
        # Note: Modern OpenAI SDK (v1.0+) uses httpx and automatically handles
        # proxy environment variables (HTTP_PROXY, HTTPS_PROXY, etc.)
        # Do NOT pass 'proxies' parameter - it's not supported

        # Create httpx client with proper configuration
        # This avoids issues with proxy configurations
        http_client = httpx.Client(
            timeout=60.0,
            follow_redirects=True,
            # httpx automatically picks up HTTP_PROXY/HTTPS_PROXY env vars
            # Do NOT manually pass proxies parameter
        )

        client_kwargs = {
            "api_key": self.api_key,
            "http_client": http_client,
            "max_retries": 2   # Retry on network errors
        }

        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        try:
            self.client = OpenAI(**client_kwargs)
        except TypeError as e:
            # Handle case where unexpected parameters are passed
            error_msg = str(e)
            if "proxies" in error_msg or "http_client" in error_msg:
                # Fallback: try without custom http_client
                print(f"Warning: Error with custom http_client: {error_msg}")
                print("Falling back to default OpenAI client configuration")
                fallback_kwargs = {"api_key": self.api_key}
                if self.base_url:
                    fallback_kwargs["base_url"] = self.base_url
                self.client = OpenAI(**fallback_kwargs)
            else:
                raise

        # Default model - validate it
        self.default_model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        is_valid, error_msg = validate_model_name(self.default_model)
        if not is_valid:
            raise ValueError(
                f"Invalid OPENAI_MODEL in environment: {error_msg}\n"
                f"Please set OPENAI_MODEL to a valid model like 'gpt-4o' or 'gpt-4o-mini'"
            )
        elif error_msg:  # Warning message
            print(error_msg)

    def fetch_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 800
    ) -> str:
        """Fetch completion from OpenAI API

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to gpt-4o)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Returns:
            The completion text
        """
        model = model or self.default_model

        # Validate the model name before making API call
        is_valid, error_msg = validate_model_name(model)
        if not is_valid:
            raise ValueError(error_msg)
        elif error_msg:  # Warning
            print(error_msg)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            error_str = str(e)
            print(f"Error calling OpenAI API: {error_str}")

            # Provide more helpful error messages
            if "model" in error_str.lower() and "does not exist" in error_str.lower():
                raise ValueError(
                    f"The model '{model}' is not recognized by OpenAI API. "
                    f"Valid models include: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo. "
                    f"Please check your OPENAI_MODEL environment variable."
                ) from e
            elif "timeout" in error_str.lower() or "timed out" in error_str.lower():
                raise TimeoutError(
                    f"Request to OpenAI API timed out. This might be due to:\n"
                    f"1. An invalid model name ('{model}')\n"
                    f"2. Network connectivity issues\n"
                    f"3. OpenAI API being slow/unavailable\n"
                    f"Please verify your OPENAI_MODEL is set to a valid model like 'gpt-4o'"
                ) from e
            elif "api_key" in error_str.lower():
                raise ValueError(
                    "Invalid or missing API key. Please check that OPENAI_API_KEY is set correctly."
                ) from e
            else:
                # Re-raise the original exception with additional context
                raise Exception(f"OpenAI API error: {error_str}") from e

    def generate_image(
        self,
        prompt: str,
        model: str = "gpt-image-1",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> str:
        """Generate an image using OpenAI image generation

        Args:
            prompt: Text description of the image to generate
            model: Model to use (default: gpt-image-1)
            size: Image size (1024x1024, 1792x1024, or 1024x1792)
            quality: Image quality (standard or hd)
            n: Number of images to generate

        Returns:
            URL of the generated image
        """
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )

            return response.data[0].url

        except Exception as e:
            error_str = str(e)
            print(f"Error generating image: {error_str}")

            # Provide helpful error messages
            if "billing" in error_str.lower():
                raise ValueError(
                    "Image generation failed due to billing issues. "
                    "Please check your OpenAI account has credits available."
                ) from e
            elif "content_policy" in error_str.lower() or "safety" in error_str.lower():
                raise ValueError(
                    "Image generation failed: Content policy violation. "
                    "The prompt may contain inappropriate content."
                ) from e
            else:
                raise Exception(f"Image generation error: {error_str}") from e


# Singleton instance
_client: Optional[OpenAIClient] = None


def get_openai_client() -> OpenAIClient:
    """Get or create the OpenAI client singleton"""
    global _client

    if _client is None:
        try:
            _client = OpenAIClient()
        except ValueError as e:
            # API key not set
            st.error(str(e))
            st.info("Please set OPENAI_API_KEY in your environment variables or .env file")
            raise

    return _client


def fetch_openai_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 800
) -> str:
    """Helper function to fetch OpenAI completion

    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model to use (defaults to gpt-4o)
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response

    Returns:
        The completion text
    """
    client = get_openai_client()
    return client.fetch_completion(messages, model, temperature, max_tokens)
