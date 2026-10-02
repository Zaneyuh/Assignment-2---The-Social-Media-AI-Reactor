import ollama
import json
import os


MODEL = "gemma4:e2b"


def analyze_post(caption, comments, metadata, image_path=None):
    """
    Analyze a LinkedIn post using the five assignment layers.
    """

    prompt = f"""
You are a Social Media AI Reactor analyzing a LinkedIn post.

Analyze the post using EXACTLY these five layers:

1. CONTENT AND SEMANTIC UNDERSTANDING
- Identify the main topic.
- Summarize the caption.
- Analyze the comments.
- If an image is provided, describe important visible content and overlay text.
- Explain the overall meaning of the post.

2. SENTIMENT AND EMOTION IDENTIFICATION
- Determine whether the overall sentiment is Positive, Negative, Neutral,
  or Mixed.
- Identify important emotions.
- Give a short explanation based on the actual text.

3. ENTITY AND INTENT RECOGNITION
Identify:
- People
- Organizations
- Locations
- Products
- Brands
- Events
- Technologies
- Other important entities

Also identify the likely intent of the post, such as:
- Inform
- Promote
- Share an experience
- Ask a question
- Recruit
- Educate
- Celebrate
- Debate
- Other

4. CONTENT AND METADATA INTEGRATION
Use the provided metadata:
- Hashtags
- Timestamp
- Location/geotag
- Follower reach
- Likes
- Shares
- Comment count

Explain how the metadata affects the interpretation and potential engagement
of the post.

Do NOT invent metadata that was not provided.

5. RISK, MODERATION AND SAFETY FILTERING
Check for:
- Hate speech
- Misinformation
- Spam
- Self-harm risks
- Copyright concerns
- Harassment
- Other platform policy concerns

For each category, say:
SAFE or FLAGGED

If something is FLAGGED, explain why.
Do not make accusations without evidence.

POST CAPTION:
{caption}

COMMENTS:
{comments}

METADATA:
{json.dumps(metadata, indent=2)}

Return the result in this JSON format:

{{
    "content_semantic_understanding": {{
        "main_topic": "",
        "summary": "",
        "comment_analysis": "",
        "image_analysis": "",
        "overall_meaning": ""
    }},
    "sentiment_emotion": {{
        "sentiment": "",
        "emotions": [],
        "explanation": ""
    }},
    "entities_intent": {{
        "people": [],
        "organizations": [],
        "locations": [],
        "products": [],
        "brands": [],
        "events": [],
        "technologies": [],
        "intent": "",
        "explanation": ""
    }},
    "metadata_integration": {{
        "hashtags": [],
        "timestamp": "",
        "location": "",
        "followers": "",
        "likes": "",
        "shares": "",
        "comments": "",
        "engagement_interpretation": ""
    }},
    "risk_moderation": {{
        "hate_speech": "SAFE",
        "misinformation": "SAFE",
        "spam": "SAFE",
        "self_harm": "SAFE",
        "copyright": "SAFE",
        "harassment": "SAFE",
        "other_policy_risk": "SAFE",
        "overall_safety": "",
        "explanation": ""
    }}
}}
"""

    message = {
        "role": "user",
        "content": prompt
    }

    # Add image if available
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        message["images"] = [image_data]

    response = ollama.chat(
        model=MODEL,
        messages=[message],
        options={
            "temperature": 0.3
        }
    )

    return response["message"]["content"]


def generate_reactions(post_analysis, caption):
    """
    Generate six different reaction comments.
    """

    prompt = f"""
You are generating LinkedIn reaction comments based on an AI analysis
of a real LinkedIn post.

POST:
{caption}

AI ANALYSIS:
{post_analysis}

Generate exactly six comments.

The six categories are:

1. VALUE-ADD
Goal:
Demonstrate expertise and add useful information or data.

2. EXPERIENCE SHARE
Goal:
Build trust by sharing a relevant personal or professional experience.

3. RESPECTFUL CHALLENGE
Goal:
Present a respectful counterpoint and encourage thoughtful debate.

4. DISCUSSION STARTER
Goal:
Ask a meaningful question that encourages the author to elaborate.

5. SUPPORTIVE / SOCIAL
Goal:
Show genuine support and maintain a professional social connection.

6. THE DISRUPTOR (TROLL)
Goal:
Create a provocative or controversial reaction.

IMPORTANT:
The comments should sound human rather than like generic AI output.

Human-like comments should:
- Avoid excessive corporate language.
- Avoid unnecessary buzzwords.
- Use natural sentence lengths.
- Reference something specific from the post.
- Avoid starting every comment with "Great post!"
- Avoid repeating the same structure.
- Sound like something an actual LinkedIn user might write.
- Keep the comments relatively short.
- Do not fabricate personal experiences or facts.
- For the Disruptor/Troll example, make it clearly provocative for the
  classroom demonstration, but do not use hate speech, threats, or
  targeted harassment.

Return exactly this JSON:

{{
    "value_add": "",
    "experience_share": "",
    "respectful_challenge": "",
    "discussion_starter": "",
    "supportive_social": "",
    "disruptor_troll": ""
}}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.8
        }
    )

    return response["message"]["content"]


def main():

    # ------------------------------------------------
    # REPLACE THESE WITH YOUR ACTUAL LINKEDIN POST
    # ------------------------------------------------

    caption = """
    Paste the LinkedIn post caption here.
    """

    comments = """
    Comment 1: Paste comment here.

    Comment 2: Paste another comment here.

    Comment 3: Paste another comment here.
    """

    metadata = {
        "hashtags": [
            "#AI",
            "#Technology"
        ],
        "timestamp": "October 2026",
        "location": "Not provided",
        "followers": "Not provided",
        "likes": 125,
        "shares": 14,
        "comments": 32
    }

    # Use None if there is no image.
    image_path = "post_image.jpg"

    print("\n========================================")
    print("SOCIAL MEDIA AI REACTOR")
    print("========================================\n")

    print("Analyzing LinkedIn post...\n")

    analysis = analyze_post(
        caption,
        comments,
        metadata,
        image_path
    )

    print("========== POST ANALYSIS ==========\n")
    print(analysis)

    print("\nGenerating six reaction comments...\n")

    reactions = generate_reactions(
        analysis,
        caption
    )

    print("========== REACTION COMMENTS ==========\n")
    print(reactions)

    # Save results
    with open("analysis_result.txt", "w", encoding="utf-8") as file:
        file.write("SOCIAL MEDIA AI REACTOR\n\n")
        file.write("POST ANALYSIS\n")
        file.write("========================\n")
        file.write(analysis)
        file.write("\n\nREACTION COMMENTS\n")
        file.write("========================\n")
        file.write(reactions)

    print("\nResults saved to analysis_result.txt")


if __name__ == "__main__":
    main()