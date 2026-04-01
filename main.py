import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# 載入我們的自訂工具
from tools import weather_tool
from tools import activity_tool

# 1. 載入環境變數與安全檢查
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    print("❌ 錯誤：找不到有效的 GEMINI_API_KEY！")
    print("請複製 .env.example 為 .env 並填入您的 API Key。")
    sys.exit(1)

# 2. 初始化 Gemini API
genai.configure(api_key=API_KEY)

# 3. 定義 Agent 的 System Prompt (SOP)
SYSTEM_INSTRUCTION = """
你是一個全方位的生活顧問與行動助手 AI Agent。
你的主要目標是協助使用者解決生活大小事，包含查詢天氣並給予具體的行動建議。

[標準作業流程 SOP]
1. 觀察使用者的請求，判斷是否需要外部資訊。
2. 若使用者詢問跟天氣、活動安排有關的問題，必須優先呼叫 `get_weather` 工具取得準確的氣象與建議資料。
3. 若使用者想要隨機活動建議、不知道做什麼好、想找事做，請呼叫 `get_random_activity` 工具取得建議。
4. 取得工具回傳的結果後，整合資訊並用親切、專業的口吻回覆使用者。
5. 若使用者詢問不屬於工具範圍內的問題，則直接給予最佳的文字回答。

要求：
- 時刻保持禮貌。
- 嚴格遵守 SOP，並確保在需要時精準捕捉城市名稱呼叫 API。
"""

# 4. 封裝 Tool 給 Gemini 使用
# 因為 SDK 預設會讀取函式的名字作為 tool 名稱，所以這裡包裝成 get_weather
def get_random_activity() -> str:
    """取得一則隨機活動建議，回傳活動名稱與類型"""
    return activity_tool.run()

def get_weather(city: str) -> str:
    """取得指定城市的即時天氣，並根據天氣狀況判斷適合室內還是室外活動 (例如輸入 Taipei)"""
    return weather_tool.run(city)

def main():
    print("=" * 60)
    print("🚀 AI 生活顧問 Agent 啟動中...")
    print("=" * 60)
    print("📜 [System Prompt 展示]")
    print(SYSTEM_INSTRUCTION.strip())
    print("=" * 60)
    
    # 準備模型與 Tools
    tools_list = [get_weather, get_random_activity]
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=tools_list,
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # 啟動對話。為了展示高透明度機制，我們手動處理 function calling 而不使用自動模式
    chat = model.start_chat()

    print("\n💡 提示：請輸入對話來測試 Agent (輸入 'q' 離開)。")
    print("您可以試著說：「週末想去東京玩，天氣如何？該安排室內還是室外活動？」\n")
    
    while True:
        try:
            user_input = input("👤 使用者: ")
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 系統關閉，再見！")
            break
            
        if not user_input.strip():
            continue
            
        print("\n🔍 [Agent 思考中...]")
        
        try:
            # 送出輸入
            response = chat.send_message(user_input)
            
            # 高透明度控制機制：處理所有回傳的 Function Calling 請求
            while response.function_calls:
                for fn_call in response.function_calls:
                    fn_name = fn_call.name
                    # 解析參數
                    fn_args = {key: val for key, val in fn_call.args.items()}
                    
                    # 顯示透明度 Log
                    print(f"   ⚙️  [觸發 Tool] 名稱: {fn_name}")
                    print(f"   📥  [參數]: {fn_args}")
                    
                    # 實際執行外部工具
                    if fn_name == "get_weather":
                        tool_result = get_weather(**fn_args)
                    elif fn_name == "get_random_activity":
                        tool_result = get_random_activity()
                    else:
                        tool_result = f"Error: 找不到對應的工具 {fn_name}"
                        
                    print(f"   📤  [執行結果]:\n       {tool_result}\n")
                    
                    # 將工具執行的結果送回給模型繼續推理
                    response = chat.send_message(
                        genai.types.Part.from_function_response(
                            name=fn_name,
                            response={"result": tool_result}
                        )
                    )
            
            # 當沒有 function call 需求時，印出最終回覆
            print(f"🤖 Agent: {response.text}\n")
            
        except Exception as e:
            print(f"⚠️ 發生錯誤: {e}\n")

if __name__ == "__main__":
    main()
