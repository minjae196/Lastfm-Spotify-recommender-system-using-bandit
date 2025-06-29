# bandit/thompson_sampling.py
from bandit.base import Bandit
import random

class ThompsonSampling(Bandit):
    def __init__(self):
        self.rewards = {}

    def update(self, item_id, reward):
        success, failure = self.rewards.get(item_id, (1, 1))
        if reward == 1.0:
            success += 1
        else:
            failure += 1
        self.rewards[item_id] = (success, failure)

    def get_value(self, item_id):
        success, failure = self.rewards.get(item_id, (1, 1))
        return success / (success + failure)

    def get_score(self, item_id):
        success, failure = self.rewards.get(item_id, (1, 1))
        score = random.betavariate(success, failure)
        print(f"🎯 탐험/이용 {item_id} | Beta({success},{failure}) → score={score:.2f}")
        return score