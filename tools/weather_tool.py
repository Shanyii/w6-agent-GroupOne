import requests

TOOL = {
    "name": "get_weather",
    "description": "取得指定城市的即時天氣，並根據天氣狀況判斷適合室內還是室外活動",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名稱，例如：Taipei, Tokyo, New York"
            }
        },
        "required": ["city"]
    }
}

def run(city: str) -> str:
    """呼叫 wttr.in API 取得天氣，並提供活動建議"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 取得目前天氣狀態
        current_condition = data.get("current_condition", [{}])[0]
        weather_desc = current_condition.get("weatherDesc", [{}])[0].get("value", "Unknown")
        temp_c = current_condition.get("temp_C", "Unknown")
        
        # 根據天氣描述判斷適合室內還室外
        weather_desc_lower = weather_desc.lower()
        
        # 定義容易引發不便的室內天氣關鍵字 (可依需求擴增)
        indoor_keywords = ["rain", "storm", "snow", "shower", "thunder", "drizzle", "mist", "fog", "heavy"]
        
        if any(keyword in weather_desc_lower for keyword in indoor_keywords):
            activity_suggestion = "建議進行【室內活動】🏠 (例如：看展覽、室內購物、咖啡廳休息)"
        else:
            activity_suggestion = "建議可以安排【室外活動】🏕️ (例如：踏青、運動、戶外景點)"
            
        result = (
            f"📍 城市: {city}\n"
            f"🌤️ 目前天氣: {weather_desc}\n"
            f"🌡️ 氣溫: {temp_c}°C\n"
            f"💡 活動建議: {activity_suggestion}"
        )
        return result
        
    except requests.exceptions.RequestException as e:
        return f"無法取得 {city} 的天氣資訊，連線錯誤: {str(e)}"
    except Exception as e:
        return f"解析 {city} 天氣資料時發生錯誤: {str(e)}"

# 簡單測試用
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(run("Taipei"))
    print("-" * 30)
    print(run("London"))
