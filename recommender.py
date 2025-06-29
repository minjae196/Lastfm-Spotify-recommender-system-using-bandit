from lastfm_client import LastFMClient
import random
import math
from collections import deque

class Recommender:
    def __init__(self, bandit):
        self.bandit = bandit
        self.lastfm = LastFMClient()
        self.previous_ids = set()
        self.recently_recommended = deque(maxlen=3)
        # recommender.py
    def recommend_personal_top(self, top_k=10):
        all_ids = list(self.bandit.rewards.keys())  # ThompsonSampling 기준
        results = []
        
        for item_id in all_ids:
            score = self.bandit.get_score(item_id)
            try:
                name, artist = item_id.split(" - ")
            except:
                continue  # 형식이 안 맞는 경우 스킵

            results.append({
                "id": item_id,
                "name": name,
                "artist": {"name": artist},
                "score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
        
    def gather_candidates(self, track_name, artist_name, tag=None):
        tracks = []
        seen_ids = set()

        sim_tracks = self.lastfm.get_similar_tracks(track_name, artist_name, limit=30)
        tracks.extend(sim_tracks)

        artist_tracks = self.lastfm.get_top_tracks_by_artist(artist_name, limit=20)
        tracks.extend(artist_tracks)

        if tag:
            tag_tracks = self.lastfm.get_top_tracks_by_tag(tag, limit=20)
            tracks.extend(tag_tracks)

        unique = []
        for t in tracks:
            tid = f"{t['name']} - {t['artist']['name']}"
            if tid not in seen_ids:
                t["id"] = tid
                seen_ids.add(tid)
                unique.append(t)
        return unique

    def recommend_bulk(self, mode, track_name="", artist_name="", tag=""):
        candidates = self.gather_candidates(track_name, artist_name, tag if mode == "tag" else None)

        results = []
        for t in candidates:
            t["score"] = self.bandit.get_score(t["id"])

            # Penalize recently recommended tracks
            if t["id"] in self.recently_recommended:
                t["score"] *= 0.5

            # Add stronger randomness to diversify score tie cases
            t["score"] += random.uniform(-0.2, 0.2)
            results.append(t)

        epsilon = 0.2
        if random.random() < epsilon:
            selected = random.sample(results, k=10)
        else:
            results.sort(key=lambda x: x["score"], reverse=True)
            selected = results[:10]

        # Update recent recommendation memory
        self.previous_ids = set(r["id"] for r in selected)
        self.recently_recommended.extend(self.previous_ids)

        return selected

    def give_feedback(self, track, reward):
        self.bandit.update(track["id"], reward)
