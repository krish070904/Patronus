def plan(query):

    q = query.lower()

    if "cagr" in q or "growth rate" in q:
        return "math"

    if "compare" in q or "concentration" in q:
        return "table"

    return "retrieve"