from pathlib import Path
from src.parser import parse_sequence_batch
from src.blaster import blast_sequence
from src.writer import write_results_to_excel

def main():
    input_folder = Path("data/oxana_sequences")
    output_file = Path("output/results.xlsx")

    # Step 1: Parse
    print("Parsing input data...")
    samples = parse_sequence_batch(input_folder)

    # Step 2: BLAST each sample
    print("Running BLAST...")
    for sample in samples:
        print(f"Blasting sequence for: {sample['TemplateName']}")
        blast_result = blast_sequence(sample['Sequence'])

        if blast_result:
            sample.update(blast_result)
        else:
            print(f"No BLAST result for {sample['TemplateName']}")
            sample.update({
                "HitID": None,
                "HitDef": None,
                "Length": None,
                "Identity": None,
                "E-value": None,
                "Accession": None
            })

    # Step 3: Write to Excel
    write_results_to_excel(samples, output_file)

if __name__ == "__main__":
    main()
