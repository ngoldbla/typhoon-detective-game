"""OpenAI client for Typhoon Detective Game"""

import os
from typing import List, Dict, Optional
from openai import OpenAI
import streamlit as st
import httpx


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

        # Default model
        self.default_model = os.getenv('OPENAI_MODEL', 'gpt-4o')

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

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise


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
