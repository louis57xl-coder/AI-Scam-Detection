AI Scam Detection Engine 🛡️
An end-to-end Machine Learning pipeline designed to detect and categorize fraudulent communications. This engine combines linguistic pattern matching with a Random Forest Classifier to identify scams with high precision and explainable reasoning.

🖥️ Interface Preview
The detector provides a color-coded breakdown of risk factors and confidence levels directly in your terminal:

Plaintext

------------------------------------------------------------
Paste the suspected message below:

PRESS CONTROL C TO EXIT

"Just got back from the dealer. Bought the new Porsche. Sending you a pic. This is what financial freedom looks like, my love. No bank loans. Just pure profit from yield farming and liquidity pools. I'm sitting here in my penthouse, watching the city lights, and all I can think about is you riding me, your legs wrapped around me, moaning my name as I thrust deep into you. I want to tie you up and spoil you sexually in this luxury. I want us to fuck on a bed of money. To get there, I need you as my investment partner. I'm giving you view-only access to my exchange dashboard right now. Look at the portfolio balance. See the APY—it's locked at 45%. I want you to allocate funds from your savings. It's a strategic reallocation. I'll set the leverage settings and stop-loss orders. Transfer $25,000 USDC to this wallet address. This is our joint investment. Our financial foreplay. Send the confirmation screenshot, and I'll video call you and do exactly what you tell me to. The market is moving. This window closes in 10 minutes. Don't miss our chance."

Analyzing behavioral markers across document windows...


================================================================================
                           🔴  CRITICAL DANGER — 99.0%
================================================================================

Matched Indicators: urgency_crisis, sexual_grooming, love_bombing_intensity, early_grooming, money_request, Lifestyle Flex

Action: Do not share financial info or send money.
--------------------------------------------------------------------------------

Paste the suspected message below:
PRESS CONTROL C TO EXIT
------------------------------------------------------------
🚀 Key Features
Hybrid Detection: Uses a dual-layer approach—statistical machine learning (Random Forest) paired with a 100+ keyword heuristic engine.

Explainable AI (XAI): The system doesn't just flag a scam; it provides a "Reasoning Breakdown" (e.g., detecting urgency, financial triggers, or authority fakes).

Multi-Vector Analysis: Specifically trained to catch Romance Scams, Crypto Fraud, and Law Enforcement Impersonation.

RESTful API Ready: Includes an endpoints.py deployment script for real-time integration into web or mobile apps.

🗝️ Detection Logic & Keyphrases
The engine identifies patterns across several high-weight categories including financial triggers, urgency tactics, and emotional manipulation. Keyphrases include:

Financial/Crypto: bitcoin, btc, gift card, wire transfer, wallet address, cash app

Urgency/Threats: urgent, immediately, within 24 hours, arrest warrant, account locked

Authority Fakes: IRS, Social Security, FBI, Microsoft Support, Amazon Security

Romance/Passion: my dearest, soulmate, trust me, investment pool, life together

Offers: winner, congratulations, lottery, jackpot, inheritance, administrative fee

🛠️ Installation & Usage
Setup
Bash

# Clone the repository
git clone https://github.com/louis57xl-coder/AI-Scam-Detection.git
cd AI-Scam-Detection

# Install dependencies
pip install -r requirements.txt
Run CLI Tool
Bash

python scam_detector.py --text "Enter your suspicious message here"
Deploy API
Bash

python endpoints.py
Access the API at http://localhost:8000. Test via Swagger UI at /docs.

📈 Performance Metrics
The model has been evaluated against a synthetic and real-world combined dataset:

Accuracy: 94.2%

Precision: 92.5%

Recall: 91.8%

F1-Score: 92.1%

📄 License
Distributed under the MIT License. See LICENSE for more information.


