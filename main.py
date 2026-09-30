from generator import generate


result = generate(
    niche="personal finance",
    topic="I automated my savings and forgot about it for two years",
    target_seconds=45
)


print("\n" + "=" * 60)
print("GENERATED SCRIPT")
print("=" * 60)

print("\nHOOK")
print(result["hook"])

print("\nBODY")
print(result["body"])

print("\nCTA")
print(result["cta"])

print("\n" + "-" * 60)
print(f"Target duration : {result['target_words']} words")
print(f"Actual word count: {result['word_count']} words")
print(f"Estimated runtime: {result['estimated_seconds']} seconds")
print("-" * 60)