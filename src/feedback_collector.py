import json
import os
from datetime import datetime

class FeedbackCollector:
    def __init__(self, feedback_file='models/feedback_data.json'):
        self.feedback_file = feedback_file
        self.ensure_feedback_file()
    
    def ensure_feedback_file(self):
        os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)
    
    def save_feedback(self, features, predicted_class, user_correction, text=""):
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'predicted': predicted_class,
            'correct': user_correction,
            'text': text,
            'features': features.tolist() if hasattr(features, 'tolist') else list(features)
        }
        
        try:
            with open(self.feedback_file, 'r') as f:
                feedbacks = json.load(f)
        except:
            feedbacks = []
        
        feedbacks.append(feedback_entry)
        
        with open(self.feedback_file, 'w') as f:
            json.dump(feedbacks, f, indent=2)
        
        return len(feedbacks)
    
    def load_feedback(self):
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_feedback_count(self):
        return len(self.load_feedback())

