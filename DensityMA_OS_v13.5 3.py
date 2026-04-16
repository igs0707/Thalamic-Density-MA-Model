from collections import deque
import re
import random
from typing import Dict

class DensityMA_OS:
    """
    Density × MA OS v13.5 (English Edition)
    - When relation_MA is low: extremely short responses
    - Answer ONLY what is asked
    - No self-talk or situation explanations
    - Response length naturally scales with Q
    """
    def __init__(self, alpha=0.978, max_D=0.65, d_decay=0.89):
        self.personal_MA = 0.0          # Your "true self" from X posts
        self.relation_MA = 0.0          # Relationship MA with this user (starts near 0)
        self.topic_MA: Dict[str, float] = {}
        self.alpha = alpha
        self.max_D = max_D
        self.d_decay = d_decay
        
        # Example: Extracted from X post tendencies (replace with actual parser in real use)
        self.like_vector: Dict[str, float] = {
            "morning activity": 0.78, "shellfish": 0.71, "iron": 0.65, "health": 0.58,
            "walk": 0.52, "nutrition": 0.48, "routine": 0.45
        }
        self.dislike_vector: Dict[str, float] = {
            "politics": 0.68, "complaint": 0.72, "boast": 0.60, "grumbling": 0.55
        }
        
        self.history = deque(maxlen=200)
        self.novelty_buffer = deque(maxlen=7)
        self.last_topic = ""
        self.topic_repeat_count = 0
        self.step_count = 0
        
        print("=== Density × MA OS v13.5 started ===")
        print("Low relation mode: super short responses")

    def extract_main_topic(self, text: str) -> str:
        text = text.lower()
        words = re.findall(r'[一-龥ぁ-んァ-ンa-zA-Z0-9]{2,}', text)
        return words[0] if words else "general"

    def get_like_boost(self, topic: str) -> float:
        like_score = self.like_vector.get(topic, 0.0)
        dislike_score = self.dislike_vector.get(topic, 0.0)
        topic_ma = self.topic_MA.get(topic, 0.12)
        boost = like_score * (topic_ma ** 1.85)
        boost -= dislike_score * 0.65
        return max(-0.45, min(1.15, boost))

    def update_topic_ma(self, topic: str, D_eff: float):
        if topic not in self.topic_MA:
            self.topic_MA[topic] = 0.13
        self.topic_MA[topic] = self.alpha * self.topic_MA[topic] + (1 - self.alpha) * D_eff * 1.12
        
        if topic == self.last_topic:
            self.topic_repeat_count += 1
            if self.topic_repeat_count >= 4:
                self.topic_MA[topic] *= 0.958
        else:
            self.topic_repeat_count = 1
        self.last_topic = topic

    def calculate_D(self, user_input: str):
        length_score = min(1.0, len(user_input) / 88)
        context_score = min(1.0, len(self.history) / 55)
        topic = self.extract_main_topic(user_input)
        raw_D = (length_score + context_score) * 0.52
        D = min(self.max_D, raw_D * self.d_decay)
        return D, topic

    def step(self, user_input: str):
        D, topic = self.calculate_D(user_input)
        self.novelty_buffer.append(topic)
        novelty = len(set(self.novelty_buffer)) / max(1, len(self.novelty_buffer))
        
        boost = self.get_like_boost(topic)
        D_eff = D * (1.0 + boost * 0.82) * (0.88 + novelty * 0.12)
        
        # Separate updates: personal_MA (X brain) and relation_MA (this chat)
        self.personal_MA = self.alpha * self.personal_MA + (1 - self.alpha) * D_eff * 0.6
        self.relation_MA = self.alpha * self.relation_MA + (1 - self.alpha) * D_eff * 0.4
        
        self.update_topic_ma(topic, D_eff)
        
        Q = D_eff * (self.personal_MA + self.relation_MA + 1e-8)
        
        self.history.append(user_input)
        self.step_count += 1
        
        return {
            "Q": Q,
            "topic": topic,
            "boost": boost,
            "topic_ma": self.topic_MA.get(topic, 0)
        }

    def generate_response(self, Q: float) -> str:
        intensity = Q + self.relation_MA * 0.8
        
        if intensity < 0.55 or self.relation_MA < 0.25:
            return random.choice(["Yeah.", "Got it.", "Hmm.", "I see."])
        
        elif intensity < 0.80:
            return random.choice([
                "Yeah, makes sense.",
                "Right.",
                "What do you think?",
                "How about that?"
            ])
        
        else:
            return random.choice([
                "Nice.",
                "What does that feel like?",
                "Interesting.",
                "Tell me more."
            ])

    def chat(self, user_input: str) -> str:
        if not user_input.strip():
            return "Huh?"
            
        result = self.step(user_input)
        return self.generate_response(result["Q"])


# ====================== HOW TO USE ======================
if __name__ == "__main__":
    os = DensityMA_OS()
    # os.load_like_vector_from_x("your_oshi_username")   # ← Put X username here
    
    while True:
        user = input("You: ")
        if user.lower() in ["exit", "quit"]:
            break
        print("OS  :", os.chat(user))