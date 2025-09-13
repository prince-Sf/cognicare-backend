import threading
import tkinter as tk
from tkinter import ttk
import random
from Cognicare import query_cognicare

BG_MAIN = "#222834"
BG_BOT_BUBBLE = "#8D84E2"
BG_USER_BUBBLE = "#5FDDE6"
BG_INPUT = "#343d4d"
FG_CHAT = "#222834"
FG_INPUT = "#ECDBBA"

class CognicareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognicare 💙")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_MAIN)

        chat_frame = tk.Frame(self.root, bg=BG_MAIN)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(chat_frame, bg=BG_MAIN, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_MAIN)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", self._resize_window)

        input_frame = tk.Frame(self.root, bg=BG_INPUT)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.user_entry = tk.Entry(
            input_frame, font=("Segoe UI", 12),
            bg=BG_INPUT, fg=FG_INPUT,
            insertbackground=FG_INPUT, relief="flat"
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 8), ipady=12)
        self.user_entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(
            input_frame, text="Send ➤", font=("Segoe UI", 12, "bold"),
            bg="#6185a8", fg="#ECDBBA", relief="flat",
            activebackground="#41546b", activeforeground="#ECDBBA",
            command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT, padx=(2, 14), ipadx=20, ipady=8)

        intros = [
            "Hi, I’m Cognicare. How are you feeling today? 💙",
            "Hello! I’m Cognicare, your support companion. What’s on your mind? 🌸",
            "Hey there, this is Cognicare. How can I be here for you today? 🤗",
            "Hi! I’m Cognicare. Would you like to share how your day is going? 🌼",
            "Hello, I’m Cognicare. How are things with you right now? 💫",
            "Hi, this is Cognicare. What’s something you’d like to talk about today? 🌷"
        ]
        self.add_bubble(intros[random.randint(0, len(intros) - 1)], is_user=False)

    def _resize_window(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=canvas_width)

    def add_bubble(self, text, is_user):
        outer = tk.Frame(self.scrollable_frame, bg=BG_MAIN)
        bubble_color = BG_USER_BUBBLE if is_user else BG_BOT_BUBBLE
        if not is_user:
            text = "🤖 " + text
        bubble = tk.Label(
            outer, text=text, bg=bubble_color, fg=FG_CHAT,
            wraplength=500, justify='left', font=("Segoe UI", 12), padx=16, pady=8,
            bd=0, relief="flat"
        )
        if is_user:
            bubble.pack(side=tk.RIGHT, padx=(10, 30), pady=8)
        else:
            bubble.pack(side=tk.LEFT, padx=(30, 10), pady=8)
        outer.pack(fill=tk.X, expand=True)
        self.scrollable_frame.update_idletasks()
        self.canvas.yview_moveto(1)
        return outer

    def send_message(self, event=None):
        user_input = self.user_entry.get().strip()
        if not user_input:
            return
        if len(user_input) > 300:
            user_input = user_input[:300] + "..."
        self.add_bubble(user_input, is_user=True)
        self.user_entry.delete(0, tk.END)
        self.user_entry.config(state=tk.DISABLED)
        typing_bubble = self.add_bubble("Cognicare is typing...", is_user=False)

        def get_bot_reply():
            bot_reply = query_cognicare(user_input)

            # ✂️ Shorten the reply to 2 sentences max
            sentences = bot_reply.split(". ")
            if len(sentences) > 2:
                bot_reply = ". ".join(sentences[:2]) + "."

            def finish():
                typing_bubble.destroy()
                self.user_entry.config(state=tk.NORMAL)
                self.add_bubble(bot_reply.strip(), is_user=False)

            self.root.after(0, finish)

        t = threading.Thread(target=get_bot_reply)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CognicareApp(root)
    root.mainloop()
