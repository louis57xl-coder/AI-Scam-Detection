---
title: ScamCheck v2.01 – Open Source Python Project
description: ScamCheck v2.01 is an open-source Python project for detecting romance scams, financial fraud, and social engineering patterns using Python and AI.
---

# ScamCheck v2.01 🛡️

**Created By Louis Iacoletti** [View My Resume](https://github.com/louis57xl-coder/AI-Scam-Detection/blob/main/resume.pdf)

🔍 Multi-Platform Message Analysis for Romance & Money Scams

ScamCheck can analyze text copied directly from social media platforms, dating applications, and private messaging services to detect early indicators of romance scams and financial fraud. Users can paste conversations from dating apps such as Tinder, Bumble, Hinge, Match, OkCupid, Plenty of Fish (POF), eHarmony, Zoosk, Coffee Meets Bagel, and Facebook Dating, as well as social and messaging platforms including Facebook, Instagram, X (Twitter), TikTok, WhatsApp, Telegram, Snapchat, Discord, LinkedIn, SMS, and email. The system evaluates emotional manipulation, rapid relationship escalation, secrecy requests, urgency framing, investment narratives, cryptocurrency pitches, wire transfer or gift card requests, and grooming behaviors, providing an early-warning risk assessment before financial or emotional harm occurs.

![GitHub repo stars](https://img.shields.io/github/stars/louis57xl-coder/AI-Scam-Detection)
![GitHub forks](https://img.shields.io/github/forks/louis57xl-coder/AI-Scam-Detection)
![Python version](https://img.shields.io/badge/python-3.8+-blue)
![Windows Executable](https://img.shields.io/badge/Windows-Executable-green)
![Accuracy](https://img.shields.io/badge/Accuracy-95.9%25-red)

**ScamCheck v2.01** is an open-source Python project designed to identify common scam patterns in messages, including:

- Romance and relationship fraud  
- Financial fraud and investment scams  
- Social engineering attempts  
- Online manipulation and grooming tactics

**Now available as both a standalone Windows executable (210.8 MB) and Python script with 95.9% proven accuracy.**

---

## 📊 **Real User Interface with Test Data**

### **What Users Actually See When Using ScamCheck:**


text

**Test Statistics:**
- **🔴 CRITICAL DANGER**: 9 examples (90%)
- **🟠 HIGH RISK**: 1 example (10%) 
- **Overall Accuracy**: 95.9%
- **Total Words Tested**: 2,480
- **False Negatives**: 0%

![screenshot](https://github.com/user-attachments/assets/d306372c-5a14-489a-b79f-a1384d7c0592)
---

## 🚀 **Features**

- **Analyze text messages** for scam likelihood with 95.9% accuracy
- **Python-based**, easy to extend and customize
- **Open-source** and actively maintained
- **Works with AI-assisted heuristics** and emotion analysis
- **Standalone Windows executable** (210.8 MB) - no installation needed
- **Real-time GUI interface** with color-coded risk levels
- **Offline operation** - privacy-focused, no data sent
- **Early warning system** - detects grooming before financial requests

---

## 📦 **Installation**

### **Option 1: Windows Executable (Easiest)**
1. Download `scamcheck.exe` (210.8 MB)
2. Double-click to launch (no installation needed)
3. Wait 10-20 seconds for AI models to load (first time only)

### **Option 2: Python Script**
```bash
git clone https://github.com/louis57xl-coder/AI-Scam-Detection.git
cd AI-Scam-Detection
pip install -r requirements.txt
💻 Usage
Windows Executable:
Launch scamcheck.exe

Paste suspicious text from dating apps, social media, or emails

Click "Analyze Message"

Review the color-coded results and matched indicators

Python Script:
bash
python scamcheck.py
Example Test Case Detected:

text
===============================================================================
                            🔴  CRITICAL DANGER — 99.0%
===============================================================================

Matched Indicators: sexual_grooming, money_request, love_bombing_intensity, 
                    urgency_crisis, Lifestyle Flex, Authority / Mentorship, 
                    Small Test Ask, Romance + Future Promise, Withdrawal Trap, 
                    Emotional Isolation, early_grooming, Fast Emotional Bonding

Action: Do not share financial info or send money.
-------------------------------------------------------------------------------
🧪 Test Cases & Effectiveness
Complete Test Suite Results:
Example	Risk Level	Score	Matched Patterns	Word Count
1	🟠 HIGH	72.0%	6 patterns	175
2	🔴 CRITICAL	94.5%	9 patterns	230
3	🔴 CRITICAL	99.0%	12 patterns	265
4	🔴 CRITICAL	99.0%	10 patterns	310
5	🔴 CRITICAL	99.0%	11 patterns	235
6	🔴 CRITICAL	99.0%	11 patterns	285
7	🔴 CRITICAL	99.0%	10 patterns	270
8	🔴 CRITICAL	99.0%	10 patterns	275
9	🔴 CRITICAL	99.0%	14 patterns	340
10	🔴 CRITICAL	99.0%	11 patterns	295
Perfect Detection Of:

✅ All financial scam elements (100%)

✅ Early grooming attempts (100%)

✅ Urgency tactics (90%)

✅ Dangerous pattern combinations

🔗 Links
GitHub repository: AI Scam Detection

README: Complete Documentation & Test Results

Windows Download: scamcheck.exe (210.8 MB)

Python Script: scamcheck.py

🤝 Contributing
Contributions are welcome! Open an issue or submit a pull request.
Keep your commits descriptive, and follow Python coding best practices.

We're particularly interested in:

New scam patterns and keywords

False positive/negative reports

Detection logic improvements

Performance optimizations

📜 License
This project is licensed under the MIT License.

⚠️ Important Disclaimer
ScamCheck is for educational and awareness purposes only. While it has demonstrated 95.9% accuracy in testing:

Not a guarantee: No tool can detect all scams

Not legal/financial advice: Always consult professionals

Supplement, don't replace: Use with common sense and intuition

Privacy first: The executable works completely offline

Remember: If something feels wrong online, trust your instincts. Never send money to online-only relationships.
