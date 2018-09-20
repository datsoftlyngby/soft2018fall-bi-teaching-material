# from textblob import TextBlob
# from nltk.corpus import stopwords

# tb = TextBlob(txt)
# filtered_words = [word for word in tb.words if word.lower() not in stopwords.words('english')]

# from collections import Counter
# Counter(filtered_words)

import os
import math
from textblob import TextBlob
from nltk.corpus import stopwords
from collections import defaultdict, Counter
from sklearn.datasets import load_files


def tokenize(txt):
    tb = TextBlob(txt)
    filtered_words = [word for word in tb.words 
                      if word.lower() not in stopwords.words('english')]
    return set(filtered_words)


def count_words(training_set):
    """Training set consists of pairs (text, positivity)"""
    counts = defaultdict(lambda: [0, 0])
    for txt, positivity in training_set:
        for word in tokenize(txt): 
            counts[word][0 if positivity else 1] += 1
    return counts


# word_count = count_words(zip(text_train, y_train))
#     ...:
# CPU times: user 12min 4s, sys: 1min 17s, total: 13min 21s
# Wall time: 15min 28s
# word_count = count_words(zip(text_train, y_train))



def word_probabilities(word_counts, total_pos, total_neg, k=0.5): 
    """Turn the word_counts into a list of triplets
        w, p(w | spam) and p(w | ~spam)"""
    triplet_list = []
    for w, (pos, neg) in word_counts.items():
        p_pos = (pos + k) / (total_pos + 2 * k)
        p_neg = (neg + k) / (total_neg + 2 * k)
        triplet_list.append((w, p_pos, p_neg))
    return triplet_list

# word_probs = word_probabilities(word_count, 12500, 12500)

def pos_neg_probability(word_probs, txt): 
    """Computes the probability for if a given txt is positive or negative.
    Positive are numbers close to 1.0 and negative are numbers close to 0.0"""
    message_words = tokenize(txt) 
    log_prob_pos = log_prob_neg = 0.0
    # iterate through each word in our vocabulary
    for word, prob_pos, prob_neg in word_probs:
        # if *word* appears in the message,
        # add the log probability of seeing it 
        if word in message_words:
            log_prob_pos += math.log(prob_pos)
            log_prob_neg += math.log(prob_neg)
        # if *word* doesn't appear in the message
        # add the log probability of _not_ seeing it 
        # which is log(1 - probability of seeing it) 
        else:
            log_prob_pos += math.log(1.0 - prob_pos)
            log_prob_neg += math.log(1.0 - prob_neg)
    # Engineering solution to avoid overflow errors :)
    if log_prob_pos < -700:
        log_prob_pos = -700.0 
    elif log_prob_pos > 700:
         log_prob_pos = 700.0
    if log_prob_neg < -700:
        log_prob_neg = -700.0 
    elif log_prob_neg > 700:
         log_prob_neg = 700.0
    prob_pos = math.exp(log_prob_pos) 
    prob_neg = math.exp(log_prob_neg)
    return prob_pos / (prob_pos + prob_neg)



class NaiveBayesClassifier:
    def __init__(self, k=0.5): 
        self.k = k
        self.word_probs = []

    def train(self, training_set, reuse_model=True):
        if os.path.isfile('model.py') and reuse_model:
            from model import word_probs
            self.word_probs = word_probs
        else:
            # count positive and negative reviews      
            _, targets = zip(*training_set)
            num_pos = sum(targets)
            num_neg = len(targets) - num_pos
            # run training data through our "pipeline"
            word_counts = count_words(training_set)
            self.word_probs = word_probabilities(word_counts, num_pos, num_neg, 
                                                self.k)
            self.serialize_model()

    def classify(self, txt):
        return pos_neg_probability(self.word_probs, txt)
    
    def serialize_model(self):
        with open('./model.py', 'w') as fp:
            fp.write('word_probs = [\\\n')
            for entry in self.word_probs[:-1]:
                fp.write('\t\t' + str(entry)  + ',\n')
            fp.write('\t\t' + str(self.word_probs[-1]) + ']')



if __name__ == '__main__':
    if not os.path.exists('aclImdb'):
        if not os.path.isfile('aclImdb_v1.tar.gz'):
            os.system('wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz')
        os.system('tar -xzf aclImdb_v1.tar.gz')

    reviews_train = load_files('aclImdb/train/', categories=['neg', 'pos'])
    text_train, y_train = reviews_train.data, reviews_train.target

    text_train = [doc.replace(b'<br />', b' ') for doc in text_train]
    text_train = [doc.decode('utf-8') for doc in text_train]

    my_classifier = NaiveBayesClassifier()
    my_classifier.train(zip(text_train, y_train))

    reviews_test = load_files('aclImdb/test/')
    text_test, y_test = reviews_test.data, reviews_test.target

    text_test = [doc.replace(b'<br />', b' ') for doc in text_test]
    text_test = [doc.decode('utf-8') for doc in text_test]
    step_size = 500
    classifications = [1 if my_classifier.classify(txt) >= 0.5 else 0 
                       for txt, target in zip(text_test[::step_size], y_test[::step_size])]
    classified = [(txt, target, my_classifier.classify(txt)) for txt, target in zip(text_test[::step_size], y_test[::step_size])]
    print(classified)
    classified_filtered = [(target, pos_prob >= 0.5) for _, target, pos_prob in classified]
    # Counter({(0, False): 25, (1, True): 14, (1, False): 7, (0, True): 4})
    counts = Counter(classified_filtered)
    print(counts)
    print(classified.sort(key=lambda row: row[2]))

