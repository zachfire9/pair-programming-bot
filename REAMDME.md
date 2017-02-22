# README

## Initial Setup Steps

- ```virtualenv pairprogrammingbot```
- ```source pairprogrammingbot/bin/activate```
- ```pip install -r requirements.txt```
- Create a bot in your Slack account (/apps/manage/custom-integrations)
- Get the API Token for the new bot and add it to SLACK_BOT_TOKEN in the .env file. 
- ```python print_bot_id.py```
- Get the Bot ID output and add it to the BOT_ID .env file. 