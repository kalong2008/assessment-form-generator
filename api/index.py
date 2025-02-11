from flask import Flask, render_template, request, jsonify
from generateAssessment import AssessmentGenerator
import json

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