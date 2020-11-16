from pynput.mouse import Listener


class Mouse:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.pressed = False
        self.button = None

    # def on_move(self, x, y):
    #     if self.pressed:
    #         if self.x1 == None and self.y1 == None:
    #             self.x1, self.y1 = x, y

    def on_click(self, x, y, button, pressed):
        if pressed:
            # self.pressed = True
            if not self.x1 == None and not self.y1 == None:
                self.x2, self.y2 = x, y
            else:
                self.x1, self.y1 = x, y
        if not pressed and not self.x2 == None:
            return False
        self.button = button

    def get_bbox(self):
        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])

        return (x1, y1, x2, y2)

    def start(self):
        self.__init__()  # initiate first
        with Listener(on_click=self.on_click) as listener:
            listener.join()
