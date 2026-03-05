def extract_firm_stats(tables):

    pure_play = None
    total_firms = None

    for table in tables:

        df = table["table"]

        for row in df.values:

            row_text = " ".join([str(cell).lower() for cell in row if cell])

            if "pure" in row_text and "play" in row_text:
                for cell in row:
                    if str(cell).isdigit():
                        pure_play = int(cell)

            if "total" in row_text:
                for cell in row:
                    if str(cell).isdigit():
                        total_firms = int(cell)

    return pure_play, total_firms