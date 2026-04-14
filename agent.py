import anthropic
from tavily import TavilyClient
from datetime import date

client = anthropic.Anthropic(api_key="your-api-key-here")

# The search tool
def search_web(query):
    print(f"Searching for: {query}")
    tavily = TavilyClient(api_key="your-api-key-here")
    results = tavily.search(query=query, max_results=3)
    output = ""
    for r in results["results"]:
        output += f"- {r['title']}: {r['content']}\n"
    return output

system_prompt = f"""You are a research agent with access to web search.
f"Today's date is {date.today()}."

To search the web you MUST write EXACTLY this format on its own line:
SEARCH: your query here

Rules:
- NEVER use XML tags or function calls to search
- ONLY use the SEARCH: format above
- You can search multiple times if needed
- When you have fully answered the goal, write DONE on its own line
- NEVER answer before receiving search results. ALWAYS search first, then answer.
- Only answer based on what search results tell you, not what you already know."""

messages = [
    {"role": "user", "content": "Why is bitcoin surging today?"}
]

max_steps = 5
step = 0

while step < max_steps:
    step += 1
    print(f"\n--- Step {step} ---")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )

    reply = response.content[0].text
    print(f"Claude: {reply}")

    messages.append({"role": "assistant", "content": reply})

    # Check if Claude wants to search
    if "SEARCH:" in reply:
        query = reply.split("SEARCH:")[1].strip().split("\n")[0]
        results = search_web(query)
        print(f"Results: {results}")
        messages.append({"role": "user", "content": f"Search results:\n{results}"})

    # Check if Claude is done
    elif "DONE" in reply:
        print("\nAgent complete!")
        break

    else:
        messages.append({"role": "user", "content": "Please continue."})

print(f"\nFinished in {step} step(s).")