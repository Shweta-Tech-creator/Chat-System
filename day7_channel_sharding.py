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

class ChannelShardManager(ShardManager):
    def get_shard(self, channel_id):
        return self.shards[channel_id % len(self.shards)]

    def send_message(self, message):
        shard = self.get_shard(message.channel_id)
        shard.store(message)

def check_hotspots(manager):
    total_messages = sum(len(s.messages) for s in manager.shards)
    if total_messages == 0: return

    for s in manager.shards:
        percentage = (len(s.messages) / total_messages) * 100
        if percentage > 50:
            print(f"[HOTSPOT WARNING] Shard {s.id} is taking {percentage:.1f}% of the load!")

if __name__ == "__main__":
    print("--- Day 7: Channel-Based Sharding ---")
    manager = ChannelShardManager(3)
    
    print("Simulating normal traffic and ONE viral channel (event spike)...")
    
    # 50 normal channels
    for _ in range(1000):
        channel_id = random.randint(1, 50)
        msg = Message(random.randint(1, 1000), channel_id, "normal chat")
        manager.send_message(msg)

    # Viral channel (e.g. Cricket Final) channel_id = 100
    viral_channel_id = 100
    for _ in range(8000):
        # Many users, but SAME channel
        msg = Message(random.randint(1, 10000), viral_channel_id, "viral chat")
        manager.send_message(msg)

    for shard in manager.shards:
        print(f"Shard {shard.id}: {len(shard.messages)} messages")

    check_hotspots(manager)

    print("\nObservation:")
    print("Even though users are distributed, relying on channel_id as the routing key creates a massive hotspot.")
    print("Because discord limits conversations to channels, a viral channel (like a live event) funnels 100% of its traffic into a single shard, crashing it.")
