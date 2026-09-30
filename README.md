# Script-bench - Short-Form Video Script Generator

An AI-powered short-form video script generator that creates structured scripts from a niche, topic, and target video duration.

The generator uses **Google Gemini 2.5 Flash** to produce a script with three sections:

- **Hook** - captures attention immediately
- **Body** - explains the main idea conversationally
- **CTA** - provides a short, relevant call-to-action

The generated script is automatically validated for structure, word count, and estimated runtime.

---

## Features

- Generate short-form scripts using **Google Gemini 2.5 Flash**
- Accepts:
  - Niche
  - Topic
  - Target duration
- Produces structured JSON output
- Separates every script into:
  - Hook
  - Body
  - CTA
- Calculates target word count based on approximately **2.5 words/second**
- Validates generated script length within a **90%-110% range**
- Automatically retries when the generated script is outside the required length
- Validates required output fields
- Handles invalid JSON responses
- Includes API retry handling
- Generates multiple sample scripts automatically
- Stores the five required examples in `sample_outputs.json`

---

## Tech Stack

- **Python**
- **Google Gemini 2.5 Flash**
- **Google GenAI SDK**
- **python-dotenv**
- **JSON**

---

## How It Works

The generator follows this pipeline:


User Input
    |
    v
Niche + Topic + Target Duration
    |
    v
Calculate Target Word Count
    |
    v
Build Structured Prompt
    |
    v
Gemini 2.5 Flash
    |
    v
Parse JSON Response
    |
    v
Validate Hook / Body / CTA
    |
    v
Validate Word Count
    |
    +---- Outside Range ----> Regenerate

Input

The main function is:

generate(
    niche="personal finance",
    topic="I automated my savings and forgot about it for two years",
    target_seconds=45
)
Parameters
Parameter	Description
niche	Content category such as finance, fitness, technology, or career
topic	Main idea of the short-form video
target_seconds	Desired video duration in seconds
Output

The generator returns a structured dictionary containing:

{
    "hook": "Attention-grabbing opening",
    "body": "Main explanation of the topic",
    "cta": "Short call-to-action",
    "word_count": 106,
    "target_words": 112,
    "estimated_seconds": 42.4
}

The required content fields are:

hook
body
cta

The additional fields provide validation and timing information.

Timing and Word Count

The generator estimates approximately 2.5 spoken words per second.

For example:

45 seconds × 2.5 words/second = 112 target words

The generator accepts scripts within:

90% - 110% of the target word count

For a 45-second script:

Target = 112 words

Minimum = 100 words
Maximum = 123 words

If the generated script falls outside this range, the generator automatically asks Gemini to regenerate it.

Output Validation

The generator performs several validation checks.

1. Input validation

It checks that:

Niche is not empty
Topic is not empty
Target duration is greater than zero
2. JSON validation

The Gemini response must be valid JSON.

3. Structure validation

The response must contain:

hook
body
cta

Each field must be:

Present
A string
Non-empty
4. Length validation

The complete script is checked against the required word-count range.

5. Runtime estimation

The final runtime is calculated using:

estimated_seconds = round(word_count / 2.5, 1)
Retry Handling

The project uses two levels of retry handling.

API Retry

If the Gemini API request fails, the model call is retried automatically.

Generation Quality Retry

If Gemini returns valid JSON but the script is outside the required word-count range, the generator requests a new version.

This separates:

API failures

from:

Generated-content validation failures
Project Structure
Script-bench/
│
├── generator.py
├── main.py
├── generate_samples.py
├── sample_outputs.json
├── requirements.txt
├── .gitignore
└── README.md
generator.py

Contains the main script-generation logic, validation, retry handling, and timing calculations.

main.py

Provides a simple example of calling the generator for a single script.

generate_samples.py

Generates five different sample scripts across different niches and runtimes.

sample_outputs.json

Contains the generated outputs for all five sample inputs.

requirements.txt

Contains the Python dependencies required to run the project.

Installation
1. Clone the repository
git clone <https://github.com/realme321/script-bench.git>
cd Script-bench
2. Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key

The API key is loaded using python-dotenv.

The .env file is excluded from Git using .gitignore and should never be committed to the repository.

Run the Generator

To generate one example script:

python main.py

To generate all five sample scripts:

python generate_samples.py

The generated samples are saved to:

sample_outputs.json
Sample Inputs

The project includes five sample cases:

#	Niche	Target Duration
1	Personal Finance	45 seconds
2	Fitness	30 seconds
3	Technology	60 seconds
4	Productivity	30 seconds
5	Career	45 seconds

These examples demonstrate that the generator can handle different content categories and target runtimes.

What Makes a Good Short-Form Script?

A good short-form script should:

1. Start with a strong hook

The opening should create curiosity quickly and give the viewer a reason to continue watching.

2. Focus on one idea

Short videos have limited time, so the body should communicate one clear idea instead of covering too many topics.

3. Sound conversational

The script should feel natural when spoken rather than reading like a formal article.

4. Avoid unnecessary details

Every sentence should contribute to the main idea.

5. End with a relevant CTA

The call-to-action should naturally connect to the content instead of feeling forced.

6. Match the target duration

The script should contain an appropriate number of words for the requested runtime.

How the Generator Gets There

The generator uses a combination of prompt engineering and programmatic validation.

The prompt gives Gemini specific instructions for:

Hook creation
Body structure
CTA generation
Natural language
Unsupported-detail avoidance
Target word count
JSON formatting

After Gemini generates the script, Python validates the response.

This approach is intentional because an LLM may produce structurally valid content that still does not meet the application's requirements.

Therefore, the application does not blindly accept the first response.

Instead:

Generate
   ↓
Parse
   ↓
Validate
   ↓
Measure
   ↓
Accept OR Regenerate
Design Decisions
Why Gemini?

Gemini 2.5 Flash provides fast generation suitable for short-form content while supporting structured prompt-based generation.

Why JSON?

Returning JSON makes the output predictable and allows the application to validate individual fields programmatically.

Why programmatic validation?

LLM output is probabilistic. Programmatic validation ensures that important application requirements such as required fields and target length are enforced consistently.

Why 2.5 words per second?

The project uses approximately 2.5 spoken words per second as a simple baseline for estimating short-form video duration. Actual speaking speed can vary depending on the creator and delivery style.

Security

API credentials are stored in environment variables rather than source code.

The repository excludes:

.env
.venv/
__pycache__/
*.pyc

Never commit API keys or other credentials to GitHub.

Future Improvements

Potential improvements include:

Add tone/style controls
Support different speaking speeds
Add platform-specific formats for YouTube Shorts, Instagram Reels, and TikTok
Add configurable word-per-second settings
Add a web interface
Add automated script quality scoring
Add additional output formats such as Markdown or plain text
Add tests for validation and generation logic
Author

Pratik Punj
    |
    v
Calculate Estimated Runtime
    |
    v
Return Final Script
