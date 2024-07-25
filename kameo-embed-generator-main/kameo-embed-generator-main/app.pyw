import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from function import generate_html
from r2 import upload_directory
from dotenv import load_dotenv

# Load .env file
load_dotenv()

r2_bucket_name = os.getenv('R2_BUCKET_NAME')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kameo EMBED GENERATOR BY KZYWEB")
        self.root.geometry("600x400")
        self.root.resizable(False, False)  
        self.root.configure(bg="#f0f0f0")

        # Title
        self.title_label = tk.Label(root, text="Kameo EMBED GENERATOR", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        # Main Frame
        self.main_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", borderwidth=1)
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Select Resolution
        self.resolution_label = tk.Label(self.main_frame, text="Select resolution:", font=("Helvetica", 10), bg="#ffffff")
        self.resolution_label.grid(row=0, column=0, sticky="w", pady=5)
        self.resolution_var = tk.StringVar(value="1080p")
        self.resolution_menu = ttk.Combobox(self.main_frame, textvariable=self.resolution_var, values=["1080p", "720p"], state="readonly")
        self.resolution_menu.grid(row=0, column=1, pady=5, sticky="ew")

        # M3U8 Link
        self.m3u8_label = tk.Label(self.main_frame, text="M3U8 Link:", font=("Helvetica", 10), bg="#ffffff")
        self.m3u8_label.grid(row=1, column=0, sticky="w", pady=5)
        self.m3u8_entry = tk.Entry(self.main_frame, width=50)
        self.m3u8_entry.grid(row=1, column=1, pady=5, sticky="ew")

        # Folder Name
        self.folder_label = tk.Label(self.main_frame, text="Folder Name:", font=("Helvetica", 10), bg="#ffffff")
        self.folder_label.grid(row=2, column=0, sticky="w", pady=5)
        self.folder_entry = tk.Entry(self.main_frame, width=50)
        self.folder_entry.grid(row=2, column=1, pady=5, sticky="ew")

        # Image Link
        self.image_label = tk.Label(self.main_frame, text="Image Link:", font=("Helvetica", 10), bg="#ffffff")
        self.image_label.grid(row=3, column=0, sticky="w", pady=5)
        self.image_entry = tk.Entry(self.main_frame, width=50)
        self.image_entry.grid(row=3, column=1, pady=5, sticky="ew")

        # Browse .srt File
        self.srt_label = tk.Label(self.main_frame, text="Browse .srt file:", font=("Helvetica", 10), bg="#ffffff")
        self.srt_label.grid(row=5, column=0, sticky="w", pady=5)
        self.srt_button = tk.Button(self.main_frame, text="Browse", command=self.browse_srt, state="disabled")
        self.srt_button.grid(row=5, column=1, sticky="ew", pady=5)
        self.srt_file_label = tk.Label(self.main_frame, text="", font=("Helvetica", 10), bg="#ffffff")
        self.srt_file_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")  # Affichage en bas du bouton

        # Do you need subtitles
        self.subtitles_var = tk.BooleanVar()
        self.subtitles_check = tk.Checkbutton(self.main_frame, text="Do you need subtitles?", variable=self.subtitles_var, command=self.toggle_subtitles, bg="#ffffff", font=("Helvetica", 10))
        self.subtitles_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Generate HTML Button
        self.generate_button = tk.Button(self.button_frame, text="Generate HTML", command=self.generate_html, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.pack(side="left", padx=10)

        # Send to R2 Button
        self.send_button = tk.Button(self.button_frame, text="Send to R2", command=self.send_to_r2, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"))
        self.send_button.pack(side="left", padx=10)

        # Initialize srt_path
        self.srt_path = None

    def toggle_subtitles(self):
        if self.subtitles_var.get():
            self.srt_button.config(state="normal")
        else:
            self.srt_button.config(state="disabled")
            self.srt_file_label.config(text="")

    def browse_srt(self):
        self.srt_path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        if self.srt_path:
            self.srt_file_label.config(text=os.path.basename(self.srt_path))

    def generate_html(self):
        m3u8_link = self.m3u8_entry.get()
        folder_name = self.folder_entry.get()
        use_subtitles = self.subtitles_var.get()
        image_link = self.image_entry.get()
        is720 = self.resolution_var.get() == "720p"
        generate_html(m3u8_link, use_subtitles, image_link, is720, folder_name, self.srt_path)
        messagebox.showinfo("Success", f"HTML files have been generated in the folder: {folder_name}")

    def send_to_r2(self):
        folder_name = self.folder_entry.get()
        directory_path = os.path.join('Build', folder_name)
        if os.path.exists(directory_path):
            upload_directory(directory_path, r2_bucket_name, folder_name)
            messagebox.showinfo("Success", f"Folder '{folder_name}' has been uploaded to R2")
        else:
            messagebox.showerror("Error", f"Folder '{folder_name}' does not exist")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
