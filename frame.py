import cv2
from tkinter import Canvas, NW, Tk
from PIL import ImageTk
import pyscreenshot as ImageGrab


class Frame:
    def __init__(self, window, root):
        self.x = None
        self.y = None
        self.width = 2048
        self.height = 1080
        self.window = window
        self.canvas = Canvas(window, width=self.width, height=self.height)
        self.rect_x1 = None
        self.rect_y1 = None
        self.rect_x2 = None
        self.rect_y2 = None
        self.imgtk = None
        self.screenie_image = None
        self.root = root

    def _draw_rect(self, fill):
        self.canvas.create_line(
            self.rect_x1, self.rect_y1, self.rect_x1, self.rect_y2, fill=fill)
        self.canvas.create_line(
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y1, fill=fill)
        self.canvas.create_line(
            self.rect_x2, self.rect_y2, self.rect_x2, self.rect_y1, fill=fill)
        self.canvas.create_line(
            self.rect_x2, self.rect_y2, self.rect_x1, self.rect_y2, fill=fill)

    def _init_window(self):
        # removes the border from the window
        self.window.overrideredirect(True)

        # ininate the canvas
        self.canvas.pack()

    def _init_image(self):
        # initiate the image

        img = ImageGrab.grab(
            bbox=(0, 0, self.width, self.height))
        self.imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = self.imgtk  # shows frame for canvas

    def _clear_canvas(self):
        self.canvas.delete('all')
        self.draw_image()

    def _click_callback(self, event):
        print("clicked at", event.x, event.y)
        if not self.rect_x1:
            self.rect_x1, self.rect_y1 = event.x, event.y
            return
        self.canvas.delete('all')
        # self.draw_image()
        self.rect_x2, self.rect_y2 = event.x, event.y

        bbox = self._get_bbox()
        self.screenshot(bbox)
        self.window.destroy()
        self.window.update()

    def screenshot(self, bbox):
        self.screenie_image = ImageGrab.grab(bbox=bbox)

    def _get_bbox(self):
        x1, x2 = sorted([self.rect_x1, self.rect_x2])
        y1, y2 = sorted([self.rect_y1, self.rect_y2])
        return (x1 + 1, y1 + 1, x2, y2)

    def _motion_callback(self, event):
        if self.rect_x1:
            self.rect_x2, self.rect_y2 = event.x, event.y
            self._clear_canvas()
            self._draw_rect('green')

    def handle_actions(self):
        # canvas actions
        self.canvas.bind('<Button-1>', self._click_callback)
        self.canvas.bind('<Motion>', self._motion_callback)

        # window actions
        self.window.bind('<Return>', lambda event: self.window.destroy())

    def draw_image(self):
        self.canvas.create_image((0, 0), anchor=NW, image=self.imgtk)

    def get_screenshot(self):
        return self.screenie_image

    def start(self):
        self._init_window()
        self._init_image()
        self.handle_actions()
        self.draw_image()


# window = Tk()
# frame = Frame(window)
# frame.start()
# window.mainloop()
