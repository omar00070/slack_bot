import random
import os
import requests
import json
import tkinter as tk
from tkinter import filedialog
from mouse import Mouse
from frame import Frame
import threading

# for windows, mac users
# from PIL import ImageGrab

# for linux
import pyscreenshot as ImageGrab


# application stes:
# - take a screenshot and save to the users storage
# - application should use the relative path of the image automatically
# - user should fill in the question as well as the potintial answer
# - post the data to slacks upload file api to the target channel


TEAM_LEADERS = {
    'pipelinka': 'U0146J252F5',
    'ninja turtles': 'U013DEGE1FT',
    'pennywise clowns': 'U012L41NQ8P',
    'cerberus': 'U01371EFELC',
}


class App:
    def __init__(self):
        self.image = None  # image object "screenshot image object"
        self.img = None
        self.question = None
        self.answer = None
        self.project = None
        self.team_leader = None
        self.team = None
        self.link = None
        self.user_id = None

        self.root = tk.Tk()
        self.frame = None

        self.mouse = Mouse()
        self.bbox = (0, 0, 2048, 1080)

    def _init_entries(self):
        self.image = None  # image object "screenshot image object"
        self.img = None
        self.question = None
        self.answer = None
        self.project = None
        self.team_leader = None
        self.team = None
        self.link = None
        self.user_id = None

    def screenshot(self):
        '''
            method to take a screenshot of a specific aread (bbox)
            params: bbox: tuple (x1, y1, x2, y2)
            returns: image_name
        '''
        # get the box
        # self.mouse.start()
        # self.bbox = self.mouse.get_bbox()

        # self.image = ImageGrab.grab(bbox=self.bbox)
        # image_name = f'screenshot_{random.randint(1, 1000000)}.png'
        # # im.save(image_name)
        # self.img = image_name

        window = tk.Toplevel(self.root)

        self.frame = Frame(window, self.root)

        self.frame.start()

        image_name = f'screenshot_{random.randint(1, 1000000)}.png'
        self.img = image_name

    def _capitalize_words(self, entery):
        '''



            private function to capitalize multi words (foo bar =>  Foo Bar)
            params: entery: tk entery object
            returns: string capitalized
        '''

        return ' '.join([n.capitalize() for n in entery.get().split(' ')])

    def send(self, entries):
        '''
            method to send the payload to slack
            arguments: entries: list of all the entries in tkinter
            returns: None
        '''
        # get all public channels

        for ent in entries:
            if not ent.get():
                print('please fill all the entries')
                return  # make sure all entries are filled before sending

        if not self.img:
            print('please take a screenshot')
            return  # make sure the screenshot is taken

        self.image = self.frame.screenie_image

        # test information to send
        self.user_id = entries[0].get()
        self.team = self._capitalize_words(entries[1])
        self.project = entries[2].get().capitalize()
        self.question = entries[3].get().capitalize()
        self.answer = entries[4].get().capitalize()
        self.link = entries[5].get()

        if self.team.lower() in TEAM_LEADERS:
            self.team_leader = TEAM_LEADERS[self.team.lower()]

        else:
            print('please provide a correct team name')
            return  # make sure that the team is provided corectly

        if self.team_leader == self.user_id:
            self.team_leader = ''

        self.image.save(self.img)

        message = f'*By:* <@{self.user_id}>\n*Team:* {self.team} <@{self.team_leader}>\n*Project:* {self.project}\n*Question:* {self.question}\n*Potential answer:* {self.answer}\n*Link:* {self.link}'

        files = {'file': open(self.img, 'rb')}

        # send to the web server to handle slack api

        res = requests.post(
            f'https://hadesslackbot.herokuapp.com/send_file/{str(self.user_id)}/{str(message)}', files=files)

        # f'http://127.0.0.1:8000/send_file/{str(self.user_id)}/{str(message)}', files=files) debugging

        # print(res.status_code)

        entries[3].delete(0, tk.END)
        entries[4].delete(0, tk.END)

        os.remove(self.img)

        self._init_entries()

        # self.__init__()  # reinitiate after sending

    def run(self):

        # labels
        tk.Label(self.root,
                 text="User ID").grid(row=0)
        tk.Label(self.root,
                 text="Team").grid(row=1)
        tk.Label(self.root,
                 text="Project").grid(row=2)
        tk.Label(self.root,
                 text="Question").grid(row=3)
        tk.Label(self.root,
                 text="Potential Answer").grid(row=4)
        tk.Label(self.root,
                 text="Link").grid(row=5)

        # entries
        e_by = tk.Entry(self.root)
        e_team = tk.Entry(self.root)
        e_project = tk.Entry(self.root)
        e_question = tk.Entry(self.root)
        e_answer = tk.Entry(self.root)
        e_link = tk.Entry(self.root)

        e_by.grid(row=0, column=1)
        e_team.grid(row=1, column=1)
        e_project.grid(row=2, column=1)
        e_question.grid(row=3, column=1)
        e_answer.grid(row=4, column=1)
        e_link.grid(row=5, column=1)
        ents = [e_by, e_team, e_project, e_question, e_answer, e_link]

        # e_by.insert(0, 'Omar') # insert default value as the user

        # buttons
        tk.Button(self.root,
                  text='screenshot',
                  command=self.screenshot).grid(row=7,
                                                column=0,
                                                sticky=tk.W,
                                                pady=4)

        tk.Button(self.root,
                  text='send',
                  command=lambda: self.send(ents)).grid(row=7,
                                                        column=2,
                                                        sticky=tk.W,
                                                        pady=3)

        tk.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
