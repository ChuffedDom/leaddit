## 🎯 Purpose

To help business owners and entrepreneurs reach the people they need to reach in a non-sucky way.

## 👀 Vision

For lead generation to be more persona and cohort management and have the boring and annoying stuff just work in the background.

## 🥅 Goals

- Build a prototype for internal use by the end of the week (13th April 2025)
- Scope and build an MVP with a landing page by next week (w/c 14th April 2025)
- Start a go-to-market strategy for the end of April 2025

## 😊 Persona
### 🙋🏾‍♀️ Sarah Solopreneur 

#### Motivations
- Financial independence - a steady income stream outside of a job 
- Grow her personal brand and authority in her niche
#### Needs & Wants
- Qualified leads
	- Generate 5–10 leads per month directly from Reddit
- For lead gen to not take up time and brain space
- Establish herself as a trusted, helpful expert
- To do lead gen without having to be a lead gen expert
#### Pain Points
- Lead gen is boring and annoying
- CRMs are just mystifying
- Sales Navigator is expensive and hard to use
#### Activities
- Works from home or local coffee shops
- Reddit
	- r/freelance
	- r/smallbusiness
	- r/entrepreneur
- Discord??
- LinkedIn
- Google Sheets - a lot of sheets
## 🤕 Problem

As a small business owner or entrepreneur, I need to have leads come in that are qualified and they know, like, and trust me. But, I have a very sporadic success, this is because I have manage several ways of doing outreach that comes with various annoyances:
- LinkedIn is noisy and too salesy
- Tools (such as CRMs) can be expensive and are built for people in that field, sales, marketing, and not me a solopreneur
- Online ads are an art form on their own and require knowledge in the field that I do not have
- Lead magnets are also expensive and require either paying someone to manage them or using up a lot of my time
- Social media is a hard game to get into and requires a lot of work for a long time before you see the benefits. To add to that ,I am just not good at it
Therefore, I feel a lot of time, effort, and money is spent on getting work through the door and not delivering higher-quality work that can sell itself. This paradox is annoying and frustrating.

## 🤔 Hypothesis
If I build a tool where a user can create a profile of the person they are trying to target from the subreddits they frequent, then I can deliver value in solving a tiny bit of the problem of "lead gen sucks".
## 🫴🏾 Proposal
### Leaddit

*Lead gen without the pain of Lead gen*

"Your next client is on Reddit right now; We will help you find them."

You build a Persona in Leaddit with the attributes of the subreddits they are likely to frequent, and we will return a list of users to target in campaigns.

#### Prototype
A command-line tool to test the functionality and start outreach for Chuffed.

#### MVP
A free-to-use tool with basic scraping and output of higher-quality leads. 

### 🖌️ Wireframes and Designs

![Wireframes](https://i.postimg.cc/wMRFFnzb/Untitled-2024-12-24-1521.png)](https://postimg.cc/T5Gr37pr)

### 👤 User Stories

As a user, I want to know I can sit down at my desk Monday morning with a cup of coffee and feel confident that the outreach I am doing to worthwhile and will lead to good work for me to bill.

As a user, I need to manage a pipeline without complex marketing and sales tools, so I can spend my time doing what I know and what I do best.

As a user, I need to add know-how to and be able to add my Reddit API credentials so I can use the scraping functionality.

As a user, I need to build a persona using subreddits so I can build an outreach list.

### ✅ Acceptance Criteria (command line tool)

- Given I am setting up Leaddit, when I open the config.json file
	- then I can add my Reddit API credentials
	- and also add a persona
	- and also add a list of subreddits
- Given I have set up Leaddit, then I can run a scan to scrape those subreddits
- When I run a scan
	- then for each subreddit
		- the last months of posts are loaded
		- each user is added to the a database
			- each user who has commented or posted has a +1 to their score
	- if the subreddit does not exist then skip it and notify me

## ➡️ Moving Forward
- Build the MVP with a simple sign-in flow

