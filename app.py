import typer
from scraper import *
from tqdm import tqdm

app = typer.Typer()

@app.command()
def get_leads(persona: str):
    """
    Get leads for a given persona.
    """
    # get subreddits from the config file from the persona
    subreddits = config["personas"][persona]
    count = 1
    for subreddit in subreddits:
        tqdm.write(f"Getting leads for subreddit: {subreddit} | {count} / {len(subreddits)}")
        populate_leads(subreddit, persona, depth="low")
        count += 1
    # print the database
    print_database()

if __name__ == "__main__":
    app()
