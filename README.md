# Assessment Form Generator

A Flask-based web application that generates customizable assessment forms with HTML and JavaScript output. Create interactive questionnaires with configurable questions, choices, and scoring logic - all through an intuitive web interface.

## 🚀 Features

- **Dynamic Form Generation**
  - Create assessment forms with custom questions and choices
  - Real-time preview of generated forms
  - Flexible scoring system

- **User-Friendly Interface**
  - Intuitive web-based form builder
  - Add/remove questions and choices dynamically
  - Real-time validation
  - One-click code copying

- **Rich Output Options**
  - Generated HTML for form structure
  - Generated JavaScript for functionality
  - Mobile-responsive design
  - Interactive results visualization

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kalong2008/assessment-form-generator.git
   ```

2. Install dependencies:
   ```bash
   cd assessment-form-generator
   pip3 install -r requirements.txt
   ```

3. Start the application locally:
   ```bash
   python3 api/index.py
   ```

Access the local development server at `http://localhost:5000`

## 🚀 Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy with Vercel**
   - Visit [Vercel](https://vercel.com)
   - Import your GitHub repository
   - Select the Python framework preset
   - Configure build settings:
     - Build Command: `pip install -r requirements.txt`
     - Output Directory: `api`
   - Deploy!

## 📖 Usage

1. **Configure Your Form**
   - Set assessment name and title
   - Define form submission endpoint
   - Add answer choices with values
   - Create assessment questions

2. **Generate & Implement**
   - Click "Generate" to create form code
   - Copy the HTML and JavaScript
   - Integrate into your website

## 📁 Project Structure

```
assessment-form-generator/
├── api/
│   ├── index.py                # Application entry point
│   ├── generateAssessment.py   # Form generation logic
│   ├── static/
│   │   └── style.css          # Application styles
│   └── templates/
│       └── index.html         # Main UI template
├── requirements.txt           # Project dependencies
└── vercel.json               # Vercel configuration
```

## ⚙️ Configuration

| Option | Description | Example |
|--------|------------|---------|
| `name` | Unique assessment identifier | `"personality_test"` |
| `title` | Display title | `"Personality Assessment"` |
| `form_action_url` | Submission endpoint | `"https://api.example.com/submit"` |
| `choices` | Answer options with values | `[["Yes", 1], ["No", 0]]` |
| `questions` | Assessment questions | `["How do you feel about..."]` |

## 🔧 Customization

1. **Form Generation**
   - Modify question templates in `generateAssessment.py`
   - Update styling in `static/style.css`
   - Adjust submission handling in `index.py`

2. **Visual Customization**
   - Edit CSS for form appearance
   - Modify result visualization options
   - Customize response messages

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push and create a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Frontend Libraries**
  - HTML2Canvas for result visualization
  - Plotly.js for data visualization
  - SweetAlert2 for enhanced UX

- **Backend Framework**
  - Flask web framework