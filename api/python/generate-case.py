"""
Vercel Serverless Function: Generate Detective Case
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.case_generator import generate_case
from lib.types import CaseGenerationParams
from dataclasses import asdict


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Extract parameters
            params = CaseGenerationParams(
                difficulty=data.get('difficulty', 'easy'),
                theme=data.get('theme', ''),
                location=data.get('location', ''),
                era=data.get('era', ''),
                language=data.get('language', 'en')
            )

            # Generate case
            result = generate_case(params)

            # Convert to dict
            response_data = {
                'case': asdict(result.case),
                'clues': [asdict(c) for c in result.clues],
                'suspects': [asdict(s) for s in result.suspects],
                'solution': result.solution
            }

            # Send response
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
