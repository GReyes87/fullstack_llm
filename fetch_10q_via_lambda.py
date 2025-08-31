# fetch_10q_via_lambda.py
import json, boto3, pathlib

REGION = "us-east-2"               # change if your Lambda 2 is in a different region
FUNC   = "lamba_two_giancarlos"   # <-- exact function name or full ARN

EVENT = {
    "request_type": "Quarter",
    "company": "AAPL",    # or "Apple Inc."
    "year": 2024,
    "quarter": 1          # your Lambda 2 handles 1 or "Q1"
}

OUTFILE = "apple_q1_2024_10q.txt"

def main():
    lam = boto3.client("lambda", region_name=REGION)
    resp = lam.invoke(FunctionName=FUNC, Payload=json.dumps(EVENT).encode("utf-8"))

    # If the function crashed, AWS sets FunctionError and the payload is an error JSON
    if "FunctionError" in resp:
        err_txt = resp["Payload"].read().decode("utf-8", errors="replace")
        print("Lambda invocation failed:", err_txt)
        return

    raw = resp["Payload"].read().decode("utf-8", errors="replace")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print("Unexpected payload (not JSON):", raw[:500])
        return

    if payload.get("statusCode") != 200:
        print("Lambda returned error:", payload)
        return

    # Body is json.dumps(doc) from Lambda 2, so decode once more
    text = json.loads(payload["body"])
    pathlib.Path(OUTFILE).write_text(text, encoding="utf-8")
    print(f"Wrote {OUTFILE} ({len(text):,} chars)")

if __name__ == "__main__":
    main()
