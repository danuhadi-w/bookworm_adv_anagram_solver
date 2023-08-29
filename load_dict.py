from itertools import permutations
from collections import Counter
import time

start_time = time.time()

class AnagramSolver:
    def load_words(self):
        with open('assets/words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())

        return valid_words

    def can_form_word(self, word, letters):
        word_count = Counter(word)
        letters_count = Counter(letters)
        for letter, count in word_count.items():
            if count > letters_count[letter]:
                return False
        return True

    def solve_anagram(self, anagram, english_words):
        available_words = set()
        for word in english_words:
            if len(word) < 5:
                continue
            if self.can_form_word(word, anagram):
                available_words.add(word)

        available_words = sorted(available_words, key=len, reverse=True)
        end_time = time.time()
        print('Total time: ', end_time - start_time)
        return available_words[:15]