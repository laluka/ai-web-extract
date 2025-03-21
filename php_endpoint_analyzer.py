#!/usr/bin/env python3
"""AI PHP Code Analyzer

Usage:
    ai-web-extract.py [<SOURCES_DIR>] [<MODEL>]

Arguments:
    SOURCES_DIR  Directory containing PHP files to analyze [default: src]
    MODEL       Ollama model to use (codellama:34b or deepseek-coder:33b) [default: codellama:34b]

Options:
    -h --help     Show this help message
"""
import os
import json
import requests
from typing import List, Optional
from pathlib import Path
from docopt import docopt

class PHPCodeAnalyzer:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "codellama:34b"):
        self.ollama_url = ollama_url
        self.model = model
        self.analysis_results = []
        self.output_dir = "out"
    def read_file(self, file_path: str) -> str:
        """Read a file and return its contents."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def analyze_file(self, file_path: str) -> None:
        """Analyze a PHP file by sending its contents to Ollama."""
        content = self.read_file(file_path)
        
        prompt = f"""Analyze this PHP code and extract every web PATH, and INPTU PARAMETERS, including:
        - HTTP methods (GET, POST, PUT, DELETE, etc.)
        - URLs/routes
        - Authentication, XHR, and other relevant headers
        - Input Parameters (GET, POST, PUT, DELETE, json, xml, ...)
        - Any security-related descriptions or comments

        Here's the code:
        {content}

        I want you to output a final clean structured json file, here is a sample below:
        {{
            "endpoints": [
                {{
                    "path": "/api/foo",
                    "methods": ["GET", "POST"],
                    "input_parameters": ["id", "name", "email"],
                    "input_headers": ["Authorization", "X-API-KEY"],
                    "description": "Get all users",
                    "curl_request": "curl -X GET 'https://example.com/api/foo?id=1&name=John&email=john@example.com' -H 'Authorization: Bearer token'"
                }},
                {{
                    "path": "/bar.html",
                    "methods": ["GET", "POST"],
                    "input_parameters": ["username", "age"],
                    "input_headers": ["Authorization", "Bearer: token"],
                    "description": "Display bar page",
                    "curl_request": "curl -X GET 'https://example.com/bar.html?username=John&age=25' -H 'Authorization: Bearer token'"
                }}
            ]
        }}
        """

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                # ensure file exists, create subdir if not exists
                file_path =  os.path.join(self.output_dir, file_path)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(result.get('response', '').strip())
        except Exception as e:
            print(f"Error analyzing file with Ollama: {e}")

    def analyze_directory(self, directory: str) -> None:
        """Recursively analyze all PHP files in a directory."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    print(f"Analyzing {file_path}...")
                    self.analyze_file(file_path)

    def export_results(self, output_file: str = "analysis_results.json") -> None:
        """Export the analysis results to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2)

def main():
    args = docopt(__doc__)
    
    sources_dir = args['<SOURCES_DIR>'] or 'src'
    model = args['<MODEL>'] or 'codellama:34b'
    
    if not os.path.exists(sources_dir):
        print(f"Error: Directory '{sources_dir}' does not exist")
        return

    if model not in ['codellama:34b', 'deepseek-coder:33b']:
        print("Error: Model must be either 'codellama:34b' or 'deepseek-coder:33b'")
        return

    print(f"Using model: {model}")
    print(f"Analyzing directory: {sources_dir}")
    
    analyzer = PHPCodeAnalyzer(model=model)
    analyzer.analyze_directory(sources_dir)
    analyzer.export_results()
    print("Analysis complete. Results exported to analysis_results.json")

if __name__ == "__main__":
    main() 