# ask_bedrock.py
import argparse, json, pathlib, time, random
import boto3, botocore
from botocore.config import Config

REGION   = "us-east-2"
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"  # your inference profile ID

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    config=Config(retries={"max_attempts": 3, "mode": "standard"})
)

def ask(prompt: str, context: str = "") -> str:
    system = (
        "You are a careful analyst. Use ONLY the provided context to answer. "
        "If the answer is not clearly in the context, reply exactly: Not in context."
    )

    messages = []
    if context:
        messages.append({"role": "user", "content": [{"type": "text", "text": f"Context:\n{context}"}]})
    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 800,
        "temperature": 0.2,
        "system": system,
        "messages": messages,
    }

    # Call Bedrock with simple exponential backoff for throttling
    last_err = None
    for attempt in range(5):
        try:
            resp = bedrock.invoke_model(modelId=MODEL_ID, body=json.dumps(body))
            break
        except botocore.exceptions.ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code in ("ThrottlingException", "TooManyRequestsException") and attempt < 4:
                time.sleep(0.5 * (2 ** attempt) + random.random() * 0.25)
                continue
            last_err = e
            break
    if last_err:
        raise last_err

    payload = json.loads(resp["body"].read())
    text = "".join(b["text"] for b in payload.get("content", []) if b.get("type") == "text")
    return text.strip()

def main():
    p = argparse.ArgumentParser(description="Ask Bedrock with optional context file.")
    p.add_argument("--prompt", required=True)
    p.add_argument("--context-file")
    args = p.parse_args()

    ctx = pathlib.Path(args.context_file).read_text(encoding="utf-8") if args.context_file else ""
    print(ask(args.prompt, ctx))

if __name__ == "__main__":
    main()
