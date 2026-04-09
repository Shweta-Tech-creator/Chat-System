import random
import hashlib
import uuid

class Message:
    def __init__(self, user_id, channel_id, content):
        self.message_id = str(uuid.uuid4())
        self.user_id = user_id
        self.channel_id = channel_id
        self.content = content

class Shard:
    def __init__(self, shard_id):
        self.id = shard_id
        self.messages = []

    def store(self, message):
        self.messages.append(message)


class ShardManager:
    def __init__(self, num_shards):
        self.shards = [Shard(i) for i in range(num_shards)]

class HashShardManager(ShardManager):
    def get_shard(self, key):
        h = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        return self.shards[h % len(self.shards)]

    def send_message(self, message):
        # We choose to hash the 'message_id' to get perfectly uniform distribution.
        # This prevents both the "influencer" and "viral channel" hotspots.
        shard = self.get_shard(message.message_id)
        shard.store(message)

def check_hotspots(manager):
    total_messages = sum(len(s.messages) for s in manager.shards)
    if total_messages == 0: return

    for s in manager.shards:
        percentage = (len(s.messages) / total_messages) * 100
        if percentage > 50:
            print(f"[HOTSPOT WARNING] Shard {s.id} is taking {percentage:.1f}% of the load!")

if __name__ == "__main__":
    print("--- Day 8: Hash-Based Sharding ---")
    manager = HashShardManager(3)
    
    print("Simulating viral channel to see if hashing fixes it...")
    
    viral_channel_id = 100
    for _ in range(9000):
        # Many users, same channel
        msg = Message(random.randint(1, 10000), viral_channel_id, "viral chat")
        manager.send_message(msg)

    for shard in manager.shards:
        print(f"Shard {shard.id}: {len(shard.messages)} messages")

    check_hotspots(manager)

    print("\nObservation:")
    print("By hashing the message_id instead of user_id or channel_id, we achieved perfect distribution!")
    print("Reasoning: Every message has a unique ID, so the hash distributes them evenly across all shards, completely avoiding hotspots.")
    print("HOWEVER, this choice creates a new hidden complexity: fetching the history of a specific channel now requires querying ALL shards, because its messages are scattered everywhere.")
