"""
Vercel Serverless Function: Analyze Clue
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.clue_analyzer import analyze_clue
from lib.types import Clue, Suspect, Case
from dataclasses import asdict


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Extract data
            clue = Clue(**data['clue'])
            suspects = [Suspect(**s) for s in data['suspects']]
            case_data = Case(**data['case'])
            discovered_clues = [Clue(**c) for c in data.get('discoveredClues', [])]
            language = data.get('language', 'en')

            # Analyze clue
            analysis = analyze_clue(clue, suspects, case_data, discovered_clues, language)

            # Convert to dict
            response_data = {
                'summary': analysis.summary,
                'connections': [asdict(c) for c in analysis.connections],
                'nextSteps': analysis.nextSteps
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
