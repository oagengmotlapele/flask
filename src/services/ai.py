import json
import os
import uuid
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# === FILE SETTINGS ===
JSON_PATH = "chat_history.json"

# Load existing chat history if exists
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r") as f:
        chat_store = json.load(f)
else:
    chat_store = {}

# === ASK USERNAME ===
username = input("Enter your username: ").strip()

# Initialize or load user's chat sessions
if username not in chat_store:
    chat_store[username] = {}

# === START NEW OR CONTINUE ===
existing_sessions = list(chat_store[username].keys())

if existing_sessions:
    print("\nYour past sessions:")
    for sid in existing_sessions:
        print(f"- {sid}")
    choice = input("Type session ID to continue or type 'new' to start a new conversation: ").strip()
else:
    choice = 'new'

# === START SESSION ===
if choice.lower() == "new":
    conv_id = f"{username}-{uuid.uuid4().hex[:24]}"
    chat_store[username][conv_id] = []
else:
    conv_id = choice if choice in chat_store[username] else f"{username}-{uuid.uuid4().hex[:24]}"
    if conv_id not in chat_store[username]:
        chat_store[username][conv_id] = []

print(f"\n📄 Conversation ID: {conv_id}")
print("Chat started. Type 'exit' to stop.\n")

# === MODEL SETUP ===
llm = OllamaLLM(model='qwen:0.5b')

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Always remember what the user said before."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

        # Load full conversation history into memory
        for entry in chat_store[username][session_id]:
            if "user" in entry:
                store[session_id].add_user_message(entry["user"])
            elif "bot" in entry:
                store[session_id].add_ai_message(entry["bot"])

    return store[session_id]


chat_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# === CHAT LOOP ===
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chat ended.")
        break
    try:
        # Save user message
        chat_store[username][conv_id].append({"user": user_input})

        response = chat_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": conv_id}}
        )

        print("Bot:", response)

        # Save bot response
        chat_store[username][conv_id].append({"bot": response})

        # Persist to JSON
        with open(JSON_PATH, "w") as f:
            json.dump(chat_store, f, indent=4)
    except Exception as e:
        print("Error:", e)
