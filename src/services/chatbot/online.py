import json
import os
from huggingface_hub import InferenceClient

class MultiUserChat:
    def __init__(self, model, token, storage_file="chats.json"):
        self.client = InferenceClient(model=model, token=token)
        self.storage_file = storage_file
        self.load_chats()
        self.current_user = None
        self.current_chat_id = None

    def load_chats(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                self.chats = json.load(f)
        else:
            self.chats = {}

    def save_chats(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.chats, f, indent=4)

    def login(self, username):
        if username not in self.chats:
            self.chats[username] = {}
        self.current_user = username
        self.current_chat_id = None
        print(f"👋 Welcome back, {username}!")

    def list_chats(self):
        """List all chats for the current user."""
        if not self.current_user:
            print("⚠️ Login first!")
            return
        chats = list(self.chats[self.current_user].keys())
        if not chats:
            print("ℹ️ No chats found. Type 'new_chat' to start one.")
        else:
            print(f"📂 Chats for {self.current_user}:")
            for cid in chats:
                print(f"  - {cid}")

    def select_chat(self, chat_id):
        """Select an existing chat."""
        if chat_id in self.chats.get(self.current_user, {}):
            self.current_chat_id = chat_id
            print(f"✅ Selected {chat_id}")
        else:
            print("⚠️ Chat ID not found. Use 'list_chats' to see available chats.")

    def new_chat(self):
        if self.current_user is None:
            print("⚠️ Login first!")
            return
        chat_id = f"chat_{len(self.chats[self.current_user]) + 1}"
        self.chats[self.current_user][chat_id] = []
        self.current_chat_id = chat_id
        print(f"🆕 New chat started → {chat_id}")

    def send_message(self, user_message, max_tokens=100):
        if not self.current_user or not self.current_chat_id:
            print("⚠️ No active chat. Use 'list_chats' and 'select_chat' or start 'new_chat'.")
            return

        # Save user message
        self.chats[self.current_user][self.current_chat_id].append({"user": "you", "msg": user_message})

        # Build message history
        messages = [
            {"role": "user", "content": m["msg"]}
            if m["user"] == "you"
            else {"role": "assistant", "content": m["msg"]}
            for m in self.chats[self.current_user][self.current_chat_id]
        ]

        # Call Hugging Face
        response = self.client.chat_completion(
            messages=messages,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message["content"]

        # Save AI reply
        self.chats[self.current_user][self.current_chat_id].append({"user": "65AI", "msg": reply})

        # Persist data
        self.save_chats()

        return reply


# ----------------- Run App -----------------
if __name__ == "__main__":
    bot = MultiUserChat(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        token="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"
    )

    print("🤖 Welcome to 65AI Chat!")
    print("Commands: login | list_chats | select_chat | new_chat | exit")
    print("After selecting chat, just type your message.")

    while True:
        cmd = input("👉 ").strip()

        if cmd.lower() == "exit":
            print("👋 Goodbye!")
            break
        elif cmd.lower() == "login":
            username = input("Enter username: ").strip()
            bot.login(username)
        elif cmd.lower() == "list_chats":
            bot.list_chats()
        elif cmd.lower() == "new_chat":
            bot.new_chat()
        elif cmd.lower().startswith("select_chat"):
            _, chat_id = cmd.split(maxsplit=1)
            bot.select_chat(chat_id)
        else:
            if not bot.current_user:
                print("⚠️ Please login first.")
            else:
                reply = bot.send_message(cmd)
                if reply:
                    print(f"65AI: {reply}")
