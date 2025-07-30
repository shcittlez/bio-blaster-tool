import pandas as pd
import os
import platform
import subprocess
from pathlib import Path

def write_to_excel(samples: list[dict], output_path: Path):
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(samples)

    # Drop unwanted columns
    df = df.drop(columns=["DNAName", "HitID"], errors='ignore')

    # Rename for clarity
    df = df.rename(columns={"HitDef": "TopHit"})

    # Reorder and keep only relevant columns
    desired_columns = [
        "TemplateName", "Primer", "Sequence",
        "TopHit", "Length", "Identity", "E-value", "Accession"
    ]
    df = df[[col for col in desired_columns if col in df.columns]]

    # Save to Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"✅ Results written to {output_path}")

    # Open file automatically
    try:
        if platform.system() == "Windows":
            os.startfile(output_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", output_path])
        else:
            subprocess.call(["xdg-open", output_path])
    except Exception as e:
        print(f"Unable to open file automatically: {e}")
