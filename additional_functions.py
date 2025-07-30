import random


NUMBER_OF_WORDS = 4
ENCODING = 'utf-8'


def make_words_dict(path_to_file, splitter='--'):
    """Split document and return dict.

    File structure: <word>{splitter}<word>
    """
    f_dict = {}
    with open(path_to_file, encoding=ENCODING, errors='replace') as file:
        for string in file:
            if not string or string == '\n':
                continue
            left, right = string.split(splitter)
            f_dict[left.strip()] = right.strip()
    return f_dict


def choose_random_words(file, num_choise=NUMBER_OF_WORDS, splitter='--'):
    """Return pack with random words."""
    data_container = make_words_dict(file, splitter=splitter)
    data_container_keys = list(data_container.keys())

    random_main_words = random.sample(data_container_keys, k=num_choise)
    random_translate_words = [
        data_container[word] for word in random_main_words
    ]
    pack_of_words = zip(random_main_words, random_translate_words)
    return list(pack_of_words)


async def set_language_mode(message):
    """Set language."""
    if message == 'English':
        return 'English.txt'
    return 'Kazakh.txt'


if __name__ == "__main__":
    filename = 'The Picture of Dorian Gray.txt'
    print(choose_random_words(filename, NUMBER_OF_WORDS))
