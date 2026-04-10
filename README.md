# 🚀 Discord Sharding Simulation: A Dev Log

---

## 🎨 Interactive Architecture Dashboard
I built a completely interactive, custom UI to visualize this entire 10-day journey.

👉 **[View the Live Dashboard (index.html)](index.html)** 👈

**What's in the Dashboard?**
- **Live Simulator:** Watch how messages route dynamically under our `User`, `Channel`, and `Hash` strategies.
- **Chaos Engineering:** Manually turn shards off (simulate hardware failure) and watch the "Eventual Inconsistency" metrics in real time.
- **Dynamic Charting:** See throughput scaling over time, how load imbalance destroys shards, and how hash sharding fixes it perfectly.
- **Post-Mortem Analysis:** See a beautifully-designed summary of the "Aha!" moments from the 10-day sprint.

---

## 🛠 Project Overview
This repository isn't just code; it's a journey from **Day 1 (The Single-Box Fantasy)** to **Day 9 (The Distributed Reality)**. I've built this to simulate what happens when a chat app goes from "quiet lobby" to "viral stadium."

---

## 📅 Day-by-Day Breakdown

| Day | File | Topic |
|-----|------|-------|
| 1-2 | `day1_day2_system_thinking.md` | System Thinking & Architecture Planning |
| 3 | `day3_basic_system.py` | Basic Single-Server Chat System |
| 4 | `day4_scaling_awareness.py` | Scaling Awareness & Bottleneck Detection |
| 5 | `day5_intro_shards.py` | Introduction to Sharding |
| 6 | `day6_user_sharding.py` | User-Based Sharding |
| 7 | `day7_channel_sharding.py` | Channel-Based Sharding |
| 8 | `day8_hash_sharding.py` | Hash-Based Sharding (The Hotspot Killer) |
| 9 | `day9_stress_failure.py` | Stress Testing & Failure Simulation |
| 📱 UI | `index.html` | Custom Interactive Dashboard |

---

## 🔑 Key Milestones

### Day 8: Hash-Based Sharding (`day8_hash_sharding.py`)
After watching the "Influencer Hotspot" (`day6`) and "Viral Channel Crash" (`day7`) destroy naive sharding strategies, Day 8 introduces the fix: **hash the `message_id`**.

- **The Insight:** Every message has a unique UUID. By hashing *that*, instead of `user_id` or `channel_id`, we scatter messages perfectly evenly across all shards.
- **The Result:** Even with 9,000 messages hammering a single channel, no single shard takes more than ~34% of the load. Hotspot problem: *solved*.
- **The Hidden Cost:** Since messages for one channel are now spread across all shards, fetching a channel's history requires a **cross-shard fan-out query**. We traded write hotspots for read complexity.

### Day 9: Stress & Failure Simulation (`day9_stress_failure.py`)
With Hash-Based Sharding as our foundation, Day 9 stress-tests the system under real-world chaos.

- **Phase 1 — Normal Load:** 2,000 messages pumped through 3 shards to verify baseline distribution.
- **Phase 2 — Cross-Shard Query:** Simulated fetching recent messages from a specific channel, requiring all 3 shards to be queried and merged by timestamp.
- **Phase 3 — System Evolution (The Modulo Nightmare):** Demonstrated that scaling from 3 → 6 shards with simple `hash % num_shards` breaks all existing routing. Every message would need re-homing — a massive migration crisis. *Consistent Hashing* is the real answer here.
- **Phase 4 — Chaos Engineering (Shard Failure):** Killed Shard 1 mid-traffic and observed the fallout: ~1/3 of writes fail silently, and cross-shard reads return incomplete history — "Eventual Inconsistency" in the flesh.

---

## 🕵️‍♂️ Post-Mortem: The Final Analysis (Day 10)

### 1. The First to Fall: Who hit the wall?
In my **User-Based Sharding** test (`day6_user_sharding.py`), the "Influencer Shard" died first. Imagine 10,000 fans sending messages to one user. Because I routed by `user_id`, one server was doing all the heavy lifting while the other two were basically on vacation. Classic hotspot.

In the **Channel-Based Sharding** test (`day7_channel_sharding.py`), the "Viral Channel Shard" (the cricket final scenario) crashed the system. Even with 10 shards, if everyone is in one channel, you're back to Square One: one box trying to handle 100% of the traffic.

### 2. The Great Deception: The strategy that *felt* right.
**Channel-based sharding** is the ultimate trap. It *feels* perfect because messages for one channel stay on one box, making "Get Last 50 Messages" super fast. But as soon as a single channel goes viral, that box is toast. It's a strategy that's great for 99% of the day and a disaster for the 1% that actually matters.

### 3. Scaling Pains: Growing from 3 → 10 Shards.
If I just use a simple modulo (`hash % total_shards`), adding shards is a nightmare. Changing the "total shards" from 3 to 10 moves almost every message to a "new home." In a real system, this would trigger a massive data migration that would probably crash the system anyway. 
*Note to self: Look into "Consistent Hashing" next time!*

### 4. When a Shard Dies (Chaos Engineering).
Simulated in `day9_stress_failure.py`:
- **Writes:** 1/3rd of our users suddenly can't send messages. The system feels broken.
- **Reads:** This is the weirdest part. When you query for "Recent Messages," you get gaps. It's like reading a book with every 3rd page ripped out. This "Eventual Inconsistency" is the price we pay for speed, but man, it makes for a frustrated user.

