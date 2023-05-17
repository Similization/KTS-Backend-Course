from typing import Optional

__all__ = (
    'find_shortest_longest_word',
)


def find_shortest_longest_word(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    В переданном тексте вернуть слово имеющее наименьшую и наибольшую длину.
    Если такого слова нет - вернуть None
    """
    shortest_word, longest_word = None, None
    for word in text.split():
        if shortest_word is None or len(word) < len(shortest_word):
            shortest_word = word
        if longest_word is None or len(word) > len(longest_word):
            longest_word = word
    return shortest_word, longest_word


print(find_shortest_longest_word('привет       всем'))
