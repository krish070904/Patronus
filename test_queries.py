import requests

queries = [
 "What is the total number of jobs reported?",
 "Compare pure-play firms in South-West vs national average",
 "What CAGR is required to reach 17000 jobs?"
]

for q in queries:
    r = requests.post(
        "http://127.0.0.1:8000/query",
        json={"query": q}
    )
    print(q)
    print(r.json())