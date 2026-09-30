import json
from generator import generate


samples = [
    {
        "niche": "personal finance",
        "topic": "I automated my savings and forgot about it for two years",
        "target_seconds": 45
    },
    {
        "niche": "fitness",
        "topic": "Why shorter workouts can sometimes be easier to stick with",
        "target_seconds": 30
    },
    {
        "niche": "technology",
        "topic": "What actually happens when you type a website address into your browser",
        "target_seconds": 60
    },
    {
        "niche": "productivity",
        "topic": "The simple rule I use to stop checking my phone while working",
        "target_seconds": 30
    },
    {
        "niche": "career",
        "topic": "The mistake I made when applying for my first software job",
        "target_seconds": 45
    }
]


results = []

for index, sample in enumerate(samples, start=1):

    print(f"\nGenerating sample {index}/5...")

    result = generate(
        niche=sample["niche"],
        topic=sample["topic"],
        target_seconds=sample["target_seconds"]
    )

    output = {
        "sample": index,
        "input": sample,
        "output": result
    }

    results.append(output)

    print(f"Sample {index} generated successfully.")


with open("sample_outputs.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)


print("\nAll five samples generated.")
print("Saved to: sample_outputs.json")