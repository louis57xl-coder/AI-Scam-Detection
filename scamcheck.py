import re
from collections import defaultdict
from typing import Dict
import sys
import time
import torch
from torch import nn
from transformers import DistilBertTokenizerFast, DistilBertModel

# ──────────────────────────── SCAM DETECTION CLASS ────────────────────────────
class BehavioralScamDetector:
    """
    Detects potential romance and pig-butchering scams in text messages
    by analyzing behavioral patterns, emotional manipulation, and investment prompts.
    """
    def __init__(self):
        # Expanded keywords (~100 per category)
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
                "philippines","malaysia","indonesia","china","vietnam","thailand","brazil","mexico","overseas","foreign country",
                "africa region","middle east","south asia","east asia","latin america","caribbean region","remote country","unknown origin",
                "western africa","central africa","north africa","southern africa","southeast asia","south america","far east","near east",
                "overseas transaction","foreign account","international bank","offshore account","remote location","global region","outside country",
                "distant country","foreign transfer","international transfer","worldwide","across borders","cross border","foreign exchange","offshore transfer",
                "overseas payment","international transaction","remote bank","foreign client","global transfer","cross country","abroad","distant bank",
                "international account","foreign investment","overseas client","offshore bank","global account","remote location transfer","foreign region",
                "international cash","overseas fund","cross border payment","global fund","foreign currency","offshore transaction","abroad payment",
                "international cash transfer","global investment","remote client","foreign finance","cross country transfer","overseas transaction request",
                "international loan","foreign banking","remote transfer","overseas banking","global client","cross border transaction","foreign wealth",
                "overseas investment","international fund","remote finance","foreign fund","global transaction","offshore finance","overseas remittance",
                "foreign transfer request","international investment","remote banking","offshore investment","cross country fund","global remittance",
                "foreign money","overseas money","international wealth","remote account","offshore wealth","global finance","foreign exchange deal",
                "overseas payment transfer","international payment","remote currency","foreign assets","offshore account fund","global client fund"
            ]
        }

        # Pig-butchering patterns remain unchanged
        self.scam_patterns = {
            "Wrong-Number Hook": ["wrong number","are we still meeting","glad fate connected us","mistyped number","hope not bother","apologies wrong contact","unexpected message","reached by mistake","accidental text","contact error"],
            "Fast Emotional Bonding": ["known you for years","only been days","connection is special","immediate bond","feel destiny","soulmate feeling","instant attraction","deep feelings","instant trust","meant to meet"],
            "Lifestyle Flex": ["checked my investments","financial freedom","another great day","luxury lifestyle","new car purchase","expensive watch","fine dining","private villa","wealthy life","successful trading"],
            "Authority / Mentorship": ["my uncle taught me","private trading method","low risk","mentor showed me","exclusive opportunity","insider tips","financial advisor","secret method","proven strategy","personal guidance"],
            "Small Test Ask": ["small amount","see how it works","step by step","first transfer","test deposit","quick trial","tiny investment","sample run","demo payment","initial check"],
            "Romance + Future Promise": ["finally meet you","build a life together","without money stress","dream house together","marry soon","travel together","happy future","joint account","shared plans","family together"],
            "Trust Reversal": ["thought you trusted me","would never lie","betray you","question loyalty","misunderstood","trust broken","not honest","deceived","double-crossed","let down"],
            "Withdrawal Trap": ["verification step","before withdrawal","everything unlocked","confirm account","release funds","account locked","final check","secure transfer","unlock money","authorize transaction"],
            "Emotional Isolation": ["outsiders","jealous","only one who's honest","trust no one","keep secret","private matter","hidden agenda","protect from others","avoid sharing","confide only me"]
        }

        # Pattern weights remain unchanged
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

        # PyTorch setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self.bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.bert_model.eval()
        self.bert_model.to(self.device)
        self.classifier = nn.Sequential(
            nn.Linear(self.bert_model.config.hidden_size,64),
            nn.ReLU(),
            nn.Linear(64,1),
            nn.Sigmoid()
        ).to(self.device)

    # Detection, probability, and PyTorch scoring functions remain the same
    def detect_counts(self,text:str):
        text=text.lower()
        counts=defaultdict(int)
        for cat,patterns in self.scam_patterns.items():
            for pattern in patterns:
                if re.search(pattern,text):
                    counts[cat]+=1
        for cat,keywords in self.red_flags.items():
            for kw in keywords:
                if kw in text:
                    counts[cat]+=1
        return counts

    def compute_probability(self,counts):
        base_prob=0.25
        matched=list(counts.keys())
        weighted_hits=[cat for cat in matched if cat in self.SCAM_PATTERN_WEIGHTS]
        prob=base_prob+sum([self.SCAM_PATTERN_WEIGHTS[cat] for cat in weighted_hits])
        n=len(weighted_hits)
        if n>=2: prob*=1.7
        if n>=3: prob*=2.0
        if n>=4: prob*=2.3
        if n>=5: prob*=2.8
        if n>=6: prob*=3.2
        dangerous_sets=[
            {"Lifestyle Flex","Authority / Mentorship"},
            {"Romance + Future Promise","Lifestyle Flex"},
            {"Trust Reversal","Emotional Isolation"},
            {"Withdrawal Trap","Trust Reversal"},
            {"Fast Emotional Bonding","Small Test Ask","Lifestyle Flex"}
        ]
        for combo in dangerous_sets:
            if combo.issubset(weighted_hits): prob=max(prob,0.92)
        if "Withdrawal Trap" in weighted_hits: prob=max(prob,0.97)
        return min(prob,0.99)

    def pytorch_probability(self,text):
        with torch.no_grad():
            tokens=self.tokenizer(text,return_tensors="pt",truncation=True,max_length=128).to(self.device)
            outputs=self.bert_model(**tokens)
            cls_emb=outputs.last_hidden_state[:,0,:]
            prob=self.classifier(cls_emb).item()
        return prob

    def analyze(self,text:str)->Dict:
        counts=self.detect_counts(text)
        kw_prob=self.compute_probability(counts)
        pt_prob=self.pytorch_probability(text)
        final_prob=min(0.99,kw_prob+pt_prob*0.5)
        return {
            'probability':final_prob,
            'percent':round(final_prob*100,1),
            'matched_categories':list(counts.keys())
        }

# ──────────────────────────── UI FUNCTIONS ────────────────────────────
def banner(title:str):
    print("\n"+"="*80)
    print(title.center(80))
    print("="*80+"\n")

def print_risk_interpretation(prob:float,categories):
    percent=prob*100
    if percent<30:
        banner(f"🟢  PROBABLY OK — Probability {percent:.1f}%")
        print("Meaning: Low likelihood of scam based on this message alone")
    elif percent<50:
        banner(f"🟡  YOU SHOULD BE CONCERNED — Probability {percent:.1f}%")
        print("Meaning: Early grooming or probing behavior detected")
    elif percent<75:
        banner(f"🟠  SCAM IS LIKELY — Probability {percent:.1f}%")
        print("Meaning: Multiple scam indicators present")
    else:
        banner(f"🔴  YOU ARE BEING SCAMMED — Probability {percent:.1f}%")
        print("Meaning: High-confidence scam behavior detected")
    if categories:
        print("\nMatched Scam Categories:")
        for cat in categories:
            print(f" - {cat}")
    print("\nRecommended Action: Protect yourself and do not send money.")
    print("Reminder: To close the application, press Ctrl+C at any time.\n")

# ──────────────────────────── MAIN LOOP ────────────────────────────
def main():
    detector=BehavioralScamDetector()
    banner("ROMANCE & PIG-BUTCHERING SCAM DETECTOR")
    print("Paste your message below to analyze it. Press Ctrl+C to exit.\n")
    while True:
        try:
            print("Paste your message (press Enter when done):")
            msg=sys.stdin.readline().strip()
        except KeyboardInterrupt:
            print("\n\nStay safe. Goodbye.\n")
            sys.exit(0)
        if not msg: continue
        print("\nAnalyzing...\n")
        time.sleep(0.5)
        result=detector.analyze(msg)
        print_risk_interpretation(result['probability'],result['matched_categories'])
        print(f"Estimated Scam Probability: {result['percent']}%")
        print("-"*80)
        print("Reminder: To close the application, press Ctrl+C.\n")

if __name__=="__main__":
    main()
