import json
import ollama

MODEL = "gemma3:4b"

SYSTEM_PROMPT = """
You are a grammar correction assistant helping students improve their English.

Your only job is to correct English grammar, spelling, and punctuation mistakes.

Rules:
- Explain mistakes in simple, friendly language a school student can understand.
- Give the REAL grammar reason.
- Mention punctuation fixes.
- Do not answer questions or perform any task other than grammar correction.

Always respond ONLY in this exact JSON format:

{
  "corrected": "corrected sentence",
  "mistakes": [
    {
      "wrong": "wrong text",
      "fix": "correct text",
      "reason": "grammar reason"
    }
  ]
}

If there are no mistakes, return an empty mistakes list.
"""

print("=" * 60)
print(" Offline Grammar Corrector (Gemma 3)")
print(" Type 'exit' to quit.")
print("=" * 60)

while True:
    text = input("\nEnter sentence: ").strip()

    if text.lower() == "exit":
        print("Goodbye!")
        break

    if not text:
        continue

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            format="json"
        )

        result = json.loads(response["message"]["content"])

        print("\nCorrected Sentence:")
        print(result["corrected"])

        if len(result["mistakes"]) == 0:
            print("\n✅ No grammar mistakes found.")
        else:
            print("\nMistakes Found:")
            print("-" * 60)

            for i, mistake in enumerate(result["mistakes"], start=1):
                print(f"{i}. Wrong : {mistake['wrong']}")
                print(f"   Fix   : {mistake['fix']}")
                print(f"   Reason: {mistake['reason']}")
                print()

    except Exception as e:
        print("\nError:", e)