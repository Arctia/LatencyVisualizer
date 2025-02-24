import socket
import time
import json
import tkinter as tk
from threading import Thread
import sys
from typing import Dict, Any, Optional

class Config:
    def __init__(self):
        self.mode: str = ""
        self.host: str = ""
        self.port: int = 0
        self.color_ranges: Dict[str, int] = {}
        self.colors: Dict[str, str] = {}
    
    @classmethod
    def from_json(cls, json_path: str) -> 'Config':
        config = cls()
        with open(json_path, 'r') as f:
            data = json.load(f)
            config.mode = data['mode']
            config.host = data['host']
            config.port = data['port']
            config.color_ranges = data['color_ranges']
            config.colors = data['colors']
        return config
    
    def __str__(self) -> str:
        return f"Config(host={self.host}, port={self.port})"


class PingOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'green')
        
        self.root.geometry('130x60+20+50') #compact mode TODO others
        
        self.canvas = tk.Canvas(
            self.root,
            width=10,
            height=60,
            highlightthickness=0,
            bg='green'
        )
        self.canvas.pack(fill=tk.BOTH, expand=False)
        
        self.ping_label = tk.Label(
            self.canvas,
            width=9,
            text="-- ms",
            font=('Helvetica', 18),
            bg='#000000',
            fg='white',
            borderwidth=0,
        )
        self.ping_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        
        self.close_button = tk.Button(
            self.canvas,
            text="●",
            font=('Helvetica', 12),
            bg='#000000',
            fg='red',
            borderwidth=0,
            highlightthickness=0
        )
        self.close_button.place(relx=0.94, rely=0.5, anchor=tk.CENTER)
        self.close_button.bind('<Button-3>', self.on_right_click)
        self.root.wm_attributes('-alpha', 0.7)
        
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.close_button.bind('<Button-1>', self.start_drag)
        self.close_button.bind('<B1-Motion>', self.drag)

        self.current_ping = "--"
        
        self.ping_thread = Thread(target=self.measure_ping_continuously)
        self.ping_thread.daemon = True
        self.ping_thread.start()

    def measure_ping(self):
        host = conf.host
        port = conf.port
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            start_time = time.time()
            sock.connect((host, port))
            rtt = (time.time() - start_time) * 1000
            
            sock.close()
            return f"{rtt:.1f}"
        except socket.error:
            return "--"

    def on_right_click(self, *args, **kwargs):
        self.on_closing()

    def measure_ping_continuously(self):
        while True:
            self.current_ping = self.measure_ping()

            if self.current_ping == "--":
                color = conf.colors.get("critical", "red")
            elif float(self.current_ping) < conf.color_ranges.get("optimal", 50):
                color = conf.colors.get("optimal", "#00ee33")
            elif float(self.current_ping) < conf.color_ranges.get("good", 150):
                color = conf.colors.get("good", "#00cc55")
            elif float(self.current_ping) < conf.color_ranges.get("warn", 230):
                color = conf.colors.get("warn", "orange")
            else:
                color = conf.colors.get("critical", "red")
            
            self.ping_label.config(
                text=f"{int(float(self.current_ping))}",
                fg=color
            )
            time.sleep(1)

    def start_drag(self, event):
        self.dragging = True
        self.last_x = event.x_root - self.root.winfo_x()
        self.last_y = event.y_root - self.root.winfo_y()

    def drag(self, event):
        if self.dragging:
            x = event.x_root - self.last_x
            y = event.y_root - self.last_y
            self.root.geometry(f'+{int(x)}+{int(y)}')

    def on_closing(self):
        self.root.destroy()
        sys.exit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    conf = Config.from_json('config.json')
    overlay = PingOverlay()
    overlay.run()