import re
import sys
import time
import torch
from collections import defaultdict
from typing import Dict
from transformers import pipeline

# ──────────────────────────── SCAM DETECTION CLASS ────────────────────────────
class BehavioralScamDetector:
    """
    Detects potential romance and pig-butchering scams in text messages
    by analyzing behavioral patterns, emotional manipulation, and investment prompts.
    """
    def __init__(self):
        # ALL ORIGINAL KEYWORDS PRESERVED
        self.red_flags = {
            'love_bombing_intensity': [
                "can't stop thinking","my everything","heart beats for","deep connection","you complete me","our souls one","never felt this","dream of you",
                "lost without you","miss you terribly","be with forever","we are meant","my destiny","long to see","think about future","life changed meeting",
                "heart is yours","my soulmate","every moment with","keep me awake","want to marry","always on mind","can't live without","my angel","my treasure",
                "love at first","crazy about you","feel so lucky","always together","my dearest love","you're my world","love forever","my only one",
                "my darling","my shining star","my perfect match","my sweet heart","love my life","always thinking of","you are amazing","love our bond",
                "my life partner","my heart belongs","love and cherish","forever yours","feel so connected","our love destiny","love you always",
                "my one true","heart beats faster","dream of future","think of you","can't forget you","our hearts one","love you deeply","my true love",
                "always remember you","my beautiful angel","love growing strong","my love forever","treasured moments","deeply in love","love you truly",
                "you are special","can't stop loving","my love angel","my love light","eternal love","always by your","love is real","you complete me",
                "my perfect love","love with all","love and cherish","my heart you","love you more","my soul mate","my heart smiles","always yours","my heart longs",
                "love beyond words","love you madly","my precious one","my guiding star","my happiness","my inspiration","my heart beats","my love forevermore",
                "love from heart","my one love","heart full love","love of life","love deeply","my sweetest love","love always with","my cherished one",
                "you are mine","love without end","my heart's desire","my eternal love","my perfect one","love always true","my beloved","my heart sings"
            ],
            'money_request': [
                "send money","need money","gift card","bitcoin","crypto","investment","loan","fees","fund transfer","western union",
                "inheritance","lottery","sweepstakes","urgent transfer","advance fee","help transfer","transfer funds","pay tax","secret account",
                "receive money","pay fees","bank transfer","wire funds","crypto wallet","bitcoin transfer","usd transfer","foreign exchange",
                "gift voucher","paypal payment","digital transfer","fund deposit","send bitcoin","cash transfer","loan request","emergency fund",
                "pay upfront","investment opportunity","early withdrawal","bank deposit","transfer immediately","secure transfer","deposit funds",
                "money urgently","send cash","fund check","confirm transfer","account deposit","payment needed","quick transfer","transfer money now",
                "loan advance","urgent payment","receive funds","tax payment","wire transfer","digital wallet","transfer bitcoin","paypal cash","crypto cash",
                "bank fees","send funds","payment confirmation","urgent transaction","transfer required","send usd","send crypto","loan funding",
                "money request","account verification","investment deposit","financial transfer","payment process","secure funds","send gift card",
                "transfer verification","funds release","send currency","urgent wire","check transfer","deposit usd","crypto funding","bank wire","transfer check",
                "receive payment","secure transfer now","payment needed asap","bitcoin deposit","digital cash","pay advance","send fast","urgent funds",
                "wire cash","account transfer","crypto transaction","loan transfer","transfer payment","funds request","send money today","receive transfer",
                "urgent deposit","fast money transfer","paypal transfer","loan check","send funds fast","transfer confirmation","digital payment"
            ],
            'urgency_crisis': [
                "urgent","emergency","right now","limited window","expires","act fast","time sensitive","last chance","immediately","hurry",
                "deadline","critical","important now","must respond","don't delay","final notice","top priority","asap","risk losing",
                "time running out","act quickly","respond now","last opportunity","limited time","urgent response","before deadline","act immediately",
                "time critical","final call","respond fast","last warning","quick action","priority now","don't wait","urgent matter","final opportunity",
                "act without delay","time urgent","deadline approaching","emergency action","urgent request","final deadline","response needed",
                "critical situation","must act","immediate action","time sensitive deal","urgent notice","hurry up","time running short",
                "priority message","quick response","limited offer","urgent task","respond asap","act fast now","final chance","time critical deal",
                "emergency transfer","urgent payment","asap request","final warning","deadline imminent","top urgency","act now please",
                "time is short","urgent deadline","respond immediately","hurry response","critical request","final notice alert","limited time only",
                "priority action","immediate response","urgent action needed","deadline alert","act quickly now","time sensitive request",
                "respond quickly","last call","hurry up now","critical alert","emergency response","asap action","urgent attention","priority urgent"
            ],
            'geo_patterns': [
                "nigeria","ghana","kenya","egypt","morocco","algeria","tunisia","south africa","india","pakistan","bangladesh",
                "philippines","malaysia","indonesia","china","vietnam","thailand","brazil","mexico","overseas","foreign country"
            ]
        }

        self.scam_patterns = {
            "Wrong-Number Hook": ["wrong number","are we still meeting","glad fate connected us","mistyped number","hope not bother"],
            "Fast Emotional Bonding": ["known you for years","only been days","connection is special","immediate bond","feel destiny"],
            "Lifestyle Flex": ["checked my investments","financial freedom","luxury lifestyle","new car purchase","expensive watch","successful trading"],
            "Authority / Mentorship": ["my uncle taught me","private trading method","low risk","mentor showed me","exclusive opportunity"],
            "Small Test Ask": ["small amount","see how it works","step by step","test deposit","quick trial"],
            "Romance + Future Promise": ["finally meet you","build a life together","without money stress","dream house together","marry soon"],
            "Trust Reversal": ["thought you trusted me","would never lie","betray you","question loyalty","misunderstood"],
            "Withdrawal Trap": ["verification step","before withdrawal","everything unlocked","confirm account","release funds","account locked"],
            "Emotional Isolation": ["outsiders","jealous","only one who's honest","trust no one","keep secret"]
        }

        self.SCAM_PATTERN_WEIGHTS = {
            "Wrong-Number Hook": 0.50,
            "Fast Emotional Bonding": 0.60,
            "Lifestyle Flex": 0.65,
            "Authority / Mentorship": 0.70,
            "Small Test Ask": 0.60,
            "Romance + Future Promise": 0.70,
            "Trust Reversal": 0.80,
            "Withdrawal Trap": 0.95,
            "Emotional Isolation": 0.85
        }

        print("Initializing AI Safeguards (Loading Pre-trained Models)...")
        self.device = 0 if torch.cuda.is_available() else -1
        self.emotion_analyzer = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base", 
            return_all_scores=True,
            device=self.device
        )

    def detect_counts(self, text: str):
        text = text.lower()
        counts = defaultdict(int)
        for cat, patterns in self.scam_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    counts[cat] += 1
        for cat, keywords in self.red_flags.items():
            for kw in keywords:
                if kw in text:
                    counts[cat] += 1
        return counts

    def compute_probability(self, counts):
        """
        Calculates probability with a NON-LINEAR boost for multiple categories.
        """
        matched = list(counts.keys())
        weighted_hits = [cat for cat in matched if cat in self.SCAM_PATTERN_WEIGHTS]
        
        if not weighted_hits:
            return 0.05 if counts else 0.0

        # Start with the HIGHEST single category weight as a baseline
        prob = max([self.SCAM_PATTERN_WEIGHTS[cat] for cat in weighted_hits])
        
        # APPLY MULTIPLIERS FOR VOLUME:
        # Instead of adding weights, we multiply the baseline to reach high numbers fast.
        n = len(weighted_hits)
        if n == 2: prob *= 1.35
        if n == 3: prob *= 1.60
        if n >= 4: prob *= 1.90
        
        # Hard-coded dangerous combinations
        dangerous_sets = [
            {"Lifestyle Flex", "Authority / Mentorship"},
            {"Romance + Future Promise", "Small Test Ask"},
            {"Withdrawal Trap", "Trust Reversal"}
        ]
        for combo in dangerous_sets:
            if combo.issubset(weighted_hits): 
                prob = max(prob, 0.94)
        
        # Withdrawal Traps are almost always 95%+
        if "Withdrawal Trap" in weighted_hits:
            prob = max(prob, 0.97)

        return min(prob, 0.99)

    def get_ai_score(self, text: str) -> float:
        if len(text.strip()) < 5: return 0.0
        results = self.emotion_analyzer(text[:512])[0]
        scores = {res['label']: res['score'] for res in results}
        # In scams, high 'Fear' (Urgency) or high 'Joy' (Flattery) are red flags
        return max(scores.get('fear', 0), scores.get('joy', 0))

    def analyze(self, text: str) -> Dict:
        counts = self.detect_counts(text)
        kw_prob = self.compute_probability(counts)
        ai_prob = self.get_ai_score(text)
        
        # HYBRID LOGIC REVISION:
        # Instead of averaging (which lowers scores), we take the max 
        # and treat the other as a 'Confidence Boost'.
        primary_score = max(kw_prob, ai_prob)
        secondary_score = min(kw_prob, ai_prob)
        
        # If both systems agree there is risk, boost the primary score significantly
        if kw_prob > 0.4 and ai_prob > 0.4:
            # Formula: moves the score halfway from its current position to 1.0
            final_prob = primary_score + (1 - primary_score) * 0.6
        else:
            final_prob = primary_score
            
        final_prob = min(0.99, final_prob)
        return {
            'probability': final_prob,
            'percent': round(final_prob * 100, 1),
            'matched_categories': list(counts.keys())
        }

# ──────────────────────────── UI FUNCTIONS ────────────────────────────
def banner(title:str):
    print("\n"+"="*80)
    print(title.center(80))
    print("="*80+"\n")

def print_risk_interpretation(prob:float, categories):
    percent = prob * 100
    if percent < 30:
        banner(f"🟢  LOW RISK — {percent:.1f}%")
    elif percent < 60:
        banner(f"🟡  MEDIUM RISK — {percent:.1f}%")
    elif percent < 85:
        banner(f"🟠  HIGH RISK — {percent:.1f}%")
    else:
        banner(f"🔴  CRITICAL DANGER — {percent:.1f}%")
        
    if categories:
        print(f"Matched Indicators: {', '.join(categories)}")
    print("\nAction: Do not share financial info or send money.")

# ──────────────────────────── MAIN ────────────────────────────
def main():
    try:
        detector = BehavioralScamDetector()
        banner("PIG-BUTCHERING & ROMANCE SCAM ANALYZER")
        while True:
            print("Paste the suspected message below:")
            msg = sys.stdin.readline().strip()
            if not msg: continue
            
            print("\nAnalyzing behavioral markers...\n")
            time.sleep(0.3)
            result = detector.analyze(msg)
            print_risk_interpretation(result['probability'], result['matched_categories'])
            print("-" * 80 + "\n")
            
    except KeyboardInterrupt:
        print("\n\nSystem Closed. Stay safe.")
        sys.exit(0)

if __name__ == "__main__":
    main()
