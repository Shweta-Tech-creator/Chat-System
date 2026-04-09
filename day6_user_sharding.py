import random

class Message:
    def __init__(self, user_id, channel_id, content):
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

class UserShardManager(ShardManager):
    def get_shard(self, user_id):
        return self.shards[user_id % len(self.shards)]

    def send_message(self, message):
        shard = self.get_shard(message.user_id)
        shard.store(message)

def check_hotspots(manager):
    total_messages = sum(len(s.messages) for s in manager.shards)
    if total_messages == 0: return

    for s in manager.shards:
        percentage = (len(s.messages) / total_messages) * 100
        if percentage > 50:
            print(f"[HOTSPOT WARNING] Shard {s.id} is taking {percentage:.1f}% of the load!")

if __name__ == "__main__":
    print("--- Day 6: User-Based Sharding ---")
    manager = UserShardManager(3)
    
    print("Simulating normal traffic and one 'influencer' sending 5000 messages...")
    
    # Normal users
    for _ in range(1000):
        # 100 random normal users
        msg = Message(random.randint(1, 100), 1, "normal chat")
        manager.send_message(msg)

    # Influencer user (Say user_id = 999) goes viral
    influencer_id = 999
    for _ in range(5000):
        msg = Message(influencer_id, 1, "influencer message")
        manager.send_message(msg)

    for shard in manager.shards:
        print(f"Shard {shard.id}: {len(shard.messages)} messages")

    check_hotspots(manager)

    print("\nObservation:")
    print("Because the influencer sticks to their assigned shard (Shard 0), that specific shard is overloaded.")
    print("User-based sharding fails to distribute load evenly when some users are significantly more active than others.")
