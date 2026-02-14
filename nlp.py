import requests
import os
from ocr import extract_text_from_image   # import Step 1 OCR function

def summarize_and_translate(text, filename="card_summary6.txt"):
    # 🔑 Add your OpenRouter API key here
    api_key = "API KEY "

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

        # 📂 Ensure output/summaries exists
        save_dir = os.path.join("output", "summaries")
        os.makedirs(save_dir, exist_ok=True)

        # Save translation + summary into a file
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"✅ Translation & Summary saved at {save_path}")
        return output
    else:
        print("❌ Error in Step 2:", response.status_code, response.text)
        return None


# 🔹 Run directly (connects with Step 1 OCR)
if __name__ == "__main__":
    # Step 1: Extract Sanskrit text from image
    image_path = "images/s-1.jpg"   # 👈 Change this to your input image
    extracted_text = extract_text_from_image(image_path)

    if extracted_text:
        print("📜 Extracted Sanskrit Text:", extracted_text)
        # Step 2: Translate & summarize, save result
        summarize_and_translate(extracted_text, "card_summary6.txt")
    else:
        print("⚠️ No text extracted from image.")
