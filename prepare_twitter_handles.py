import pandas as pd
import pycountry

country_codes = [country.alpha_2.lower() for country in pycountry.countries]


def keep_unique_twitter_handles():
    twitter_handles_df = pd.read_csv("output/cleaned_twitter_links.csv", header=None)
    unique_links_df = twitter_handles_df.drop_duplicates()
    unique_links_df.reset_index(inplace=True)
    unique_handles_df = unique_links_df[unique_links_df.columns[-1]].apply(lambda link: link.split("/")[-1])
    unique_handles_df.to_csv("output/unique_twitter_handles.csv", index=False)


def clean_tweets():
    not_twitter_handles_parts = ["intent", "search", "share", "hashtag", "/ja/", "/ko_KR/", "/zh/"]

    with open('output/raw_twitter_links.csv', 'r') as raw_twitter_handles:
        with open('output/cleaned_twitter_links.csv', 'w') as cleaned_twitter_handles:
            for link in raw_twitter_handles:
                link = remove_whitespaces(link)
                if is_twitter_link(link, not_twitter_handles_parts):
                    twitter_handle = truncate_twitter_link(link)
                    cleaned_twitter_handles.write(twitter_handle + "\n")


def truncate_twitter_link(link):
    split_link = link.split("/")
    if len(split_link) >= 4 and split_link[3] in country_codes:
        last_part = split_link[-1]
        link = link.replace(last_part, "")[:-3] + last_part
    return link.split("/status")[0].split("?")[0].split("/lists")[0]


def is_twitter_link(link, not_twitter_handles_parts):
    return not any(unwanted_part in link for unwanted_part in not_twitter_handles_parts) and \
           link.startswith("https://twitter.com/")


def remove_whitespaces(line):
    no_whitespace_link = ''.join(line.split())
    return no_whitespace_link


if __name__ == '__main__':
    clean_tweets()
    keep_unique_twitter_handles()
