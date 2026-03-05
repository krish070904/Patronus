def verify_answer(answer, chunks):

    if answer is None:
        return False

    number = answer["answer"].split()[0]

    number = number.replace(",", "")

    for chunk in chunks:

        text = chunk["text"].replace(",", "")

        if number in text:
            return True

    return False 