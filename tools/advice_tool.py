import requests

TOOL = {
    "name": "get_daily_advice",
    "description": "取得一則今日人生建議，回傳一句隨機建議",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

def run() -> str:
    """呼叫 Advice Slip API 取得一則隨機人生建議"""
    try:
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        advice = data.get("slip", {}).get("advice", "Unknown")

        result = f"💡 今日建議: {advice}"
        return result

    except requests.exceptions.RequestException as e:
        return f"無法取得人生建議，連線錯誤: {str(e)}"
    except Exception as e:
        return f"解析建議資料時發生錯誤: {str(e)}"

# 簡單測試用
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(run())
