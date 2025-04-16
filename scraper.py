import yaml
import praw
import os
import data_management
from tabulate import tabulate
from tqdm import tqdm

CONFIG_FILE = "config.yaml"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Missing config file: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

config = load_config()

# Access credentials
client_id = config["credentials"]["client_id"]
client_secret = config["credentials"]["client_secret"]
user_agent = config["credentials"]["user_agent"]

# Drop Leads table from the database
def drop_leads_table():
    data_management.db.drop_tables([data_management.Lead], safe=True)
    data_management.db.create_tables([data_management.Lead], safe=True)
drop_leads_table()

# just get the top 100 posts of the last month from a subreddit and return
# the posts as a list
def get_top_posts(subreddit_name, depth="low"):
    if depth == "low":
        limit = 10
    elif depth == "high":
        limit = 100
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(time_filter="month", limit=limit)
    posts = [post for post in top_posts]
    return posts

# get user from a submission and return the user
def get_user_of_post(submission):
    if submission.author:
        return submission.author.name
    else:
        return None
    
# get top 100 comments from a submission and return the comments as a list
def get_top_comments(submission, depth="low"):
    if depth == "low":
        limit = 10
    elif depth == "high":
        limit = 100
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=limit)
    comments = submission.comments.list()
    return comments

def get_user_of_comment(comment):
    if comment.author:
        return comment.author.name
    else:
        return None
    
# add user to the Leads table in the database
def add_user_to_database(user, persona, score):
    if user == "AutoModerator":
        # Skip AutoModerator
        return
    else:
        # check if the user already exists in the database
        lead, created = data_management.Lead.get_or_create(name=user, defaults={"persona": persona, "score": score})
        if not created:
            # Update the lead if it already exists
            lead.persona = persona
            lead.score += score
            lead.save()
        else:
            # If the lead is newly created, set the persona and score
            lead.persona = persona
            lead.score = score
            lead.save()

# print the database in a table to the screen
def print_database():
    # select leads order by score descending
    leads = data_management.Lead.select().order_by(data_management.Lead.score.desc()).where(data_management.Lead.score > 3)
    table = []
    for lead in leads:
        table.append([lead.id, lead.name, lead.persona, lead.score])
    print(tabulate(table, headers=["ID", "Name", "Persona", "Score"], tablefmt="grid"))

# print_database()

def populate_leads(subreddit_name, persona, depth="low"):
    for post in tqdm(get_top_posts(subreddit_name, depth=depth), desc="Getting posts", unit="post"):
        user = get_user_of_post(post)
        if user:
            add_user_to_database(user, persona, 2)
        for comment in get_top_comments(post, depth=depth):
            user = get_user_of_comment(comment)
            if user:
                add_user_to_database(user, persona, 1)