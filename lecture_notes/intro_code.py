path = 'data/books/the_sign_of_the_four.txt'


def find_potential_names(path_to_file, titles=['Mr.', 'Mrs.', 'Ms.', 'Dr.']):
    with open(path_to_file, encoding='utf-8') as fp:
        all_txt = fp.read()

    all_txt = all_txt.replace('\n', ' ')
    words = all_txt.split()

    potential_names = []
    for idx, word in enumerate(words):
        if (word[0] == word[0].upper()) and (words[idx - 1] in titles):
            potential_names.append(word)
    return set(potential_names)


def count_words(path_to_file):
    word_freq = {}
    with open(path_to_file, encoding='utf-8') as fp:
        all_txt = fp.read()

    all_txt = all_txt.replace('\n', ' ')
    words = all_txt.split()
    for word in words:
        word_freq.setdefault(word, 0)
        word_freq[word] += 1

    return word_freq


if __name__ == '__main__':
    name_freqs = count_words(path)
    print(name_freqs)
