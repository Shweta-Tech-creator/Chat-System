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
    print("--- Day 3: Naive System Simulation ---")
    server = ChatServer()
    
    # Simulating 10 users sending messages (works fine)
    print("Simulating 10 users sending 5 messages each...")
    for user_id in range(1, 11):
        for _ in range(5):
            msg = Message(user_id, 1, "Hello from Day 3")
            server.send_message(msg)

    server.stats()
    print("System operating normally. Data stored in global array.")
