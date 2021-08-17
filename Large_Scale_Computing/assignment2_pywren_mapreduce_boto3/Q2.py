
from mrjob.job import MRJob
from mrjob.step import MRStep
import dataset
import re

WORD_RE = re.compile(r"[\w']+")


class MRMostUsedWord(MRJob):

    def mapper_get_words(self, _, desc):
        for word in WORD_RE.findall(desc):
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_find_max_words(self, _, word_count_pairs):
        max_10 = sorted(word_count_pairs)[-10:]
        yield max_10, None


    def steps(self):
        return [
            MRStep(mapper = self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_max_words)
        ]

if __name__ == '__main__':
    MRMostUsedWord.run()
