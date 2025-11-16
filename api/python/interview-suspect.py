"""
Vercel Serverless Function: Interview Suspect
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.suspect_analyzer import process_interview_question
from lib.types import Suspect, Clue, Case


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Extract data
            question = data['question']
            suspect = Suspect(**data['suspect'])
            clues = [Clue(**c) for c in data.get('clues', [])]
            case_data = Case(**data['case'])
            previous_questions = data.get('previousQuestions', [])
            language = data.get('language', 'en')

            # Process interview
            answer = process_interview_question(
                question,
                suspect,
                clues,
                case_data,
                previous_questions,
                language
            )

            # Send response
            response_data = {'answer': answer}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
