import requests
import os
from ocr import extract_text_from_image   # Step 1 OCR

# -------------------------------
# STEP 2: Translate & Summarize
# -------------------------------
def summarize_and_translate(text, api_key, filename="card_summary6.txt"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a translator and summarizer. Translate Sanskrit into simple English and summarize it."
            },
            {
                "role": "user",
                "content": f"Text: {text}\n\nTranslate this into English and give a short summary."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        output = result["choices"][0]["message"]["content"]

        # save locally (optional)
        save_dir = os.path.join("output", "summaries")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"✅ Translation & Summary saved at {save_path}")
        return output
    else:
        print("❌ Error in Step 2:", response.status_code, response.text)
        return None


# -------------------------------
# STEP 2.5: Epic Classification
# -------------------------------
def classify_epic(summary_text, hf_token):
    API_URL = "ADD API URL TOKEN "
    headers = {"Authorization": f"Bearer {hf_token}"}

    candidate_labels = ["Mahabharata", "Ramayana", "Bhagavad Gita", "Other Vedic"]

    response = requests.post(API_URL, headers=headers, json={
        "inputs": summary_text,
        "parameters": {"candidate_labels": candidate_labels}
    })

    result = response.json()
    if "labels" in result:
        return result["labels"][0]
    return "Other Vedic"


# -------------------------------
# MAIN PIPELINE (Step 2 → Step 2.5)
# -------------------------------
if __name__ == "__main__":
    # Keys
    OPENROUTER_KEY = "oPEN ROUTER TOKEN"
    HF_TOKEN = "hF TOKEN"

    # Step 1: OCR
    image_path = "images/s-1.jpg"
    extracted_text = extract_text_from_image(image_path)

    if extracted_text:
        print("📜 Extracted Sanskrit Text:", extracted_text)

        # Step 2: Translate & Summarize
        summary = summarize_and_translate(extracted_text, OPENROUTER_KEY, "card_summary6.txt")

        if summary:
            # Step 2.5: Classify Epic
            epic_label = classify_epic(summary, HF_TOKEN)
            print("🔮 Identified Epic:", epic_label)
    else:
        print("⚠️ No text extracted from image.")
