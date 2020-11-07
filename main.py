from fastapi import FastAPI, File, UploadFile
from slack import BearerAuth, Slack
import os, requests

TOKEN = os.environ.get('SLACK_TOKEN')


Slacker = Slack(
        TOKEN, 
        BearerAuth(TOKEN)
        )

class SlackTwo(Slack):
    def send_file(self, channel, file, message):
        files = {
            'file': file
        }
        
        data = {
            'channels': channel,
            'initial_comment': message
        }
        res = requests.post(
            self.urls['uploadFile'], 
            auth=self.auth,
            data=data, 
            files=files
            )

        res_json = res.json()

        if not res_json['ok']:
            print(res_json)

        return res



Slacker = SlackTwo(
        TOKEN, 
        BearerAuth(TOKEN)
        )


channels, _ = Slacker.get_conversations()

CHANNEL = channels['test']
print(CHANNEL)

app = FastAPI()




@app.get('/')
def get_something():
    return 'hello'



@app.post('/uploadfile/')
async def upload_file(file: UploadFile = File(...), message: str = None):
    image = await file.read()
    print(CHANNEL)
    Slacker.send_file(CHANNEL, image, 'some message')
    return {"filename": file.filename}