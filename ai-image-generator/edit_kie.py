"""
Edit an existing image using Kie.ai nano-banana-edit model.
Usage: python3 scripts/edit_kie.py <image_url> <edit_prompt> <output_file> [aspect_ratio]
"""
import os, sys, json, time, requests

def run():
    if len(sys.argv) < 4:
        print("Usage: python3 scripts/edit_kie.py <image_url> <edit_prompt> <output_file> [aspect_ratio]")
        sys.exit(1)

    image_url = sys.argv[1]
    edit_prompt = sys.argv[2]
    output_file = sys.argv[3]
    aspect_ratio = sys.argv[4] if len(sys.argv) > 4 else "4:5"

    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    api_key = None
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('KIE_API_KEY='):
                api_key = line.strip().split('=', 1)[1].strip('"\'')
                break

    if not api_key:
        print("ERROR: KIE_API_KEY not found in .env")
        sys.exit(1)

    url = "https://api.kie.ai/api/v1/jobs/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "google/nano-banana-edit",
        "input": {
            "prompt": edit_prompt,
            "image_urls": [image_url],
            "output_format": "png",
            "image_size": aspect_ratio
        }
    }

    print(f"Creating edit task via Kie.ai API...")
    print(f"Edit prompt: {edit_prompt[:100]}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"ERROR creating task: {e}")
        if 'response' in locals() and response is not None:
            print(response.text)
        sys.exit(1)

    task_id = result.get("data", {}).get("taskId")
    if not task_id:
        print("ERROR: No taskId returned")
        print(result)
        sys.exit(1)

    print(f"Task created. Task ID: {task_id}. Polling...")

    poll_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
    poll_params = {"taskId": task_id}

    attempts = 0
    while attempts < 60:
        time.sleep(4)
        attempts += 1
        try:
            poll_resp = requests.get(poll_url, headers=headers, params=poll_params, timeout=15)
            poll_resp.raise_for_status()
            poll_result = poll_resp.json()
        except Exception as e:
            print(f"Poll {attempts} Error: {e}")
            continue

        data = poll_result.get("data", {})
        if not data:
            print(f"Poll {attempts}: Empty data. Retrying...")
            continue

        state = data.get("state")
        print(f"Poll {attempts}: state = {state}")

        if state in ("success", "completed"):
            result_json_str = data.get("resultJson", "{}")
            try:
                result_json = json.loads(result_json_str)
            except json.JSONDecodeError:
                result_json = {}

            result_urls = result_json.get("resultUrls", [])
            if result_urls:
                img_url = result_urls[0]
                print(f"Downloading from {img_url}")
                try:
                    img_resp = requests.get(img_url, timeout=30)
                    img_resp.raise_for_status()
                    with open(output_file, 'wb') as f:
                        f.write(img_resp.content)
                    print(f"Saved to {output_file}")
                    sys.exit(0)
                except Exception as e:
                    print(f"ERROR downloading: {e}")
                    sys.exit(1)
            else:
                print("ERROR: No result URLs found")
                print(json.dumps(data, indent=2))
                sys.exit(1)

        elif state in ("failed", "error", "fail"):
            print("ERROR: Task failed.")
            print(json.dumps(data, indent=2))
            sys.exit(1)

    print("ERROR: Timed out")
    sys.exit(1)

if __name__ == "__main__":
    run()
