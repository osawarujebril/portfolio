import os
import sys
import json
import time
import requests

def run():
    if len(sys.argv) < 4:
        print("Usage: python generate_kie_video.py <image_url> <prompt> <output_file> [model]")
        print("  image_url: Public URL of the source image")
        print("  prompt: Motion description")
        print("  output_file: Where to save the video")
        print("  model: kling-2.6/image-to-video (default), sora-2-image-to-video")
        sys.exit(1)

    image_url = sys.argv[1]
    prompt = sys.argv[2]
    output_file = sys.argv[3]
    model = sys.argv[4] if len(sys.argv) > 4 else "kling-2.6/image-to-video"

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

    # Build payload based on model
    if model.startswith("veo3"):
        payload = {
            "model": model,
            "input": {
                "prompt": prompt,
                "imageUrls": [image_url],
                "aspect_ratio": "16:9"
            }
        }
    else:
        # Kling format
        payload = {
            "model": model,
            "input": {
                "prompt": prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": "5"
            }
        }

    print(f"Creating video task via Kie.ai ({model})...")
    print(f"  Image: {image_url}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"API Response: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"ERROR creating task: {e}")
        if 'response' in locals() and response is not None:
            print(response.text[:500])
        sys.exit(1)

    if result is None:
        print("ERROR: API returned None")
        sys.exit(1)

    task_id = result.get("data", {}).get("taskId") if isinstance(result.get("data"), dict) else result.get("taskId")
    if not task_id:
        print("ERROR: No taskId returned")
        print(json.dumps(result, indent=2))
        sys.exit(1)

    print(f"Task created. ID: {task_id}. Polling (videos take 1-5 min)...")

    poll_url = "https://api.kie.ai/api/v1/jobs/recordInfo"
    poll_params = {"taskId": task_id}

    attempts = 0
    while attempts < 150:
        time.sleep(5)
        attempts += 1

        try:
            poll_resp = requests.get(poll_url, headers=headers, params=poll_params, timeout=15)
            poll_resp.raise_for_status()
            poll_result = poll_resp.json()
        except Exception as e:
            if attempts % 10 == 0:
                print(f"Poll {attempts} Error: {e}")
            continue

        data = poll_result.get("data", {})
        if not data:
            continue

        state = data.get("state")
        if attempts % 10 == 0 or state in ("success", "completed", "failed", "error"):
            print(f"Poll {attempts}: state = {state}")

        if state == "success" or state == "completed":
            result_json_str = data.get("resultJson", "{}")
            try:
                result_json = json.loads(result_json_str)
            except json.JSONDecodeError:
                result_json = {}

            result_urls = result_json.get("resultUrls", [])
            if result_urls and len(result_urls) > 0:
                video_url = result_urls[0]
                print(f"Downloading video from {video_url}")
                try:
                    vid_resp = requests.get(video_url, timeout=120)
                    vid_resp.raise_for_status()
                    with open(output_file, 'wb') as f:
                        f.write(vid_resp.content)
                    print(f"Successfully saved to {output_file}")
                    sys.exit(0)
                except Exception as e:
                    print(f"ERROR downloading video: {e}")
                    sys.exit(1)
            else:
                print("ERROR: No video URL in resultJson.")
                print(json.dumps(data, indent=2))
                sys.exit(1)

        elif state in ("failed", "error", "fail"):
            print("ERROR: Task failed.")
            print(json.dumps(data, indent=2))
            sys.exit(1)

    print("ERROR: Timed out (12.5 min)")
    sys.exit(1)

if __name__ == "__main__":
    run()
