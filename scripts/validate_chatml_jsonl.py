import argparse
import json
import sys

REQUIRED_TAGS = ("<|user|>", "<|assistant|>")


def validate_line(obj, idx):
    errors = []
    if not isinstance(obj, dict):
        return [f"line {idx}: not a JSON object"]
    if "prompt" not in obj or "completion" not in obj:
        errors.append(f"line {idx}: missing 'prompt' or 'completion'")
        return errors
    prompt = obj.get("prompt", "")
    completion = obj.get("completion", "")
    if not isinstance(prompt, str) or not isinstance(completion, str):
        errors.append(f"line {idx}: 'prompt'/'completion' must be strings")
    for t in REQUIRED_TAGS:
        if t not in prompt:
            errors.append(f"line {idx}: prompt missing tag {t}")
    if prompt.strip().endswith("<|assistant|>") is False:
        errors.append(f"line {idx}: prompt should end with '<|assistant|>'")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="ChatML JSONL file to validate")
    args = parser.parse_args()

    total = 0
    errors = []
    with open(args.input, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
            except Exception as e:
                errors.append(f"line {i}: invalid JSON - {e}")
                continue
            errors.extend(validate_line(obj, i))

    if errors:
        print("Validation failed:")
        for e in errors[:50]:
            print(" -", e)
        print(f"Total errors: {len(errors)} on {total} lines")
        sys.exit(1)
    else:
        print(f"OK: {total} lines valid ChatML prompt/completion")


if __name__ == "__main__":
    main()
