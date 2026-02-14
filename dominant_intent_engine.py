from collections import Counter

class DominantIntentTracker:
    def __init__(self):
        self.window = []

    def add(self, intent):
        self.window.append(intent)
        if len(self.window) > 5:
            self.window.pop(0)

    def dominant(self):
        if not self.window:
            return None
        count = Counter(self.window)
        return count.most_common(1)[0][0]

tracker = DominantIntentTracker()
