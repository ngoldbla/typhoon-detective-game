"""
Audio utilities for the detective game.
Provides text-to-speech, voice dictation, and sound effects using browser APIs.
"""

import streamlit as st
from typing import Optional


def get_tts_component(text: str, button_label: str = "🔊 Listen") -> str:
    """
    Create a text-to-speech button using Web Speech API.

    Args:
        text: The text to be read aloud
        button_label: Label for the button

    Returns:
        HTML string with the TTS button component
    """
    # Escape quotes and newlines for JavaScript
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')

    html = f"""
    <button onclick="speakText_{id(text)}()" style="
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: 2px solid #2C3E50;
        border-radius: 8px;
        padding: 8px 16px;
        cursor: pointer;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        box-shadow: 2px 2px 0px #2C3E50;
        margin: 5px 0;
    ">
        {button_label}
    </button>
    <script>
        function speakText_{id(text)}() {{
            if ('speechSynthesis' in window) {{
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();

                const utterance = new SpeechSynthesisUtterance("{safe_text}");
                utterance.rate = 0.9;  // Slightly slower for clarity
                utterance.pitch = 1.1;  // Slightly higher pitch for kid-friendly voice
                utterance.volume = 1.0;

                // Try to use a child-friendly voice if available
                const voices = window.speechSynthesis.getVoices();
                const preferredVoice = voices.find(voice =>
                    voice.name.includes('Google') ||
                    voice.name.includes('female') ||
                    voice.lang.startsWith('en')
                );
                if (preferredVoice) {{
                    utterance.voice = preferredVoice;
                }}

                window.speechSynthesis.speak(utterance);
            }} else {{
                alert('Sorry, your browser does not support text-to-speech.');
            }}
        }}

        // Load voices (needed for some browsers)
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.getVoices();
        }}
    </script>
    """

    return html


def get_speech_recognition_component(input_key: str, placeholder: str = "Ask a question...") -> str:
    """
    Create a voice input button using Web Speech Recognition API.

    Args:
        input_key: The session state key for the text input to fill
        placeholder: Placeholder text for the input field

    Returns:
        HTML string with the speech recognition button component
    """
    html = f"""
    <div style="margin: 10px 0;">
        <button onclick="startDictation()" id="dictation-btn" style="
            background: linear-gradient(135deg, #17A2B8 0%, #138496 100%);
            color: white;
            border: 2px solid #2C3E50;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            font-family: 'Comic Neue', cursive;
            font-weight: bold;
            box-shadow: 2px 2px 0px #2C3E50;
            margin: 5px 0;
        ">
            🎤 Speak Your Question
        </button>
        <span id="dictation-status" style="
            margin-left: 10px;
            font-family: 'Comic Neue', cursive;
            color: #F7931E;
            font-weight: bold;
        "></span>
    </div>

    <script>
        function startDictation() {{
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                alert('Sorry, your browser does not support voice dictation. Please use Chrome, Edge, or Safari.');
                return;
            }}

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();

            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            const statusElement = document.getElementById('dictation-status');
            const btnElement = document.getElementById('dictation-btn');

            recognition.onstart = function() {{
                statusElement.textContent = '🎤 Listening...';
                btnElement.style.background = 'linear-gradient(135deg, #DC3545 0%, #C82333 100%)';
            }};

            recognition.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;

                // Find the text input and set its value
                const inputs = window.parent.document.querySelectorAll('input[type="text"], textarea');
                for (let input of inputs) {{
                    if (input.placeholder === "{placeholder}" || input.value === "") {{
                        input.value = transcript;
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        break;
                    }}
                }}

                statusElement.textContent = '✅ Got it!';
                setTimeout(() => {{ statusElement.textContent = ''; }}, 2000);
            }};

            recognition.onerror = function(event) {{
                statusElement.textContent = '❌ Error: ' + event.error;
                setTimeout(() => {{ statusElement.textContent = ''; }}, 3000);
            }};

            recognition.onend = function() {{
                btnElement.style.background = 'linear-gradient(135deg, #17A2B8 0%, #138496 100%)';
            }};

            recognition.start();
        }}
    </script>
    """

    return html


def get_sound_effect(effect_type: str) -> str:
    """
    Play a sound effect using Web Audio API.

    Args:
        effect_type: Type of sound ('clue', 'success', 'error')

    Returns:
        HTML string with the sound effect script
    """
    if effect_type == 'clue':
        # Pleasant discovery tone
        script = """
        <script>
            (function() {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = 800;
                oscillator.type = 'sine';

                gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.5);
            })();
        </script>
        """
    elif effect_type == 'success':
        # Celebration chord sequence
        script = """
        <script>
            (function() {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();

                function playTone(frequency, startTime, duration) {
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();

                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);

                    oscillator.frequency.value = frequency;
                    oscillator.type = 'sine';

                    gainNode.gain.setValueAtTime(0.2, startTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

                    oscillator.start(startTime);
                    oscillator.stop(startTime + duration);
                }

                const now = audioContext.currentTime;
                playTone(523.25, now, 0.2);        // C
                playTone(659.25, now + 0.15, 0.2); // E
                playTone(783.99, now + 0.3, 0.4);  // G
            })();
        </script>
        """
    elif effect_type == 'error':
        # Alert tone
        script = """
        <script>
            (function() {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = 200;
                oscillator.type = 'square';

                gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.3);
            })();
        </script>
        """
    else:
        return ""

    return script


def play_celebration_sound() -> str:
    """Play a celebration sound for solving a case

    Returns:
        HTML string with the celebration sound script
    """
    return get_sound_effect('success')


def get_audio_settings_ui() -> dict:
    """
    Create audio settings UI and return current settings.

    Returns:
        Dictionary with audio settings
    """
    st.markdown("### 🔊 Audio Settings")

    # Initialize audio settings in session state if not present
    if 'audio_settings' not in st.session_state:
        st.session_state.audio_settings = {
            'tts_enabled': True,
            'dictation_enabled': True,
            'sounds_enabled': True
        }

    tts_enabled = st.checkbox(
        "Text-to-Speech",
        value=st.session_state.audio_settings.get('tts_enabled', True),
        help="Hear suspect responses read aloud",
        key="audio_tts"
    )

    dictation_enabled = st.checkbox(
        "Voice Dictation",
        value=st.session_state.audio_settings.get('dictation_enabled', True),
        help="Ask questions using your voice",
        key="audio_dictation"
    )

    sounds_enabled = st.checkbox(
        "Sound Effects",
        value=st.session_state.audio_settings.get('sounds_enabled', True),
        help="Play sounds for game events",
        key="audio_sounds"
    )

    # Update session state
    settings = {
        'tts_enabled': tts_enabled,
        'dictation_enabled': dictation_enabled,
        'sounds_enabled': sounds_enabled
    }

    st.session_state.audio_settings = settings

    return settings
