def validate(file):
    """
    Validates a `.txt` or `.csv` file by checking if each line is formatted as 'WORD, DEFINITION'.

    The function reads through each line in the text file and ensures that each line contains a word 
    and a corresponding definition separated by a comma.

    Args:
        file: The uploaded `.txt` or `.csv` file object to be validated.

    Returns:
        bool: True if all lines in the file are correctly formatted; otherwise, False.
    """

    try:
        for line in file:
            line = line.decode('utf-8').strip()
            if ',' not in line:
                return False
            word, definition = line.split(',', 1)
            if not word or not definition:
                return False
        return True
    except:
        return False


