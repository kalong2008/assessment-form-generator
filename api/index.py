from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Add the project root directory to Python path for local development
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

try:
    from api.generateAssessment import AssessmentGenerator  # For Vercel
except ImportError:
    from generateAssessment import AssessmentGenerator  # For local development

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        config = request.json
        generator = AssessmentGenerator(config)
        
        # Generate HTML and JS
        html = generator.generate_html()
        js = generator.js_generator.generate_js()
        
        return jsonify({
            'html': html,
            'js': js,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 