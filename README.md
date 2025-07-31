# 🔬 BioBlaster

**BioBlaster** is a lightweight desktop app for parsing DNA sequence files, running NCBI BLAST queries, and exporting annotated results to Excel.

![BioBlaster screenshot](https://your-image-link-here) <!-- Optional: add screenshot later -->

---

## ✨ Features

- 🧬 Batch parsing of `.seq` DNA sequence files
- 🌐 Automatic NCBI BLAST search for top hit alignment
- 📊 Exports to Excel with quality metrics
- 🖼️ Intuitive GUI (Tkinter-based)
- 💾 Standalone `.exe` — no Python install required

---

## 🚀 How to Use

1. **Run the app** (`.exe` download below)
2. **Select a folder** that contains:
   - A single subfolder containing `.seq` files
   - And a '.xls' .xlsx` (metadata) file inside the same folder 
3. **Click “Start”** — the app:
   - Parses your sequences, analyzing QS and CRL scores 
   - Submits to NCBI BLAST, one at a time, (can be long) avoid midday US time
   - Writes results to Excel reporting Sample Name, Primer, Sequence, Top Hit on NCBI with Accession #, Sequence Length, % Identitity, E - Value
4. The output Excel file opens automatically

---

## 📥 Download

👉 [**Download BioBlaster (.exe)**](https://github.com/shcittlez/bio-blaster-tool/releases/download/v1.0.0/BioBlaster.exe)

> 💡 Just download and run — no install needed.

---

## 🛠️ Developer Setup (optional)

Want to modify or run from source?

```bash
git clone https://github.com/shcittlez/bio-blaster-tool.git
cd bio-blaster-tool
pip install -r requirements.txt
python gui.py
