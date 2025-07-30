import pandas as pd
from pathlib import Path


def classify(qs, crl):
    if qs >= 40 and crl >= 500:
        return 'PASS'
    elif 25 <= qs < 40 and crl >= 500:
        return 'REVIEW'
    else:
        return 'FAIL'


def parse_sequence_batch(data_root: Path):
    # Automatically detect the subfolder inside the selected data_root
    subfolders = [f for f in data_root.iterdir() if f.is_dir()]
    if len(subfolders) != 1:
        raise ValueError("The data folder must contain exactly one subfolder.")

    batch_folder = subfolders[0]

    # Find Excel summary
    excel_file = next(batch_folder.glob("*.xls*"), None)
    if not excel_file:
        raise FileNotFoundError("No Excel summary (.xls or .xlsx) found in the folder.")

    df = pd.read_excel(excel_file, engine='openpyxl' if excel_file.suffix == '.xlsx' else None)

    # Find .seq files
    seq_files = list(batch_folder.glob("*.seq"))
    seq_dir = batch_folder

    # Normalize and classify
    df['DNAName'] = df['DNAName'].astype(str).str.strip()
    df['status'] = df.apply(lambda row: classify(row['QualitySCore'], row['CRL']), axis=1)

    # Attach .seq content
    results = []
    for _, row in df.iterrows():
        dna_name = row['DNAName']
        seq_file = seq_dir / f"{dna_name}.seq"

        if not seq_file.exists():
            print(f"Warning: {seq_file.name} not found.")
            continue

        with open(seq_file, 'r') as f:
            sequence = f.read().strip()

        results.append({
            "TemplateName": row["TemplateName"],
            "DNAName": dna_name,
            "Primer": row["PrimerName"],
            "QualityScore": row["QualitySCore"],
            "CRL": row["CRL"],
            "Status": row["status"],
            "Sequence": sequence
        })

    return results