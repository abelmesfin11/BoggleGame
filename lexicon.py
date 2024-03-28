def read_lexicon(filename):
    """Reads in a lexicon of valid Boggle words from a file.
    
    DO NOT CHANGE.

    Parameters
    ----------
    filename : str
        The filename containing the valid words (one word per line)
    
    Returns
    -------
    set[str]
        The set of words found in the file.
    """
    lex = []
    with open(filename) as reader:
        for line in reader:
            lex.append(line.strip().upper())
    return set(lex)