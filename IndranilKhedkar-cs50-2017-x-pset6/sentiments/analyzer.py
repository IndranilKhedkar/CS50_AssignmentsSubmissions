import nltk

class Analyzer():
    """Implements sentiment analysis."""
    positive_words = []
    negative_words = []
    def __init__(self, positives, negatives):
        with open(positives) as lines:
            for line in lines:
                if line.startswith(';'):
                    continue
                else:
                    self.positive_words.append(line.strip())

        with open(negatives) as lines:
            for line in lines:
                if line.startswith(";"):
                    continue
                else:
                    self.negative_words.append(line.strip())


    def analyze(self, text):
            score = 0
            tokenizer = nltk.tokenize.TweetTokenizer()
            tokens = tokenizer.tokenize(text)
            for token in tokens:
                if token.lower() in self.positive_words:
                    score = score + 1;
                elif token.lower() in self.negative_words:
                    score = score - 1;
            return score;
