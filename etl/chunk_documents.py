def chunk_documents(pages):

    chunks = []

    for page in pages:

        text = page["text"]

        parts = text.split("\n")

        for part in parts:

            if len(part) > 50:

                chunks.append({
                    "page": page["page"],
                    "text": part
                })

    return chunks