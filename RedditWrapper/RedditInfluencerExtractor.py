from ast import literal_eval

import pandas as pd


def check_author(redditors, author):
    if author not in redditors.index:
        redditors.loc[author] = [0, 0, 0, 0, 0, 0, 0.0]
    return redditors


def handle_submission(redditors, submission):
    submission_author = submission['author']
    redditors = check_author(redditors, submission_author)
    redditor = redditors.loc[submission_author]
    redditor['crypto_threads_count'] = redditor['crypto_threads_count'] + 1
    redditor['crypto_threads_upvotes'] = redditor['crypto_threads_upvotes'] + submission['score']
    redditor['crypto_threads_comments_count'] = redditor['crypto_threads_comments_count'] + submission['comms_num']


def handle_comments(redditors, comments):
    comments = literal_eval(comments)
    for comment in comments:
        comment_author = comment.author
        check_author(redditors, comment_author)
        redditor = redditors.loc(comment_author)

        redditor['crypto_comments_count'] = redditor['crypto_comments_count'] + 1
        redditor['crypto_comments_upvotes'] = redditor['crypto_comments_upvotes'] + comment.score


def update_redditors(submission, redditors):
    handle_submission(redditors, submission)
    handle_comments(redditors, submission['comments'])


def calculate_influencer_score(redditor):
    redditor['influencer_score'] = redditor['crypto_comments_count'] \
                                   + redditor['crypto_comments_upvotes'] \
                                   + 10 * redditor['crypto_threads_count'] \
                                   + 5 * redditor['crypto_threads_upvotes'] \
                                   + 10 * redditor['crypto_threads_comments_count']


columns = ['name',
           'user_comment_karma',
           'crypto_comments_count',
           'crypto_comments_upvotes',
           'crypto_threads_count',
           'crypto_threads_upvotes',
           'crypto_threads_comments_count',
           'influencer_score']

dtype = dict(zip(columns, [str, int, int, int, int, int, int, float]))

reddit_data = pd.read_csv("reddit_data", sep='\t')
# pd.eval(reddit_data['comments'])

redditors = pd.DataFrame(columns=columns)
redditors.set_index('name', inplace=True)
print(reddit_data.head())
print(redditors.head())

reddit_data.apply(update_redditors, axis='columns', args=(redditors,))
reddit_data.apply(calculate_influencer_score, axis='columns')

print(redditors.head())
