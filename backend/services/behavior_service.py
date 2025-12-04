import json
import datetime
from collections import defaultdict
from flask import request, jsonify
from utils.mongo_util import mongo_util


class Behavior_Service:

    @staticmethod
    def track_behavior():
        data = request.json
        email = data.get("email")
        time_interval = data.get("time_interval")

        if not email or time_interval is None:
            return jsonify({"error": "email and time_interval required"}), 400

        entry = {
            "time_interval": time_interval,
            "timestamp": datetime.datetime.now()
        }

        updated = mongo_util.update_one(
            "behavior_logs",
            {"email": email},
            {"$push": {"patterns": entry}}
        )

        if updated.matched_count == 0:
            mongo_util.insert_one("behavior_logs", {
                "email": email,
                "patterns": [entry]
            })

        return jsonify({"message": "behavior logged successfully"}), 201


    # -----------------------------
    # Group behavior by minute
    # -----------------------------
    @staticmethod
    def _group_by_minute(patterns):
        buckets = defaultdict(list)
        for p in patterns:
            ts = p["timestamp"]
            minute_key = ts.replace(second=0, microsecond=0)
            buckets[minute_key].append(p["time_interval"])
        return buckets


    # -----------------------------
    # Manhattan distance function
    # -----------------------------
    @staticmethod
    def manhattan_distance(baseline, sample):
        return (
            abs(baseline["avg_interval"] - sample["avg_interval"]) +
            abs(baseline["variance"] - sample["variance"]) +
            abs(baseline["std_dev"] - sample["std_dev"]) +
            abs(baseline["score"] - sample["score"]) +
            abs(baseline["total_samples"] - sample["total_samples"])
        )


    # -----------------------------
    # Behavior scoring per minute + anomaly detection
    # -----------------------------
    @staticmethod
    def score_behavior():
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "email required"}), 400

        user_log = mongo_util.find_one("behavior_logs", {"email": email})

        if not user_log or "patterns" not in user_log:
            return jsonify({"error": "no data found"}), 404

        patterns = user_log["patterns"]

        # Group by 1-minute windows
        buckets = Behavior_Service._group_by_minute(patterns)

        results = []
        historical_windows = []  # store all previous window feature profiles

        for window_start, intervals in sorted(buckets.items()):
            if len(intervals) == 0:
                continue

            avg = sum(intervals) / len(intervals)
            variance = sum((x - avg) ** 2 for x in intervals) / len(intervals)
            std_dev = variance ** 0.5
            score = max(0, 100 - std_dev)

            current_sample = {
                "avg_interval": avg,
                "variance": variance,
                "std_dev": std_dev,
                "score": round(score, 2),
                "total_samples": len(intervals)
            }

            # -----------------------------
            # ADAPTIVE BASELINE:
            # Average all previous windows
            # -----------------------------
            if len(historical_windows) > 0:
                baseline = {
                    "avg_interval": sum(w["avg_interval"] for w in historical_windows) / len(historical_windows),
                    "variance": sum(w["variance"] for w in historical_windows) / len(historical_windows),
                    "std_dev": sum(w["std_dev"] for w in historical_windows) / len(historical_windows),
                    "score": sum(w["score"] for w in historical_windows) / len(historical_windows),
                    "total_samples": sum(w["total_samples"] for w in historical_windows) / len(historical_windows)
                }

                # Manhattan distance
                dist = Behavior_Service.manhattan_distance(baseline, current_sample)

                # Threshold → tune depending on system
                THRESHOLD = 15
                auth = "genuine" if dist < THRESHOLD else "anomaly"

            else:
                # First window → no baseline yet
                baseline = None
                dist = None
                auth = "baseline_established"

            # Append current window to history AFTER scoring
            historical_windows.append(current_sample)

            results.append({
                "window_start": window_start.isoformat(),
                "features": current_sample,
                "baseline": baseline,
                "distance": dist,
                "auth": auth
            })

        return jsonify(results), 200
