import string

def assert_ignore_whitespace_string_equal(a, b):
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return a.translate(mapping) == b.translate(mapping)