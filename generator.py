import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def count_words(result):
    text = " ".join([
        result["hook"],
        result["body"],
        result["cta"]
    ])

    return len(text.split())

def is_valid_length(word_count, target_words):
    minimum = int(target_words * 0.90)
    maximum = int(target_words * 1.10)

    return minimum <= word_count <= maximum


def validate_script(result):
    required_fields = ["hook", "body", "cta"]

    # Check required fields
    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Missing required field: {field}"
            )

    # Check field types and values
    for field in required_fields:

        if not isinstance(result[field], str):
            raise ValueError(
                f"{field} must be a string"
            )

        if not result[field].strip():
            raise ValueError(
                f"{field} cannot be empty"
            )

    return result


def call_model(prompt, max_retries=2):

    for attempt in range(max_retries + 1):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()

            # Remove markdown code fences if Gemini adds them
            if result.startswith("```"):
                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

            return result

        except Exception as e:

            if attempt == max_retries:
                raise RuntimeError(
                    "Failed to generate script after multiple attempts."
                ) from e


def generate(niche, topic, target_seconds):

    # -------------------------
    # Input validation
    # -------------------------

    if not niche.strip():
        raise ValueError("Niche cannot be empty.")

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if target_seconds <= 0:
        raise ValueError(
            "Target seconds must be greater than 0."
        )

    # -------------------------
    # Calculate target words
    # -------------------------

    target_words = int(target_seconds * 2.5)

    minimum_words = int(target_words * 0.90)
    maximum_words = int(target_words * 1.10)

    # -------------------------
    # Create prompt
    # -------------------------

    prompt = f"""
You are an expert short-form video scriptwriter.

Create a short-form video script for a creator in the following niche.

Niche:
{niche}

Topic:
{topic}

Target duration:
{target_seconds} seconds

Target word count:
Approximately {target_words} words.

Acceptable word-count range:
{minimum_words} to {maximum_words} words.

REQUIREMENTS:

1. HOOK
- The first sentence must immediately create curiosity.
- Make the viewer want to keep watching.
- Do not start with:
  "Today I'm going to talk about..."
  "In this video..."
  "Let's talk about..."

2. BODY
- Focus on one clear idea.
- Make it conversational and natural when spoken.
- Use a concrete example only when it helps explain the topic.
- Do not invent facts, statistics, numbers, dates, financial amounts,
  time durations, frequencies, achievements, or personal experiences.
- Do not invent actions or outcomes that the creator supposedly experienced.
- If the topic is written in first person, only use the personal facts
  explicitly provided in the topic.
- Do not introduce details such as "$50", "hundreds of applications",
  "three months", "every payday", or "20 minutes" unless they appear
  in the input.
- Keep unsupported details generic.
- Avoid unnecessary explanations.
- Avoid generic AI-sounding language.

3. CTA
- End with a short and natural call-to-action.
- The CTA should be relevant to the topic.
- Avoid aggressive marketing language.

4. LANGUAGE QUALITY
- Use normal spaces between words.
- Make sure there is a space after every sentence-ending punctuation mark.
- Never produce text such as "it.Seriously" or "drop.It".
- Use clear, natural sentences.
- Avoid awkward punctuation.
- Avoid excessive ellipses.
- Make the script sound natural when spoken aloud.

5. TIMING
- Stay within the acceptable word-count range.
- Target approximately {target_words} words.
- The final script MUST contain between {minimum_words} and {maximum_words} words.
- Do not sacrifice natural language just to hit an exact number.

OUTPUT FORMAT:

Return ONLY valid JSON.

Before returning the JSON, check that:
- hook, body, and cta are non-empty strings.
- There are spaces between all words.
- There are no accidentally concatenated words.
- No unsupported specific facts or personal experiences were added.
- The total word count is between {minimum_words} and {maximum_words}.

{{
    "hook": "string",
    "body": "string",
    "cta": "string"
}}
"""

    # -------------------------
    # Generate and validate
    # -------------------------

    max_generation_attempts = 3

    for attempt in range(max_generation_attempts):

        result = call_model(prompt)

        # -------------------------
        # Parse JSON
        # -------------------------

        try:
            script = json.loads(result)

        except json.JSONDecodeError as e:

            if attempt == max_generation_attempts - 1:
                raise ValueError(
                    "Gemini returned invalid JSON after multiple attempts."
                ) from e

            prompt += """
The previous response was not valid JSON.

Regenerate the script and return ONLY valid JSON.
"""

            continue

        # -------------------------
        # Validate structure
        # -------------------------

        try:
            script = validate_script(script)

        except ValueError as e:

            if attempt == max_generation_attempts - 1:
                raise

            prompt += f"""

The previous response failed validation:

{str(e)}

Regenerate the script and return ONLY valid JSON.
"""

            continue

        # -------------------------
        # Calculate word count
        # -------------------------

        word_count = count_words(script)

        # -------------------------
        # Validate length
        # -------------------------

        if is_valid_length(word_count, target_words):

            estimated_seconds = round(
                word_count / 2.5,
                1
            )

            script["word_count"] = word_count
            script["target_words"] = target_words
            script["estimated_seconds"] = estimated_seconds

            return script

        # -------------------------
        # Ask model to fix length
        # -------------------------

        if attempt < max_generation_attempts - 1:

            prompt += f"""

The previous script contained {word_count} words.

The target is approximately {target_words} words.

The acceptable range is {minimum_words} to {maximum_words} words.

Regenerate the script so that the total word count falls within
that range.

Keep the same topic and niche.

Do not add unsupported facts or specific numbers.

Return ONLY valid JSON.
"""

    # -------------------------
    # All attempts failed
    # -------------------------

    raise ValueError(
        f"Could not generate a script within the required length "
        f"after {max_generation_attempts} attempts. "
        f"Target: {target_words} words."
    )