REAL = r"(?:\d+(?:\.\d*)?|\.\d+)"
FRACTION = r"(?:\d+/\d+)"
EXACT_REAL = rf"(?:{REAL}|{FRACTION})"
# Shared by scanner (is_complex_number) and numbers.parse_number_token / Complex.
COMPLEX_LITERAL_RE = rf"([+-]?{EXACT_REAL})?([+-](?:{EXACT_REAL})?)i"
