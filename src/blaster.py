import time
import requests
from Bio.Blast import NCBIXML
from io import StringIO

NCBI_BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

def blast_sequence(seq, program="blastn", database="nt"):
    # Step 1: Submit job
    params = {
        "CMD": "Put",
        "PROGRAM": program,
        "DATABASE": database,
        "QUERY": seq,
    }
    print("Submitting sequence to NCBI BLAST...")
    response = requests.post(NCBI_BLAST_URL, data=params)
    if response.status_code != 200:
        raise RuntimeError(f"BLAST request failed: {response.status_code}")

    rid_line = next((line for line in response.text.splitlines() if "RID =" in line), None)
    rtoe_line = next((line for line in response.text.splitlines() if "RTOE =" in line), None)

    if not rid_line or not rtoe_line:
        raise RuntimeError("Failed to retrieve RID or RTOE from BLAST response.")

    rid = rid_line.split("=")[1].strip()
    rtoe = int(rtoe_line.split("=")[1].strip())
    print(f"RID: {rid}, estimated wait: {rtoe}s")
    time.sleep(rtoe + 2)

    # Step 2: Poll for results
    while True:
        check_params = {
            "CMD": "Get",
            "RID": rid,
            "FORMAT_OBJECT": "SearchInfo"
        }
        check_response = requests.get(NCBI_BLAST_URL, params=check_params)
        status = check_response.text
        if "Status=READY" in status and "ThereAreHits=yes" in status:
            break
        elif "Status=FAILED" in status or "Status=UNKNOWN" in status:
            raise RuntimeError("BLAST job failed or expired.")
        print("Waiting for BLAST to finish...")
        time.sleep(3)

    # Step 3: Retrieve results
    result_params = {
        "CMD": "Get",
        "RID": rid,
        "FORMAT_TYPE": "XML"
    }
    result_response = requests.get(NCBI_BLAST_URL, params=result_params)
    blast_record = NCBIXML.read(StringIO(result_response.text))

    if not blast_record.alignments:
        return None  # No hits found

    top_hit = blast_record.alignments[0]
    hsp = top_hit.hsps[0]

    return {
        "HitID": top_hit.hit_id,
        "HitDef": top_hit.hit_def,
        "Length": top_hit.length,
        "Identity": hsp.identities / hsp.align_length * 100,
        "E-value": hsp.expect,
        "Accession": top_hit.accession
    }
