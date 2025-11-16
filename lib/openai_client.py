"""OpenAI client for Typhoon Detective Game"""

import os
from typing import List, Dict, Optional
from openai import OpenAI
import streamlit as st


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

        # Initialize OpenAI client
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

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
