import os
import glob
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

class ImageCaptionGUI(ThemedTk):
    def __init__(self):
        super().__init__()

        self.title("☆━━━━CAPTIOONR━━━━☆")

        # Set the window size
        self.geometry("768x690")

        # Center the window on the screen
        self.center_window()

        # Set the dark mode theme as default
        self.set_theme("equilux")
        self.configure(bg="#464646")  # set background color to dark gray

        self.folder_path = StringVar()
        self.caption_text = StringVar()
        self.image_files = []
        self.image_index = 0

        self.content_frame = ttk.Frame(self)
        self.content_frame.place(anchor='center', relx=0.5, rely=0.5)

        self.folder_label = ttk.Label(self.content_frame, text="Folder:")
        self.folder_label.grid(row=0, column=0, sticky=E)

        self.folder_entry = ttk.Entry(self.content_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1)

        self.browse_button = ttk.Button(self.content_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2)

        self.canvas = Canvas(self.content_frame, width=512, height=512, bg="#464646", highlightbackground="#464646")
        self.canvas.grid(row=1, column=0, columnspan=3)


        self.apply_to_all_label = ttk.Label(self.content_frame, text="Apply to all:")
        self.apply_to_all_label.grid(row=2, column=0, sticky=E)

        self.apply_to_all_entry = ttk.Entry(self.content_frame, width=35)
        self.apply_to_all_entry.grid(row=2, column=1, sticky=W)

        self.prepend_button = ttk.Button(self.content_frame, text="Prepend", command=self.prepend_to_all)
        self.prepend_button.grid(row=2, column=1, sticky=E)

        self.append_button = ttk.Button(self.content_frame, text="Append", command=self.append_to_all)
        self.append_button.grid(row=2, column=2)

        self.caption_label = ttk.Label(self.content_frame, text="Caption:")
        self.caption_label.grid(row=3, column=0, sticky=E)

        self.caption_entry = ttk.Entry(self.content_frame, textvariable=self.caption_text, width=50)
        self.caption_entry.grid(row=3, column=1)

        self.save_button = ttk.Button(self.content_frame, text="Save this", command=self.save_caption)
        self.save_button.grid(row=3, column=2)

        self.prev_button = ttk.Button(self.content_frame, text="Previous", command=self.show_prev_image)
        self.prev_button.grid(row=4, column=0)

        self.next_button = ttk.Button(self.content_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=4, column=2)

        self.create_caption_button = ttk.Button(self.content_frame, text="Create txt-files for each img", command=self.create_caption_files)
        self.create_caption_button.grid(row=5, column=0, columnspan=3)

    def show_done_message(self, button, original_text):
        button.config(text="Done!")
        self.after(1000, lambda: button.config(text=original_text))

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.folder_path.set(folder)
        self.image_files = sorted(glob.glob(os.path.join(folder, "*.*g")))
        self.image_index = 0
        self.show_image()

    def show_image(self):
        if not self.image_files:
            return

        img_path = self.image_files[self.image_index]
        img = Image.open(img_path)
        img.thumbnail((500, 500), Image.ANTIALIAS)

        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img_tk)

        txt_path = self.get_txt_path(img_path)
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                self.caption_text.set(f.read())
        else:
            self.caption_text.set("")

    def show_prev_image(self):
        if not self.image_files:
            return

        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.image_files) - 1

        self.show_image()

    def show_next_image(self):
        if not self.image_files:
            return

        self.image_index += 1
        if self.image_index >= len(self.image_files):
            self.image_index = 0

        self.show_image()

    def create_caption_files(self):
        self.create_caption_button.config(text="Working...")
        self.update_idletasks()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if not os.path.exists(txt_path):
                with open(txt_path, 'w') as f:
                    f.write("")

        self.show_done_message(self.create_caption_button, "Create txt-file for each img")



    def get_txt_path(self, img_path):
        base, ext = os.path.splitext(img_path)
        return base + '.txt'

    def save_caption(self):
        if not self.image_files:
            return

        img_path = self.image_files[self.image_index]
        txt_path = self.get_txt_path(img_path)

        self.save_button.config(text="Working...")
        self.update_idletasks()

        with open(txt_path, 'w') as f:
            f.write(self.caption_text.get())

        self.show_done_message(self.save_button, "Save this")

    def on_closing(self):
        self.save_caption()
        self.destroy()

    def modify_all_files(self, action):
        modify_str = self.apply_to_all_entry.get()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'r') as f:
                    content = f.read()

                if action == 'prepend':
                    new_content = modify_str + content
                elif action == 'append':
                    new_content = content + modify_str

                with open(txt_path, 'w') as f:
                    f.write(new_content)

    def prepend_to_all(self):
        self.prepend_button.config(text="Working...")
        self.update_idletasks()

        self.modify_all_files('prepend')
        self.show_done_message(self.prepend_button, "Prepend")

    def append_to_all(self):
        self.append_button.config(text="Working...")
        self.update_idletasks()

        self.modify_all_files('append')
        self.show_done_message(self.append_button, "Append")

if __name__ == "__main__": 
    gui = ImageCaptionGUI() 

    gui.protocol("WM_DELETE_WINDOW", gui.on_closing)
    gui.mainloop()