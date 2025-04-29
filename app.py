import typer
from scraper import *
from tqdm import tqdm
 
app = typer.Typer()

@app.command()
def get_leads(persona: str, depth: str = "low", export_csv: bool = False):
    """
    Get leads for a given persona.
    """
    # get subreddits from the config file from the persona
    subreddits = config["personas"][persona]
    count = 1
    for subreddit in subreddits:
        tqdm.write(f"Getting leads for subreddit: {subreddit} | {count} / {len(subreddits)}")
        populate_leads(subreddit, persona, depth=depth)
        count += 1
    # print the database
    trim_leads()
    active_recently(persona)
    print_database()
    if export_csv:
        export_leads_to_csv(persona)
        tqdm.write(f"Exported leads to {persona}_leads.csv")


if __name__ == "__main__":
    app()
