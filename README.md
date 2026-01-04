Requires:
torch
scikit-learn
pandas
numpy

AI Scam Detection App
Python/PyTorch project for detecting relationship fraud and pig-butchering scams in text messages
Overview
This project is an interactive AI application that analyzes text messages for potential fraud. Using machine learning and deep learning models, it identifies linguistic and behavioral indicators of scams and outputs a probability-based risk assessment, helping users understand potential threats and protect themselves.
The project leverages Python, PyTorch, scikit-learn, and LLM-assisted workflows for feature extraction, classification, and scoring.
Features
⦁	Text Input: Users can provide text messages for analysis.
⦁	Fraud Detection: Identifies relationship fraud and pig-butchering scams using trained ML/DL models.
⦁	Probability Scoring: Outputs a risk probability for each message.
⦁	Guidance: Provides actionable insights to help users avoid scams.
⦁	Iterative Development: Continuously tested and refined for accuracy.
Technologies & Tools
⦁	Languages & Libraries: Python, PyTorch, scikit-learn, pandas, NumPy
⦁	AI Platforms: OpenAI, Hugging Face, LangChain (used for LLM-assisted analysis)
⦁	Development & Testing: Jupyter Notebook, iterative model validation, feature engineering
Installation
1.	Clone the repository:
git clone https://github.com/yourusername/ai-scam-detection.git
cd ai-scam-detection
2.	Create and activate a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3.	Install dependencies:
pip install -r requirements.txt
Usage
Run the main application script:
python scam_detector.py
⦁	Enter text messages when prompted.
⦁	The application will output a risk probability and a short fraud assessment.
⦁	Repeat with additional messages as needed.
Example Output
Input message: "I need you to invest $5,000 in this opportunity immediately."
Risk probability: 87%
Assessment: High likelihood of pig-butchering scam. Exercise caution and verify independently.
Contributing
This project is currently independent and project-based, but contributions are welcome via pull requests or suggestions.
License
MIT License
