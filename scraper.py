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
 
# go through the database and get all leads check if they have
# posted in the subreddits of the persona in the last 24 hours
# if so add 2 to the score of that lead
def active_recently(persona):
    subreddits = config["personas"][persona]
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    for subreddit in tqdm(subreddits, desc="Checking activity", unit="subreddit"):
        # get the last 24 hours of posts and comments from the subreddit
        tqdm.write(f"Checking activity in subreddit: {subreddit}")
        subreddit = reddit.subreddit(subreddit)
        subreddit_posts = subreddit.new(limit=100)
        # check if author of the post is in the database
        for post in subreddit_posts:
            if post.author:
                try:
                    lead = data_management.Lead.get(name=post.author.name, persona=persona)
                    if lead:
                        tqdm.write(f"Found lead post: {lead.name} in subreddit: {subreddit} for persona: {persona}")
                        lead.score += 2
                        lead.save()
                except data_management.Lead.DoesNotExist:
                    pass
            # get the comments of the post
            post.comments.replace_more(limit=0)
            for comment in post.comments.list():
                if comment.author:
                    try:
                        lead = data_management.Lead.get(name=comment.author.name, persona=persona)
                        if lead:
                            tqdm.write(f"Found lead comment: {lead.name} in subreddit: {subreddit} for persona: {persona}")
                            lead.score += 1
                            lead.save()
                    except data_management.Lead.DoesNotExist:
                        pass

# print the database in a table to the screen
def print_database():
    # select leads order by score descending
    leads = data_management.Lead.select().order_by(data_management.Lead.score.desc()).where(data_management.Lead.score > 3)
    table = []
    for lead in leads:
        table.append([lead.id, lead.name, lead.persona, lead.score])
    print(tabulate(table, headers=["ID", "Name", "Persona", "Score"], tablefmt="grid"))

# get the leads out of the database for a persona and export to a CSV
def export_leads_to_csv(persona):
    leads = data_management.Lead.select().where(data_management.Lead.persona == persona)
    # create a CSV file with the leads
    with open(f"{persona}_leads.csv", "w") as f:
        f.write("ID,Name,Persona,Score\n")
        for lead in leads:
            f.write(f"{lead.id},{lead.name},{lead.persona},{lead.score}\n")

def populate_leads(subreddit_name, persona, depth="low"):
    for post in tqdm(get_top_posts(subreddit_name, depth=depth), desc="Getting posts", unit="post"):
        user = get_user_of_post(post)
        if user:
            add_user_to_database(user, persona, 4)
        for comment in get_top_comments(post, depth=depth):
            user = get_user_of_comment(comment)
            if user:
                add_user_to_database(user, persona, 3)

def trim_leads():
    # get all leads from the database
    leads = data_management.Lead.select()
    # order the leads by score
    leads = sorted(leads, key=lambda x: x.score, reverse=True)
    # remove all leads that are not in the top 50
    for lead in leads[50:]:
        lead.delete_instance()