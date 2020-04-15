from pycorenlp import StanfordCoreNLP
import csv

nlp = StanfordCoreNLP('http://localhost:9000')


def get_sentiment(text):
    res = nlp.annotate(text,
                       properties={'annotators': 'sentiment',
                                   'outputFormat': 'json',
                                   'timeout': 1000,
                                   })
    print(text)
    print('Sentiment:', res['sentences'][0]['sentiment'])
    print('Sentiment score:', res['sentences'][0]['sentimentValue'])
    print('Sentiment distribution (0-v. negative, 5-v. positive:', res['sentences'][0]['sentimentDistribution'])
    sentiment = {
        'sentiment': res['sentences'][0]['sentiment'],
        'sentiment_score': res['sentences'][0]['sentimentValue']
    }
    return sentiment


def read_comments():
    with open('cbc_comments_with_replies.csv', newline='') as csvfile:
        comment_reader = csv.DictReader(csvfile)
        with open('sentiment_analysis.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(["id", "name", "comment", "sentiment", "sentiment_score"])
            for row in comment_reader:
                sentiment = get_sentiment(row["comment"])
                writer.writerow([row['id'], row['name'], row['comment'], sentiment['sentiment'],
                                 sentiment['sentiment_score']])
                print([row['id'], row['name'], row['comment'], sentiment['sentiment'],
                                 sentiment['sentiment_score']])


read_comments()


