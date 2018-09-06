import numpy as np
import pandas as pd
from textblob import TextBlob


def analyse_senitments(review_bodies):
    sentiments = []
    for review_body in review_bodies:
        tb = TextBlob(review_body.replace('<br />', '\n'))
        polarity, subjectivity = tb.sentiment
        sentiments.append((polarity, subjectivity))

    sentiments_arr = np.array(sentiments)
    return sentiments_arr[:,0].mean(), sentiments_arr[:,1].mean()


def main():
    df = pd.read_csv('amazon_reviews_multilingual_UK_v1_00.tsv.gz',
                     compression='gzip', error_bad_lines=False, sep='\t')

    df_prg = df[(df.product_category == 'Books') &
                (df.product_title.str.contains('Programming'))]
    df_yoga = df[(df.product_category == 'Books') &
                 (df.product_title.str.contains('Yoga'))]

    print(analyse_senitments(df_prg.review_body))
    print(analyse_senitments(df_yoga.review_body))


if __name__ == '__main__':
    main()