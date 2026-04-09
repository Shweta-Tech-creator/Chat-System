import time

class Message:
    def __init__(self, user_id, channel_id, content):
        self.user_id = user_id
        self.channel_id = channel_id
        self.content = content

class ChatServer:
    def __init__(self):
        self.messages = []
    
    def send_message(self, message):
        self.messages.append(message)

    def stats(self):
        print("Total messages:", len(self.messages))

if __name__ == "__main__":
    print("--- Day 4: Scaling Awareness ---")
    server = ChatServer()
    
    print("Simulating 10,000 users each sending 500 messages (Massive Load)...")
    start_time = time.time()
    
    # 5,000,000 messages total
    try:
        for i in range(5_000_000):
            user_id = (i % 10000) + 1
            msg = Message(user_id, 1, "Spam message")
            server.send_message(msg)
            
            if i > 0 and i % 1_000_000 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {i} messages in {elapsed:.2f} seconds.")
    except MemoryError:
        print("Memory Error: The server array crashed due to massive memory consumption.")
        
    final_time = time.time() - start_time
    server.stats()
    print(f"Total time taken: {final_time:.2f} seconds.")
    
    print("\nObservation:")
    print("The system slows down dramatically and consumes huge amounts of memory.")
    print("In a real environment, Python list append is fast, but managing millions of objects")
    print("eats up gigabytes of RAM in a single process. Memory grows endlessly without eviction.")
