import random
import hashlib
import uuid
import time

class Message:
    def __init__(self, user_id, channel_id, content):
        self.message_id = str(uuid.uuid4())
        self.user_id = user_id
        self.channel_id = channel_id
        self.content = content
        self.timestamp = time.time()
        
    def __repr__(self):
        return f"<Msg | Ch:{self.channel_id} | Usr:{self.user_id}>"

class Shard:
    def __init__(self, shard_id):
        self.id = shard_id
        self.messages = []
        self.is_active = True

    def store(self, message):
        if not self.is_active:
            raise Exception(f"Shard {self.id} is down! Write failed.")
        self.messages.append(message)


class HashShardManager:
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shards = [Shard(i) for i in range(num_shards)]

    def get_shard(self, key):
        h = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        return self.shards[h % self.num_shards]

    def send_message(self, message):
        shard = self.get_shard(message.message_id)
        try:
            shard.store(message)
        except Exception as e:
            # Failure handling
            print(f"[ERROR] {e}")

    # Cross-Shard Query logic
    def fetch_recent_messages(self, channel_id, limit=10):
        print(f"Executing Cross-Shard Query for channel {channel_id}...")
        results = []
        shards_checked = 0
        
        for shard in self.shards:
            shards_checked += 1
            if not shard.is_active:
                print(f"[WARN] Shard {shard.id} is down. Partial data only.")
                continue
            
            # Find messages in this shard belonging to the channel
            shard_msgs = [m for m in shard.messages if m.channel_id == channel_id]
            results.extend(shard_msgs)
        
        # Sort by timestamp to merge them correctly
        results.sort(key=lambda x: x.timestamp, reverse=True)
        print(f"Checked {shards_checked} shards.")
        return results[:limit]

def simulate(manager, num_users=1000, num_messages=5000):
    for i in range(num_messages):
        user_id = random.randint(1, num_users)
        channel_id = random.randint(1, 10) # 10 distinct channels

        msg = Message(user_id, channel_id, "stress test msg")
        manager.send_message(msg)
        # sleep slightly to give unique timestamps
        time.sleep(0.0001)

if __name__ == "__main__":
    print("--- Day 9: Stress + Failure Simulation ---")
    
    # 1. Normal Setup & Load
    print("\n[Phase 1] Normal Load (3 Shards)")
    manager = HashShardManager(3)
    simulate(manager, num_messages=2000)
    for shard in manager.shards:
        print(f"Shard {shard.id}: {len(shard.messages)} messages")

    # 2. Cross Shard Query
    print("\n[Phase 2] Cross-Shard Query Test")
    target_channel = 5
    recent = manager.fetch_recent_messages(target_channel, limit=3)
    print(f"Recent messages for channel {target_channel}: {recent}")

    # 3. Increase Shards (System Evolution)
    print("\n[Phase 3] System Evolution (3 -> 6 shards attempt)")
    print("If we change num_shards from 3 to 6, modulo `h % num_shards` changes!")
    print("Past hashes wouldn't map correctly anymore, forcing a massive data migration (rebalancing).")

    # 4. Failure Simulation
    print("\n[Phase 4] Failure Simulation")
    print("Simulating Shard 1 going down...")
    manager.shards[1].is_active = False
    
    print("Sending spike traffic with a downed shard...")
    simulate(manager, num_messages=1000)
    
    print("Attempting to query channel history during failure:")
    recent_failure = manager.fetch_recent_messages(target_channel, limit=5)
    print(f"Recent messages returned: {len(recent_failure)} (Missing some due to downed shard!)")
