import json
import os
import time
from dotenv import load_dotenv
from slackclient import SlackClient
from watson_developer_cloud import ConversationV1

from pairprogrammingbot import PairProgrammingBot

if __name__ == "__main__":
  load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

  bot_id = os.environ.get("BOT_ID")

  slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

  conversation_client = ConversationV1(
    username=os.environ.get("CONVERSATION_USERNAME"),
    password=os.environ.get("CONVERSATION_PASSWORD"),
    version='2017-02-10')

  workspace_id = os.environ.get("WORKSPACE_ID")

  pairprogrammingbot = PairProgrammingBot(bot_id, 
                      slack_client, 
                      conversation_client, 
                      workspace_id)
  pairprogrammingbot.run()