AI Scam Detection App
An advanced NLP pipeline leveraging Deep Learning and Large Language Models (LLMs) to identify relationship fraud and "pig-butchering" (investment-romance) scams in text-based communications.

🚀 Overview
This application provides a multi-layered analysis of text messages to detect sophisticated social engineering tactics. Unlike simple keyword filters, this project uses a hybrid approach:

Linguistic Analysis: Identifying high-pressure tactics and emotional manipulation.

Behavioral Scoring: Detecting patterns typical of pig-butchering (e.g., pivot to investment, crypto-solicitation).

Probabilistic Risk Assessment: Delivering a confidence-weighted score to the end user.

🛠️ Technologies & Library Stack
Machine Learning & Deep Learning
PyTorch: Primary framework for building and deploying neural network architectures (e.g., Transformers or LSTMs).

scikit-learn: Utilized for data preprocessing, TF-IDF vectorization, and baseline classification models (SVM, Random Forest).

pandas & NumPy: The backbone for structured data manipulation and numerical operations.

Large Language Model (LLM) Integration
Hugging Face (Transformers/Diffusers): Integration of pre-trained models (like BERT or RoBERTa) for high-accuracy text embeddings and sequence classification.

OpenAI API: Leveraged for complex semantic reasoning and nuanced fraud assessment summaries.

LangChain: Used to orchestrate LLM chains, manage prompts, and handle context memory for multi-message conversations.

Development Environment
Jupyter Notebooks: Used for exploratory data analysis (EDA), feature engineering, and iterative model validation.
