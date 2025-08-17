import requests
from bs4 import BeautifulSoup
import subprocess

def duckduckgo_search(query, pages=1):
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    for page in range(pages):
        params = {
            'q': query,
            's': page * 30
        }
        url = "https://html.duckduckgo.com/html"
        res = requests.post(url, data=params, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.select('.result__title a'):
            title = a.text.strip()
            link = a['href']
            results.append(f"{title}\n{link}")

    return "\n\n".join(results[:5])  # Top 5 results

def ask_ollama(prompt, model='mistral'):
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=prompt)
    return stdout.strip()

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("🔍 Searching DuckDuckGo...")
        web_context = duckduckgo_search(user_input)

        full_prompt = f"""You are an AI chatbot using real-time web data.

Web search results:\n{web_context}

Based on the above, answer the user's question:
{user_input}
"""
        print("🤖 Thinking...")
        response = ask_ollama(full_prompt)
        print(f"\nAI:\n{response}\n")

if __name__ == "__main__":
    main()
