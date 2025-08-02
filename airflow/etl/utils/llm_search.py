import requests
import json
from concurrent.futures import ThreadPoolExecutor
from libs.app_config.config import OLLAMA_URL, LLM_MODEL
from ddgs import DDGS

# Search with duckduckgo and extract 20 snippets
def get_funding_snippets(company_name: str) -> str:
    query = f'"{company_name.lower().strip()}" "startup" "funding" "y combinator"'
    snippets = []

    with DDGS() as ddg:
        for r in ddg.text(query, region="us-en",
                        safesearch="off", max_results=20):
            snippets.append("( website title: " + r["title"] + " | " + "snippet: " + r["body"] + " )")

    return "\n".join(snippets)

# Gets a response from specified model by feeding the snippet texts
def get_llm_response(company_name: str, snippets_text: str) -> str:
    url = OLLAMA_URL
    response = requests.post(
        url,
        json={
            'model': LLM_MODEL,
            'prompt': f"""
            You are an information extractor. Your job is to extract funding data for a company.

            TASK:
            - Extract the **funding amount** for the company "{company_name}" from the data and text below, CONVERT TO USD.
            - Respond with a **SINGLE INTEGER**.
            - Do NOT include words, explanations, dollar signs, or commas.
            - If no funding is mentioned, respond with **0**.

            EXAMPLES:
            - "Raised $12M" → 12000000
            - "Received 40 million dollars in Series A" → 40000000
            - "No funding info found" → 0

            Now analyze the following data snippets, each enclosed in brackets. Prioritize information from well-known titles first:

            {snippets_text}
            """,
            "options": {
                "temperature": 0.1
            }
        },
        timeout=200,
        stream=True
    )

    full_response = ""
    for chunk in response.iter_lines():
        if chunk:
            data = json.loads(chunk.decode('utf-8'))
            full_response += data.get("response", "")
    
    return full_response

# Turns a string into a valid number (returns 0 if no valid number can be created)
def clean_number(string: str="0") -> float:
    idx = None      # first index of a number
    last = None     # last index of a number

    # Search for first and last nums
    for i in range(len(string)):
        if string[i].isnumeric():
            last = i
            if idx is None:
                idx = i

    # End early if no numbers found
    if idx is None:
        return 0
    last += 1

    # Check thousand
    if last < len(string) and string[last] == "k":
        return float((string[idx:last]).replace(",", "")) * (10**3)
    
    # Check million
    if last < len(string) and string[last] == "m":
        return float((string[idx:last]).replace(",", "")) * (10**6)
    
    # Check billion (you never know one day)
    elif last < len(string) and string[last] == "b":
        return float((string[idx:last]).replace(",", "")) * (10**9)
    
    # Evaluate as usual after checking all possible cases
    return float((string[idx:last]).replace(",", ""))

# Tries to convert the LLM response into a valid number
def clean_response(resp: str="0") -> int:
    words = resp.strip().lower().replace('*', '').replace('"', '').replace("'", '').split()
    largest = clean_number(words[0])

    # Case 1: a response containing something like $3.27 M or $20 Million
    # Case 2: a response containing something like $3.7M or 2.1M
    # Case 3: a normal response containing something like 300000 (or $300000)
    # We can handle all cases actually in one pass by being greedy and pray that the highest number is the correct one, This would take O(c) time and space
    for i in range(1, len(words)):
        
        # Only check potential candidates (words that don't start with a letter)
        if not words[i][0].isalpha():
            largest = max(largest, clean_number(words[i]))

        # Otherwise check for million or billion
        elif words[i] in {"m", "million"}:
            num = clean_number(words[i-1])

            # if the LLM is not being a dickhead this number should be correct
            if num and num < 1000:
                largest = max(largest, num*(10**6))
        
        elif words[i] in {"b", "billion"}:
            num = clean_number(words[i-1])
            if num and num < 1000:
                largest = max(largest, num*(10**9))
        
    # if we somehow get a huge number then ignore it
    return int(largest) if 10000 < int(largest) < 10**11 else 0

def one_sample(company_name: str) -> int:
    try:
        snippets = get_funding_snippets(company_name)
        resp = get_llm_response(company_name, snippets)
        return clean_response(resp)
    except Exception as e:
        print("Sample failed:", e)
        return 0

# Take a sample size of 3, and return the median
def get_funding(company_name: str) -> int:
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda _: one_sample(company_name), range(3)))
    
    results.sort()
    return results[1]  # median