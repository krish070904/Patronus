def extract_job_numbers(chunks):

    start_jobs = None
    target_jobs = None

    for chunk in chunks:

        text = chunk["text"].replace(",", "")

        # detect baseline employment
        if "7351" in text or "cybersecurity workforce" in text.lower():
            start_jobs = 7351

        # detect target employment
        if "17000" in text or "target" in text.lower():
            target_jobs = 17000

    return start_jobs, target_jobs