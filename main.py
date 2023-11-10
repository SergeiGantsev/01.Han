import tkinter as tk
import tkinter.ttk as ttk
from MySqlCall import MySqlCall
from threading import Thread
from Common import get_timestamp, get_config
import time
import configparser
import pathlib
from pathlib import Path
import logging
from MyDBLogger import MyDBLogger
from PIL import Image, ImageTk
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import json
from datetime import datetime
import io
import xml.etree.ElementTree as ET


class HanApp:
    def __init__(self):
        # build ui
        self.root = tk.Tk() # if master is None else tk.Toplevel(master)
        self.root.configure(height=500, width=700)
        self.root.minsize(500, 500)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        frame1 = ttk.Frame(self.root)
        frame1.configure(borderwidth=0, height=500, width=700)
        frame1.grid(column=0, row=0, sticky="nsew")
        frame1.grid_propagate(0)
        frame1.grid_anchor("center")
        frame1.rowconfigure(1, weight=1)
        frame1.columnconfigure(1, weight=1)

        frame_btn = ttk.Frame(self.root)
        frame_btn.configure(borderwidth=0,height=200, width=200)
        frame_btn.rowconfigure(0, weight=1)
        frame_btn.columnconfigure(0, weight=1)
        frame_btn.grid(column=0, row=1, sticky="new")

        btn_quit = ttk.Button(frame_btn)
        btn_quit.configure(text='Quit', command=self.click_quit)
        btn_quit.grid(column=0, padx="5 5", pady="5 5", row=0, sticky="e")

        labelframe_connections = ttk.Labelframe(frame1)
        labelframe_connections.configure(
            height=200,
            labelanchor="n",
            text='Connections',
            width=200)
        labelframe_connections.grid(column=0, row=0, pady=5, sticky="nw")
        labelframe_connections.columnconfigure("all", weight=1)

        self.canvas_connect_me = tk.Canvas(labelframe_connections)
        self.canvas_connect_me.configure(
            background="red",
            height=15,
            highlightthickness=0,
            width=15)
        self.canvas_connect_me.grid(column=0, padx=10, row=0, sticky="e")

        self.btn_connect_me = ttk.Button(labelframe_connections)
        self.btn_connect_me.configure(text='Start ME', command=self.click_connect_me)
        self.btn_connect_me.grid(column=1, pady="5 5", row=0, sticky="w")

        self.canvas_connect_pbd = tk.Canvas(labelframe_connections)
        self.canvas_connect_pbd.configure(
            background="red",
            height=15,
            highlightthickness=0,
            width=15)
        self.canvas_connect_pbd.grid(column=2, padx=10, row=0, sticky="e")

        self.btn_connect_pbd = ttk.Button(labelframe_connections)
        self.btn_connect_pbd.configure(text='Start PBD', command=self.click_connect_pbd)
        self.btn_connect_pbd.grid(column=3, padx="0 5", row=0, sticky="w")

        labelframe2 = ttk.Labelframe(frame1)
        labelframe2.configure(
            height=200,
            labelanchor="n",
            text='Status',
            width=200)
        labelframe2.grid(column=0, padx=5, row=1, sticky="new")
        labelframe2.rowconfigure(0, weight=0)
        labelframe2.columnconfigure(1, weight=1)

        # Images
        path = Path(pathlib.Path.cwd(), "images", "True.PNG")
        self.img_true = ImageTk.PhotoImage(Image.open(path))
        path = Path(pathlib.Path.cwd(), "images", "False.PNG")
        self.img_false = ImageTk.PhotoImage(Image.open(path))

        # Status Thread global
        self.label_global_img = tk.Label(labelframe2, image=self.img_true)
        self.label_global_img.grid(column=0, row=0, sticky="n")

        label_global = tk.Label(labelframe2)
        label_global.configure(text='Global thread')
        label_global.grid(column=1, row=0, sticky="new")

        # Status Thread ME
        self.label1 = tk.Label(labelframe2, image=self.img_true)
        self.label1.grid(column=0, row=1, sticky="n")

        label2 = tk.Label(labelframe2)
        label2.configure(text='Thread ME')
        label2.grid(column=1, row=1, sticky="new")

        # Status MySQL connect ME
        self.label_mysql_connect_img = tk.Label(labelframe2, image=self.img_true)
        self.label_mysql_connect_img.grid(column=0, row=2, sticky="n")

        label_mysql_connect = tk.Label(labelframe2)
        label_mysql_connect.configure(text='MySQL connect')
        label_mysql_connect.grid(column=1, row=2, sticky="new")

        # Status connect PBD
        self.label_connect_pbd_img = tk.Label(labelframe2, image=self.img_false)
        self.label_connect_pbd_img.grid(column=0, row=3, sticky="n")

        label_connect_binance = tk.Label(labelframe2)
        label_connect_binance.configure(text='Partial book depth')
        label_connect_binance.grid(column=1, row=3, sticky="new")

        self.canvas = tk.Canvas(frame1)
        self.canvas.configure(height=500, highlightthickness=0, width=500)
        self.canvas.grid(column=1, padx=5, row=0, rowspan=2, sticky="nsew")
        self.canvas.update()
        # ------------------------------------------------------------

        # config
        self.config = configparser.ConfigParser()
        path_config = Path(pathlib.Path.cwd(), "Config.ini")
        self.config.read(path_config)
        # ------------------------------------------------------------

        # logging
        self.my_logger = MyDBLogger("Han", logging.DEBUG).logger
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d, %(name)s, %(levelname)s: %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

        path_config = Path(pathlib.Path.cwd(), "logs", "Han.log")
        file_log = logging.FileHandler(filename=path_config, mode="w")
        file_log.setFormatter(formatter)
        self.my_logger.addHandler(file_log)

        console_out = logging.StreamHandler()
        console_out.setFormatter(formatter)
        self.my_logger.addHandler(console_out)
        # ------------------------------------------------------------

        # VARS
        self.spot_code = self.config.get("general", "spot_code")
        self.fut_code = self.config.get("general", "fut_code")
        self.binance_code = self.config.get("general", "binance_code")

        self.spot_price = None
        self.fut_price = None

        self.min_price = None
        self.max_price = None
        self.binance_price = None

        self.canvas_dict = None

        self.min_delta = 100000000
        self.max_delta = 0

        # Init Canvas
        self.init_canvas()

        # root.bind
        self.root.bind("<Configure>", self.root_handler)
        self.root.bind("<Destroy>", self.on_root_destroy)

        # Thread ME
        self.db = MySqlCall()
        self.is_db_connection = False

        self.thread_me = Thread(target=self.target_thread_me)
        self.thread_me.daemon = True
        self.thread_me.start()

        # Socket SpotWebsocketStreamClient
        self.is_connection_pbd = False
        self.pbd_client = None

        # Thread global
        self.thread_global = Thread(target=self.target_thread_global)
        self.thread_global.daemon = True
        self.thread_global.start()

    def pbd_handler(self, _, message):
        # self.my_logger.info(message)
        message_json = json.loads(message)

        if 'bids' in message_json and 'asks' in message_json:
            s = 0
            bid_depth = None
            for item in message_json['bids']:
                s += float(item[1])

                if s >= 1000:
                    bid_depth = float(item[0])
                    break

            s = 0
            ask_depth = None
            for item in message_json['asks']:
                s += float(item[1])

                if s >= 1000:
                    ask_depth = float(item[0])
                    break

            bid = float(message_json['bids'][0][0])
            ask = float(message_json['asks'][0][0])

            self.binance_price = {'bid': bid, 'bid_depth': bid_depth, 'ask': ask, 'ask_depth': ask_depth,
                                  'timestamp': get_timestamp()}

            # print(self.binance_price)

    def click_quit(self):
        self.root.destroy()

    def target_thread_global(self):
        sleep = float(self.config.get("thread_global", "sleep"))

        time_save_canvas = get_timestamp()
        delay_save_canvas = int(get_config("thread_global", "delay_save_canvas"))

        time_save_status = get_timestamp()
        delay_save_status = int(get_config("thread_global", "delay_save_status"))

        while True:
            if not self.thread_me.is_alive():
                self.label1["image"] = self.img_false
                self.is_db_connection = False
                self.label_mysql_connect_img["image"] = self.img_false

            if self.db.conn is None:
                self.label_mysql_connect_img["image"] = self.img_false
            else:
                if self.db.conn.connection_id is None:
                    self.label_mysql_connect_img["image"] = self.img_false
                    self.is_db_connection = False
                else:
                    self.label_mysql_connect_img["image"] = self.img_true

            # Check status partial_book_depth if it is lost the connection
            if self.is_connection_pbd:
                if self.pbd_client is None:
                    self.is_connection_pbd = False
                else:
                    if not self.pbd_client.socket_manager.ws.connected:
                        self.is_connection_pbd = False

                if not self.is_connection_pbd:
                    self.update_form_pbd()

            self.update_canvas()

            # Save Canvas into file and DB
            if get_timestamp() - time_save_canvas >= delay_save_canvas:
                path1 = Path(pathlib.Path.cwd(), "images", "canvas.ps")
                self.canvas.postscript(file=path1, colormode="color")

                img = Image.open(path1)
                path2 = Path(pathlib.Path.cwd(), "images", "canvas.png")
                img.save(path2, "png")

                img_byte_arr = open(path2, "rb").read()

                db = MySqlCall()
                db.start_conn()
                db.save_image("canvas", img_byte_arr)
                db.stop_conn()

                time_save_canvas = get_timestamp()

            # Status
            if get_timestamp() - time_save_status >= delay_save_status:
                now = datetime.now()

                root = ET.Element('root')
                date = ET.SubElement(root, 'date')
                date.text = str(now.strftime("%d-%m-%Y %H:%M:%S"))
                if self.binance_price is not None:
                    binance = ET.SubElement(root, 'binance_price')
                    ask = ET.SubElement(binance, 'ask')
                    ask.text = str(self.binance_price['ask'])
                    bid = ET.SubElement(binance, 'bid')
                    bid.text = str(self.binance_price['bid'])
                    timestamp = ET.SubElement(binance, 'timestamp')
                    timestamp.text = str(self.binance_price['timestamp'])

                if self.spot_price is not None:
                    spot = ET.SubElement(root, 'spot_price')
                    ask = ET.SubElement(spot, 'ask')
                    ask.text = str(self.spot_price['ask'])
                    bid = ET.SubElement(spot, 'bid')
                    bid.text = str(self.spot_price['bid'])
                    timestamp = ET.SubElement(spot, 'timestamp')
                    timestamp.text = str(get_timestamp())

                if self.fut_price is not None:
                    fut_price = ET.SubElement(root, 'fut_price')
                    ask = ET.SubElement(fut_price, 'ask')
                    ask.text = str(self.fut_price['ask'])
                    bid = ET.SubElement(fut_price, 'bid')
                    bid.text = str(self.fut_price['bid'])
                    timestamp = ET.SubElement(fut_price, 'timestamp')
                    timestamp.text = str(get_timestamp())

                db = MySqlCall()
                db.start_conn()
                db.save_status(ET.tostring(root), now.strftime("%Y-%m-%d %H:%M:%S"))
                db.stop_conn()

                time_save_status = get_timestamp()

            time.sleep(sleep)

        self.label_global_img["image"] = self.img_false

    def update_form_pbd(self):
        if self.is_connection_pbd:
            self.canvas_connect_pbd["background"] = "green"
            self.label_connect_pbd_img["image"] = self.img_true
            self.btn_connect_pbd["text"] = "Stop PBD"
        else:
            self.canvas_connect_pbd["background"] = "red"
            self.label_connect_pbd_img["image"] = self.img_false
            self.btn_connect_pbd["text"] = "Start PBD"

    def target_thread_me(self):
        sleep = float(self.config.get("thread_me", "sleep"))

        while True:
            if self.is_db_connection:
                try:
                    prices_me = self.db.get_me_prices()
                    if self.spot_code in prices_me:
                        self.spot_price = {'ask': float(prices_me[self.spot_code]['ask']),
                                           'bid': float(prices_me[self.spot_code]['bid'])}
                    else:
                        self.spot_price = None

                    if self.fut_code in prices_me:
                        self.fut_price = {'ask': float(prices_me[self.fut_code]['ask']),
                                          'bid': float(prices_me[self.fut_code]['bid'])}
                    else:
                        self.fut_price = None

                    # self.my_logger.info(str(prices_me))
                except Exception as ex:
                    self.my_logger.error(f"call get_me_prices: {ex}")
                    break

            time.sleep(sleep)

    def click_connect_me(self):
        if not self.is_db_connection:
            self.db.start_conn()
            self.is_db_connection = True

            self.canvas_connect_me["background"] = "green"
            self.btn_connect_me["text"] = "Stop ME"

            self.my_logger.info("Connection ME is started")
        else:
            self.is_db_connection = False
            self.db.stop_conn()

            self.canvas_connect_me["background"] = "red"
            self.label_mysql_connect_img["image"] = self.img_false
            self.btn_connect_me["text"] = "Start ME"

            self.my_logger.info("Connection ME is stopped")

    def click_connect_pbd(self):
        if not self.is_connection_pbd:
            self.pbd_client = SpotWebsocketStreamClient(on_message=self.pbd_handler)
            self.pbd_client.partial_book_depth(symbol=self.binance_code, level=10, speed=1000)
            self.is_connection_pbd = True

            self.my_logger.info("Connection PBD is started")
        else:
            self.is_connection_pbd = False
            self.pbd_client.stop()

            self.my_logger.info("Connection PBD is stopped")

        self.update_form_pbd()

    def root_handler(self, event):
        if event.widget == self.root:
            self.update_canvas()

    def on_root_destroy(self, event):
        if event.widget == self.root:
            if self.is_connection_pbd:
                self.is_connection_pbd = False
                self.pbd_client.stop()

            if self.is_db_connection:
                self.is_db_connection = False
                self.db.stop_conn()

            self.my_logger.info("Han is stopped!")

    def init_canvas(self):
        self.canvas_dict = {}

        base_size = 500
        base_height = 400
        base_width = 50
        base_arrow_height = 60

        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()

        centre_x = int(width / 2)
        centre_y = int(height / 2)

        ratio = min(height, width)/base_size

        w_min = int(centre_x - ratio * base_width / 2)
        w_max = int(centre_x + ratio * base_width / 2)

        h_min = int(centre_y - ratio * base_height / 2)
        h_max = int(centre_y + ratio * base_height / 2)

        min_price = 90.5112
        max_price = 91.4912

        me_price = 90.9123
        b_price = 91.2123

        # Date and time
        x = 100
        y = 20
        self.canvas_dict['text_datetime'] = self.canvas.create_text(x, y, text=str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
                                                                                        fill=self.canvas['background'], font=('Helvetica 15'))

        # Base rectangle
        self.canvas_dict['rectangle_id'] = self.canvas.create_rectangle(w_min, h_min, w_max, h_max)

        # Text min, max
        x = (w_min + w_max)/2
        y = h_min - 30
        self.canvas_dict['text_min_id'] = self.canvas.create_text(x, y, text=str(min_price), fill=self.canvas['background'], font=('Helvetica 15 bold'))
        y = h_max + 30
        self.canvas_dict['text_max_id'] = self.canvas.create_text(x, y, text=str(max_price), fill=self.canvas['background'], font=('Helvetica 15 bold'))

        # Arrow ME
        if b_price is None:
            color = "black"
        elif me_price >= b_price:
            color = "red"
        else:
            color = "green"

        x1 = w_max + 10
        x2 = int(w_max + ratio * base_arrow_height)

        y = h_min + (h_max - h_min) * (me_price - min_price) / (max_price - min_price)
        self.canvas_dict['arrow_me_id'] = self.canvas.create_line(x1, y, x2, y, arrow="first", dash=(5, 2),
                                                                  fill=self.canvas['background'])

        x = x2 + 40
        y = y + 0
        self.canvas_dict['text_arrow_me_id'] = self.canvas.create_text(x, y, text="", # str(me_price),
                                                                       fill=self.canvas['background'],
                                                                       font=('Helvetica 15 bold'))

        # arrow Binance
        x1 = int(w_min - ratio * base_arrow_height)
        x2 = w_min

        if me_price is None:
            color = "black"
        else:
            if me_price < b_price:
                color = "red"
            else:
                color = "green"

            x = int((w_min + w_max)/2)
            y = int((h_min + h_max)/2)
            self.canvas_dict['text_delta_id'] = self.canvas.create_text(x, y,
                                                                        text="", # str(round(abs(b_price-me_price), 2)),
                                                                        fill=self.canvas['background'],
                                                                        font=('Helvetica 15 bold'))

            x = int((w_min + w_max)/2)
            y = int((h_min + h_max)/2 - 30)
            self.canvas_dict['text_min_delta_id'] = self.canvas.create_text(x, y,
                                                                        text="", # str(self.min_delta),
                                                                        # fill='blue',
                                                                        fill=self.canvas['background'],
                                                                        font=('Helvetica 15 bold'))

            x = int((w_min + w_max)/2)
            y = int((h_min + h_max)/2 + 30)
            self.canvas_dict['text_max_delta_id'] = self.canvas.create_text(x, y,
                                                                        text="", # str(self.max_delta),
                                                                        # fill='blue',
                                                                        fill=self.canvas['background'],
                                                                        font=('Helvetica 15 bold'))

        y = h_min + (h_max - h_min) * (b_price - min_price)/(max_price - min_price)

        self.canvas_dict['arrow_binance_id'] = self.canvas.create_line(x1, y, x2, y, arrow="last", dash=(5, 2),
                                                                       fill=self.canvas['background'])

        x = x2 - 90
        y = y + 0
        self.canvas_dict['text_arrow_binance_id'] = self.canvas.create_text(x, y, text=str(b_price),
                                                                            fill=self.canvas['background'],
                                                                            font=('Helvetica 15 bold'))

    def update_canvas(self):
        base_size = 500
        base_height = 400
        base_width = 70
        base_arrow_height = 60

        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()

        centre_x = int(width / 2)
        centre_y = int(height / 2)

        ratio = min(height, width)/base_size

        w_min = int(centre_x - ratio * base_width / 2)
        w_max = int(centre_x + ratio * base_width / 2)

        h_min = int(centre_y - ratio * base_height / 2)
        h_max = int(centre_y + ratio * base_height / 2)

        if self.binance_price is not None:
            b_price = round((self.binance_price['ask'] + self.binance_price['bid'])/2, 2)

            if self.min_price is None or self.max_price is None:
                self.min_price = round(self.binance_price['bid'] * 0.995, 2)
                self.max_price = round(self.binance_price['ask'] * 1.005, 2)
            else:
                self.min_price = min(self.min_price, self.binance_price['bid'])
                self.max_price = max(self.max_price, self.binance_price['ask'])
        else:
            b_price = None

        if self.spot_price is not None:
            me_price = round((self.spot_price['ask'] + self.spot_price['bid'])/2, 2)

            if self.min_price is None or self.max_price is None :
                self.min_price = round(self.spot_price['bid'] * 0.995, 2)
                self.max_price = round(self.spot_price['ask'] * 1.005, 2)
            else:
                self.min_price = min(self.min_price, self.spot_price['bid'])
                self.max_price = max(self.max_price, self.spot_price['ask'])
        else:
            if self.fut_price is not None:
                me_price = round((self.fut_price['ask'] + self.fut_price['bid']) / 2, 2)

                if self.min_price is None or self.max_price is None:
                    self.min_price = round(self.fut_price['bid'] * 0.995, 2)
                    self.max_price = round(self.fut_price['ask'] * 1.005, 2)
                else:
                    self.min_price = min(self.min_price, self.fut_price['bid'])
                    self.max_price = max(self.max_price, self.fut_price['ask'])
            else:
                me_price = None

        # Date and time
        self.canvas.itemconfig(self.canvas_dict['text_datetime'], fill='black',
                               text=str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

        # Base rectangle
        self.canvas.coords(self.canvas_dict['rectangle_id'], w_min, h_min, w_max, h_max)

        # view min_price and max_price
        if self.min_price is not None and self.max_price is not None:
            x = int((w_min + w_max)/2)
            y = h_min - 30
            self.canvas.coords(self.canvas_dict['text_min_id'], x, y)
            self.canvas.itemconfig(self.canvas_dict['text_min_id'], fill='black', text=str(self.min_price))

            x = int((w_min + w_max)/2)
            y = h_max + 30
            self.canvas.coords(self.canvas_dict['text_max_id'], x, y)
            self.canvas.itemconfig(self.canvas_dict['text_max_id'], fill='black', text=str(self.max_price))

        # arrow Binance
        if b_price is not None:
            x1 = int(w_min - ratio * base_arrow_height)
            x2 = w_min

            if me_price is None:
                color = "black"
            elif me_price < b_price:
                color = "red"
            else:
                color = "green"

            y = h_min + (h_max - h_min) * (b_price - self.min_price) / (self.max_price - self.min_price)
            self.canvas.coords(self.canvas_dict['arrow_binance_id'], x1, y, x2, y)
            self.canvas.itemconfig(self.canvas_dict['arrow_binance_id'], fill=color)

            x = w_min - 90
            y = y + 0
            self.canvas.coords(self.canvas_dict['text_arrow_binance_id'], x, y)
            self.canvas.itemconfig(self.canvas_dict['text_arrow_binance_id'], fill=color, text=str(b_price))

        # arrow ME
        if me_price is not None:
            x1 = w_max
            x2 = int(w_max + ratio * base_arrow_height)

            if b_price is None:
                color = "black"
            else:
                if me_price >= b_price:
                    color = "red"
                else:
                    color = "green"

                x = int((w_min + w_max)/2)
                y = int((h_min + h_max)/2)
                delta = round(abs(me_price - b_price), 2)
                self.canvas.coords(self.canvas_dict['text_delta_id'], x, y)
                self.canvas.itemconfig(self.canvas_dict['text_delta_id'], fill='black', text=str(delta))

                self.min_delta = round(min(self.min_delta, abs(b_price-me_price)), 2)

                x = int((w_min + w_max)/2)
                y = int((h_min + h_max)/2 - 30)
                self.canvas.coords(self.canvas_dict['text_min_delta_id'], x, y)
                self.canvas.itemconfig(self.canvas_dict['text_min_delta_id'], fill='blue', text=str(self.min_delta))

                self.max_delta = round(max(self.max_delta, abs(b_price-me_price)), 2)

                x = int((w_min + w_max)/2)
                y = int((h_min + h_max)/2 + 30)
                self.canvas.coords(self.canvas_dict['text_max_delta_id'], x, y)
                self.canvas.itemconfig(self.canvas_dict['text_max_delta_id'], fill='blue', text=str(self.max_delta))

            y = h_min + (h_max - h_min) * (me_price - self.min_price)/(self.max_price - self.min_price)
            self.canvas.coords(self.canvas_dict['arrow_me_id'], x1, y, x2, y)
            self.canvas.itemconfig(self.canvas_dict['arrow_me_id'], fill=color)

            x = int(w_max + ratio * base_arrow_height) + 30
            y = y + 0
            self.canvas.coords(self.canvas_dict['text_arrow_me_id'], x, y)
            self.canvas.itemconfig(self.canvas_dict['text_arrow_me_id'], fill=color, text=str(me_price))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HanApp()
    app.run()


