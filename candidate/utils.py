"""
Utilities
"""


def sanitize_data(data):
    assert type(data) is list, "expected list"
    result = []
    for item in data:
        interim = {}
        for key, value in item.items():
            interim[key] = value.strip()
        result.append(interim)
    return result
