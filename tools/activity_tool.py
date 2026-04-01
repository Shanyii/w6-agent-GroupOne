import requests

TOOL = {
    "name": "get_random_activity",
    "description": "取得一則隨機活動建議，回傳活動名稱與類型",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

def run() -> str:
    """呼叫 Bored API 取得一則隨機活動建議"""
    try:
        url = "https://bored-api.appbrewery.com/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        activity = data.get("activity", "Unknown")
        activity_type = data.get("type", "Unknown")

        result = (
            f"🎯 活動名稱: {activity}\n"
            f"📂 活動類型: {activity_type}"
        )
        return result

    except requests.exceptions.RequestException as e:
        return f"無法取得活動建議，連線錯誤: {str(e)}"
    except Exception as e:
        return f"解析活動資料時發生錯誤: {str(e)}"

# 簡單測試用
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(run())
