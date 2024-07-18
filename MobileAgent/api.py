import base64
import requests

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def inference_chat(chat, API_TOKEN):    
    api_url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    data = {
        "model": 'gpt-4-turbo',
        "messages": [],
        "max_tokens": 2048,
    }

    for role, content in chat:
        data["messages"].append({"role": role, "content": content})

    while 1:
        try:
            res = requests.post(api_url, headers=headers, json=data)
            res = res.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"API access exception: {e}")
            try:
                result_json = res.json()
                print(result_json)
                error_code = result_json['error']['code']

                if error_code == 'invalid_image_format':
                    raise Exception("Invalid image format.")
                elif error_code == 'rate_limit_exceeded':
                    raise Exception("Rate limit exceeded. Retry later.")
                elif error_code == 'insufficient_quota':
                    raise Exception("Insufficient quota. Add credits and retry.")
                else:
                    raise Exception(f"Error code: {error_code}.")
            except:
                raise Exception(f"Unknown API error {e}.")
        else:
            break
    
    return res
