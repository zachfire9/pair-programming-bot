import os
import time
from dotenv import load_dotenv
from os.path import join, dirname
from slackclient import SlackClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class PairProgrammingBot:
    def __init__(self, bot_id, slack_client, conversation_client, workspace_id):
        self.bot_id = bot_id
        self.slack_client = slack_client
        self.conversation_client = conversation_client
        self.workspace_id = workspace_id
        self.at_bot = "<@" + bot_id + ">"
        self.delay = 0.5 #second
        self.context = {}

    def handle_message(self, message, channel):
        """
            Receives commands directed and sends them to Watson.
            Adds the response to the context and returns the message.
        """
        watson_response = self.conversation_client.message(
            workspace_id=self.workspace_id,
            message_input={'text': message},
            context=self.context)

        self.context = watson_response['context']
        self.slack_client.api_call("chat.postMessage", channel=channel,
                              text=watson_response['output']['text'][0], as_user=True)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.at_bot in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(self.at_bot)[1].strip().lower(), \
                           output['channel']
        return None, None

    def run(self):
        if self.slack_client.rtm_connect():
            print("Pair Programming Bot connected and running!")
            while True:
                slack_output = self.slack_client.rtm_read()
                command, channel = self.parse_slack_output(slack_output)
                if command and channel:
                    self.handle_message(command, channel)
                time.sleep(self.delay)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
