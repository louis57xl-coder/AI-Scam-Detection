import re
import sys
import time
import torch
from collections import defaultdict
from typing import Dict, List
from transformers import pipeline

# ──────────────────────────── ADVANCED BEHAVIORAL DETECTOR ────────────────────────────
class AdvancedBehavioralDetector:
    """
    Enhanced pig-butchering/romance scam detector with sliding windows,
    document-wide AI emotion scanning, and early-stage grooming detection.
    All original keywords preserved.
    """

    def __init__(self):
        # ──── PRESERVED ORIGINAL KEYWORDS & PATTERNS ────
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

        # ──── NEW: Early-stage grooming / hook indicators ────
        self.red_flags['early_grooming'] = [
            # Mild flattery & interest
            "caught my eye", "warm smile", "genuine smile", "you looked really kind", "handsome", "cutie", "really insightful",
            "know your stuff", "seem really smart", "thought of you", "made me think of you", "for some reason it made me think of",
            "you seem special", "you seem like someone who", "had to message you",
            # Loneliness / new in town / seeking connection
            "lonely", "kinda lonely", "feeling lonely", "bit lonely", "new in town", "just moved", "recently moved",
            "adjusting to life here", "could use a friendly chat", "kinda lonely and could use", "need a friend", "someone to talk to",
            # Early finance/crypto seeding (subtle)
            "crypto trader", "passive income", "digital asset", "blockchain", "low-risk", "smart financial moves",
            "investment tips", "finance and investments", "digital assets", "portfolio manager", "generate really nice passive income",
            "international finance", "financial freedom", "successful trading"
        ]

        # ──── PRESERVED ORIGINAL SCAM PATTERNS ────
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

        # ──── WEIGHTS (original preserved + new early category) ────
        self.SCAM_PATTERN_WEIGHTS = {
            "Wrong-Number Hook": 0.50,
            "Fast Emotional Bonding": 0.60,
            "Lifestyle Flex": 0.65,
            "Authority / Mentorship": 0.70,
            "Small Test Ask": 0.60,
            "Romance + Future Promise": 0.70,
            "Trust Reversal": 0.80,
            "Withdrawal Trap": 0.95,
            "Emotional Isolation": 0.85,
            # New: medium weight for early grooming (needs combination to spike)
            "early_grooming": 0.45
        }

        print("Initializing AI Safeguards (Sliding Context Analysis)...")
        self.device = 0 if torch.cuda.is_available() else -1
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
            device=self.device
        )

    def clean_text(self, text: str) -> str:
        """Remove emojis, multiple spaces, and normalize for better matching."""
        # Remove emojis and non-word symbols (preserves basic punctuation)
        text = re.sub(r'[^\w\s,.!?\'\-]', '', text)
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _get_windows(self, text: str, window_size: int = 60, overlap: int = 20) -> List[str]:
        words = text.split()
        if len(words) <= window_size:
            return [text]
        return [" ".join(words[i:i + window_size]) for i in range(0, len(words), window_size - overlap)]

    def _get_full_ai_score(self, text: str) -> float:
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        max_peak = 0.0
        for chunk in chunks:
            if len(chunk.strip()) < 10:
                continue
            results = self.emotion_analyzer(chunk)[0]
            scores = {res['label']: res['score'] for res in results}
            # Boost on fear (urgency) + joy (flattery) + sadness (loneliness)
            peak = max(
                scores.get('fear', 0),
                scores.get('joy', 0),
                scores.get('sadness', 0) * 0.7   # sadness is common in grooming
            )
            if peak > max_peak:
                max_peak = peak
        return max_peak

    def compute_window_probability(self, text_window: str):
        text_lower = text_window.lower()
        matched = []

        # Check all categories (original + new)
        for cat, patterns in self.scam_patterns.items():
            if any(re.search(r'\b' + re.escape(p) + r'\b', text_lower) for p in patterns):
                matched.append(cat)

        for cat, keywords in self.red_flags.items():
            if any(kw in text_lower for kw in keywords):
                matched.append(cat)

        if not matched:
            return 0.0, []

        # Weighted scoring
        weighted_hits = [c for c in matched if c in self.SCAM_PATTERN_WEIGHTS]
        if not weighted_hits:
            return 0.05, matched

        # Take highest single weight, then multiplier for combinations
        prob = max(self.SCAM_PATTERN_WEIGHTS[cat] for cat in weighted_hits)
        n = len(set(weighted_hits))

        if n == 2:
            prob *= 1.35
        elif n == 3:
            prob *= 1.60
        elif n >= 4:
            prob *= 1.90

        # Extra boost for dangerous combos (original + new early ones)
        dangerous_combos = [
            {"Lifestyle Flex", "Authority / Mentorship"},
            {"Romance + Future Promise", "Small Test Ask"},
            {"Withdrawal Trap", "Trust Reversal"},
            # New: very common early pig-butchering pattern
            {"early_grooming", "money_request"},
            {"early_grooming", "Lifestyle Flex"},
            {"early_grooming", "Authority / Mentorship"}
        ]

        for combo in dangerous_combos:
            if combo.issubset(set(weighted_hits)):
                prob = max(prob, 0.82 if "early_grooming" in combo else 0.94)

        if "Withdrawal Trap" in weighted_hits:
            prob = max(prob, 0.97)

        return min(prob, 0.99), list(set(matched))

    def analyze(self, text: str) -> Dict:
        cleaned = self.clean_text(text)
        windows = self._get_windows(cleaned)
        results = [self.compute_window_probability(w) for w in windows]

        kw_prob = max([r[0] for r in results]) if results else 0.0
        all_matched = list(set(cat for r in results for cat in r[1]))

        ai_prob = self._get_full_ai_score(cleaned)

        # Hybrid fusion (original logic preserved)
        primary_score = max(kw_prob, ai_prob)
        if kw_prob > 0.4 and ai_prob > 0.4:
            final_prob = primary_score + (1 - primary_score) * 0.6
        else:
            final_prob = primary_score

        final_prob = min(0.99, final_prob)

        return {
            'probability': final_prob,
            'percent': round(final_prob * 100, 1),
            'matched_categories': all_matched
        }

# ──────────────────────────── UI FUNCTIONS (unchanged) ────────────────────────────
def banner(title: str):
    print("\n" + "="*80 + f"\n{title.center(80)}\n" + "="*80 + "\n")

def print_risk_interpretation(prob: float, categories):
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

def main():
    try:
        detector = AdvancedBehavioralDetector()
        banner("PIG-BUTCHERING & ROMANCE SCAM ANALYZER (V3 - Early Grooming Enhanced)")
        while True:
            print("Paste the suspected message below:")
            print("PRESS CONTROL C TO EXIT")
            msg = sys.stdin.readline().strip()
            if not msg:
                continue

            print("\nAnalyzing behavioral markers across document windows...\n")
            result = detector.analyze(msg)
            print_risk_interpretation(result['probability'], result['matched_categories'])
            print("-" * 80 + "\n")

    except KeyboardInterrupt:
        print("\n\nSystem Closed. Stay safe.")
        sys.exit(0)

if __name__ == "__main__":
    main()