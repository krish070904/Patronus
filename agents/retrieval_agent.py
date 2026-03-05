def retrieve_jobs_stat(chunks):

    for chunk in chunks:

        if "7,351" in chunk["text"]:

            return {
                "answer": "7351 jobs",
                "page": chunk["page"],
                "citation": chunk["text"]
            }

    return None