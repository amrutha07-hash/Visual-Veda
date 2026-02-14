import requests
import os

HF_TOKEN = "HF TOKEN"

def generate_image_hf(story_prompt, output_path="output/story_card/story_card5.png"):
    url = "URL "
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": story_prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("🔍 Response status:", response.status_code)

    if response.status_code != 200:
        print("❌ Error generating image:", response.text)
        return None

    # Hugging Face may return raw image bytes
    content_type = response.headers.get("content-type", "")
    if "image" in content_type:
        # Save raw bytes directly
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved at {output_path}")
        return output_path
    else:
        print("❌ Unexpected response type:", content_type)
        print("Response snippet:", response.text[:500])
        return None

if __name__ == "__main__":
    story_prompt = "Arjuna stands in the battlefield guided by Krishna, epic, cinematic, dramatic lighting"
    generate_image_hf(story_prompt, "output/story_card/story_card5.png")
