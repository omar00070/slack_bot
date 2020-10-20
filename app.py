from slack import BearerAuth, Slack
import random, os
import pyscreenshot as ImageGrab
import tkinter as tk
from tkinter import filedialog
from mouse import Mouse

# application stes:
# - take a screenshot and save to the users storage
# - application should use the relative path of the image automatically 
# - user should fill in the question as well as the potintial answer
# - post the data to slacks upload file api to the target channel

#change this token value
TOKEN = os.environ.get('SLACK_TOKEN')


class App:
    def __init__(self):
        self._token = TOKEN
        self.img = None
        self.question = None
        self.answer = None
        self.link = None
        self.by = None
        self.bbox = (0, 0, 2048, 1080)
        self.Slacker = Slack(
            self._token, 
            BearerAuth(self._token)
        )
        self.mouse = Mouse()

    def screenshot(self):
        '''
            method to take a screenshot of a specific aread (bbox)
            params: bbox: tuple (x1, y1, x2, y2)
            returns: image_name
        '''
        #get the pox
        self.mouse.start()
        self.bbox = self.mouse.get_bbox()

        im = ImageGrab.grab(bbox=self.bbox)
        image_name = f'screenshot_{random.randint(1, 1000000)}.png'
        im.save(image_name)
        self.img = image_name

    def send(self, entries):
        '''
            method to send the payload to slack
            arguments: entries: list of all the entries in tkinter
            returns: None
        '''
        #get all public channels
        channels, _ = self.Slacker.get_conversations()
        print(channels)
        #channel to send to 
        # channel = channels['test']  ----> for testing
        
        channel = channels['04-labeling-questions']
        
        for ent in entries:
            if not ent.get(): 
                print('please fill all the entries')
                return # make sure all entries are filled 
        
        if not self.img:
            print('please take a screenshot')
            return #make sure the screenshot is taken
        
        # test information to send
        self.by = entries[0].get()
        self.question = entries[1].get()
        self.answer = entries[2].get()
        self.link = entries[3].get()
        
        message = f'*By:* {self.by}\n*Question:* {self.question}\n*Potential answer:* {self.answer}\n*Link:* {self.link}'
        
        self.Slacker.send_file(channel, self.img, message)
        os.remove(self.img)
        self.__init__()

    def run(self):
        root = tk.Tk()
        # myButton = tk.Button(
        #     text="Take Screenshot",
        #     command=self.screenshot,
        #     bg='green',
        #     fg='white',
        #     font=10
        # )
        
        #labels
        tk.Label(root, 
            text="By").grid(row=0)
        tk.Label(root, 
            text="Question").grid(row=1)
        tk.Label(root, 
            text="Potential Answer").grid(row=2)
        tk.Label(root, 
            text="Link").grid(row=3)

        #entries
        e_by = tk.Entry(root)
        e_question = tk.Entry(root)
        e_answer = tk.Entry(root)
        e_link = tk.Entry(root)
        
        e_by.grid(row=0, column=1)
        e_question.grid(row=1, column=1)
        e_answer.grid(row=2, column=1)
        e_link.grid(row=3, column=1)
        ents = [e_by, e_question, e_answer, e_link]

        e_by.insert(0, 'Omar') # insert default value as the user

        #buttons
        tk.Button(root, 
          text='screenshot', 
          command=self.screenshot).grid(row=5, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
        
        
        tk.Button(root, 
          text='send', 
          command=lambda : self.send(ents)).grid(row=5, 
                                    column=2, 
                                    sticky=tk.W, 
                                    pady=3)

        
        tk.mainloop()





if __name__ == "__main__":
    app = App()
    app.run()