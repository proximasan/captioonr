import shutil
import os
import glob
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

class ImageCaptionGUI(ThemedTk):
    def __init__(self):
        super().__init__()

        self.title("☆━━━━CAPTIOONR━━━━☆")

        # Set the window size
        self.geometry("840x880")

        # Center the window on the screen
        self.center_window()

        self.set_theme("equilux")
        self.configure(bg="#464646")  # set background color to dark gray

        self.folder_path = StringVar()
        self.caption_text = StringVar()
        self.image_files = []
        self.image_index = 0

        self.content_frame = ttk.Frame(self)
        self.content_frame.place(anchor='center', relx=0.5, rely=0.5)

        self.image_file_label = ttk.Label(self.content_frame, text="")
        self.image_file_label.grid(row=2, column=1)
        if self.image_files:
            self.image_file_label.config(text=self.truncate_filename(self.image_files[self.image_index]))

        self.auto_save_mode = BooleanVar()

        # Bind arrow keys for navigation
        self.bind('<Left>', lambda e: self.show_prev_image())
        self.bind('<Right>', lambda e: self.show_next_image())

        # Bind Command+S and Ctrl+S for saving
        self.bind('<Command-s>', lambda e: self.save_and_show_done())
        self.bind('<Control-s>', lambda e: self.save_and_show_done())

        self.folder_label = ttk.Label(self.content_frame, text="Folder:")
        self.folder_label.grid(row=0, column=0, sticky=E)

        self.folder_entry = ttk.Entry(self.content_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1)

        self.browse_button = ttk.Button(self.content_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2)

        self.canvas = Canvas(self.content_frame, width=512, height=512, bg="#464646", highlightbackground="#464646")
        self.canvas.grid(row=1, column=0, columnspan=3)

        self.apply_to_all_label = ttk.Label(self.content_frame, text="Apply to all:")
        self.apply_to_all_label.grid(row=3, column=0, sticky=E)

        self.apply_to_all_entry = ttk.Entry(self.content_frame, width=35)
        self.apply_to_all_entry.grid(row=3, column=1, sticky=W)

        self.prepend_button = ttk.Button(self.content_frame, text="Prepend", command=self.prepend_to_all)
        self.prepend_button.grid(row=3, column=1, sticky=E)

        self.append_button = ttk.Button(self.content_frame, text="Append", command=self.append_to_all)
        self.append_button.grid(row=3, column=2)

        self.find_label = ttk.Label(self.content_frame, text="Find:")
        self.find_label.grid(row=4, column=0, sticky=E)

        self.find_entry = ttk.Entry(self.content_frame, width=35)
        self.find_entry.grid(row=4, column=1, sticky=W)

        self.remove_button = ttk.Button(self.content_frame, text="Remove", command=self.remove_from_all)
        self.remove_button.grid(row=4, column=2)

        self.replace_with_label = ttk.Label(self.content_frame, text="Replace with:")
        self.replace_with_label.grid(row=5, column=0, sticky=E)

        self.replace_entry = ttk.Entry(self.content_frame, width=35)
        self.replace_entry.grid(row=5, column=1, sticky=W)

        self.replace_button = ttk.Button(self.content_frame, text="Replace", command=self.replace_all)
        self.replace_button.grid(row=5, column=2)

        self.caption_padding = ttk.Label(self.content_frame, text="", padding=(0, 10))
        self.caption_padding.grid(row=6, column=0)

        self.caption_label = ttk.Label(self.content_frame, text="Caption:")
        self.caption_label.grid(row=7, column=0, sticky=E)

        self.caption_entry = Text(self.content_frame, height=6, width=55, bg="#414141", fg="#a6a6a6", highlightbackground="#2a2a2a", highlightcolor="#2a2a2a")
        self.caption_entry.configure(insertbackground="white", highlightthickness=1, relief=SOLID, padx=5, pady=5)
        self.caption_entry.grid(row=7, column=1, sticky=W)


        self.save_button = ttk.Button(self.content_frame, text="Save this", command=self.save_caption)
        self.save_button.grid(row=7, column=2)

        self.caption_padding = ttk.Label(self.content_frame, text="", padding=(0, 10))
        self.caption_padding.grid(row=8, column=0)


        self.backup_button = ttk.Button(self.content_frame, text="Backup txt-files", command=self.backup_txt_files)
        self.backup_button.grid(row=9, column=0, sticky=W)

        self.create_caption_button = ttk.Button(self.content_frame, text="Create txt-file for each img", command=self.create_caption_files)
        self.create_caption_button.grid(row=9, column=1, sticky=W)

        self.auto_save_check = ttk.Checkbutton(self.content_frame, text="Save when moving", variable=self.auto_save_mode)
        self.auto_save_check.grid(row=9, column=1, sticky=E)

        self.prev_button = ttk.Button(self.content_frame, text="Previous", command=self.show_prev_image)
        self.prev_button.grid(row=9, column=2)

        self.next_button = ttk.Button(self.content_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=9, column=3)

    def save_and_show_done(self):
        self.save_caption()
        self.show_done_message(self.save_button, "Save this")


    def show_done_message(self, button, original_text):
        button.config(text="Done!")
        self.after(1000, lambda: button.config(text=original_text))

    def truncate_filename(self, filename, max_length=40):
        if len(filename) <= max_length:
            return filename
        else:
            return '...' + filename[-max_length+3:]

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
        img.thumbnail((512, 512), Image.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img_tk)
        self.image_file_label.config(text=self.truncate_filename(os.path.basename(img_path)))

        txt_path = self.get_txt_path(img_path)
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                self.caption_entry.delete("1.0", "end") # clear existing caption text
                self.caption_entry.insert("1.0", f.read()) # insert new caption text from file
        else:
            self.caption_entry.delete("1.0", "end") # clear caption text if file doesn't exist



    def remove_from_all(self):
        modify_str = self.find_entry.get()

        self.remove_button.config(text="Working...")
        self.update_idletasks()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'r') as f:
                    content = f.read()

                new_content = content.replace(modify_str, "")

                with open(txt_path, 'w') as f:
                    f.write(new_content)

                # update the caption text
                with open(txt_path, 'r') as f:
                    self.caption_text.set(f.read())

        self.show_done_message(self.remove_button, "Remove")

        # add delay before updating the image caption
        self.after(500, self.show_image)



    def show_prev_image(self):
        if not self.image_files:
            return

        if self.auto_save_mode.get():  # If auto save mode is on, save the caption before navigating
            self.save_caption()

        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.image_files) - 1

        self.show_image()

    def show_next_image(self):
        if not self.image_files:
            return

        if self.auto_save_mode.get():  # If auto save mode is on, save the caption before navigating
            self.save_caption()

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

        self.show_done_message(self.create_caption_button, "Create txt-files for each img")

    def replace_all(self):
        modify_str = self.find_entry.get()
        replace_str = self.replace_entry.get()

        self.replace_button.config(text="Working...")
        self.update_idletasks()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'r') as f:
                    content = f.read()

                new_content = content.replace(modify_str, replace_str)

                with open(txt_path, 'w') as f:
                    f.write(new_content)

        self.show_done_message(self.replace_button, "Replace")

        # add delay before updating the image caption
        self.after(500, self.show_image)




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
            f.write(self.caption_entry.get("1.0", "end-1c"))

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
        modify_str = self.apply_to_all_entry.get()

        self.prepend_button.config(text="Working...")
        self.update_idletasks()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'r') as f:
                    content = f.read()

                new_content = modify_str + content

                with open(txt_path, 'w') as f:
                    f.write(new_content)

                # update the caption text
                with open(txt_path, 'r') as f:
                    self.caption_entry.delete("1.0", "end")
                    self.caption_entry.insert("1.0", f.read())

        self.show_done_message(self.prepend_button, "Prepend")


    def append_to_all(self):
        modify_str = self.apply_to_all_entry.get()

        self.append_button.config(text="Working...")
        self.update_idletasks()

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                with open(txt_path, 'r') as f:
                    content = f.read()

                new_content = content + modify_str

                with open(txt_path, 'w') as f:
                    f.write(new_content)

                # update the caption text
                with open(txt_path, 'r') as f:
                    self.caption_entry.delete("1.0", "end")
                    self.caption_entry.insert("1.0", f.read())

        self.show_done_message(self.append_button, "Append")

    def backup_txt_files(self):
        self.backup_button.config(text="Working...")
        self.update_idletasks()

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

        backup_folder = os.path.join(self.folder_path.get(), f"backup_{dt_string}")
        os.makedirs(backup_folder)

        for img_path in self.image_files:
            txt_path = self.get_txt_path(img_path)
            if os.path.exists(txt_path):
                shutil.copy(txt_path, backup_folder)

        self.show_done_message(self.backup_button, "Backup txt-files")


if __name__ == "__main__": 
    gui = ImageCaptionGUI() 

    gui.protocol("WM_DELETE_WINDOW", gui.on_closing)
    gui.mainloop()