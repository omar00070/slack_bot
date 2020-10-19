from slack import BearerAuth, Slack
import os

TOKEN = os.environ.get('SLACK_TOKEN')


auth = BearerAuth(TOKEN)
print(TOKEN)
#instance of slack object
Slacker = Slack(TOKEN, auth)

channels = Slacker.get_conversations()
print(channels)