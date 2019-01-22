import praw
import pandas as pd
import datetime
from praw.models import Comment

considered_subreddits = ['crypto_data', 'Bitcoin', 'litecoin', 'btc', 'Cryptocurrency',
                         'CryptoMarkets', 'ethereum']

reddit = praw.Reddit(client_id='niEeEjiqEMilzg',
                     client_secret='hi2pHt9T1cjiKD_FFYfL8OdkGZ8',
                     password='Lemur24',
                     user_agent='testscript by /u/Jumanchi',
                     username='Jumanchi')

print(reddit.user.me())
submissions_per_subreddit = [reddit.subreddit(subreddit).top(limit=None) for subreddit in considered_subreddits]

topics_dict = {"author": [],
               "title": [],
               "score": [],
               "id": [],
               "url": [],
               "comms_num": [],
               "created": [],
               "body": [],
               "comments": [],
               "subreddit": []}

n_sub = 0

for subreddit in submissions_per_subreddit:
    for submission in subreddit:

        print("[INFO][" + str(n_sub) + "] " + submission.title + " - created: " + str(submission.created) + ", " + str(len(submission.comments)) + " comments.")
        n_sub = n_sub + 1
        topics_dict["author"].append(submission.author)
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
        topics_dict["subreddit"].append(submission.subreddit.display_name)

        # done_replaces = 0
        # while done_replaces < 3:
        #     try:
        #         submission.comments.list().replace_more()
        #         done_replaces = done_replaces + 1
        #     except Exception:
        #         time.sleep(1)

        sub_comments = []
        for comment in submission.comments.list():
            if isinstance(comment, Comment):
                sub_comments.append(comment)
        topics_dict["comments"].append(sub_comments)


topics_data = pd.DataFrame(topics_dict)

timestamps = topics_data["created"].apply(datetime.datetime.fromtimestamp)
topics_data = topics_data.assign(timestamp=timestamps)

topics_data.info()
print("[INFO] Finished successfully")
topics_data.to_csv("reddit_data_test", sep='\t')

