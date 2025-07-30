import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pathlib import Path
import threading

from src import parser, blaster, writer

class BioBlastGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BioBlast Tool")

        self.folder_path = tk.StringVar()
        self.status_text = tk.StringVar()
        self.progress = tk.DoubleVar()

        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Select Data Folder").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.folder_path, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_folder).grid(row=0, column=2)

        tk.Button(self.root, text="Run BioBlast", command=self.run_pipeline_threaded).grid(row=1, column=1, pady=10)
        tk.Label(self.root, textvariable=self.status_text, fg="blue").grid(row=2, column=0, columnspan=3)

        self.progress_bar = Progressbar(self.root, variable=self.progress, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def run_pipeline_threaded(self):
        thread = threading.Thread(target=self.run_pipeline)
        thread.start()

    def run_pipeline(self):
        try:
            folder = Path(self.folder_path.get())
            if not folder.exists():
                raise FileNotFoundError("Folder does not exist.")

            self.status_text.set("Parsing sequences...")
            samples = parser.parse_sequence_batch(folder)
            total = len(samples)
            if total == 0:
                raise ValueError("No valid samples found.")

            for i, sample in enumerate(samples):
                self.status_text.set(f"Blasting {sample['TemplateName']} ({i+1}/{total})")
                result = blaster.blast_sequence(sample['Sequence'])
                sample.update(result)
                self.progress.set((i + 1) / total * 100)
                self.root.update_idletasks()

            self.status_text.set("Writing to results.xlsx...")
            writer.write_to_excel(samples, folder / "results.xlsx")

            self.status_text.set("Done! Results saved to results.xlsx")
            messagebox.showinfo("Success", "All done! ✅")

        except Exception as e:
            self.status_text.set("Error occurred.")
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = BioBlastGUI(root)
    root.mainloop()
