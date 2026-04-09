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
        # We start with 3 shards
        self.shards = [Shard(i) for i in range(num_shards)]

    def send_message(self, message):
        # Intentionally incomplete as per Day 5
        print("ERROR: Don't know where to route this message yet!")
        pass

if __name__ == "__main__":
    print("--- Day 5: Introduce Shards ---")
    manager = ShardManager(3)
    
    msg = Message(1, 1, "Hello shard 1")
    manager.send_message(msg)
    
    print("\nObservation:")
    print("Data structures are separated per server (shard), so there is no global 'self.messages'.")
    print("But without a routing strategy, the 'send_message' doesn't know which shard should accept the data.")
