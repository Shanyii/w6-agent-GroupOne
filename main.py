import os
import sys
import glob
from dotenv import load_dotenv
import google.generativeai as genai

# 載入我們的自訂工具
from tools import weather_tool
from tools import advice_tool

# 1. 載入環境變數與安全檢查
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    print("❌ 錯誤：找不到有效的 GEMINI_API_KEY！")
    print("請複製 .env.example 為 .env 並填入您的 API Key。")
    sys.exit(1)

# 2. 初始化 Gemini API
genai.configure(api_key=API_KEY)

# --- 新增技能 (Skill) 讀取機制 ---
def load_skills():
    """從 skills 工作目錄讀取所有 markdown 或 txt 檔案作為擴充技能 SOP"""
    skills_text = ""
    skills_dir = "skills"
    if os.path.exists(skills_dir):
        skill_files = glob.glob(os.path.join(skills_dir, "*.txt")) + glob.glob(os.path.join(skills_dir, "*.md"))
        for filepath in skill_files:
            with open(filepath, "r", encoding="utf-8") as f:
                filename = os.path.basename(filepath)
                skills_text += f"\n--- [Skill: {filename}] ---\n"
                skills_text += f.read().strip() + "\n"
    return skills_text

# 3. 定義 Agent 的 System Prompt (SOP)
base_instruction = """
你是一個全方位的生活顧問與行動助手 AI Agent。
你的主要目標是協助使用者解決生活大小事，包含查詢天氣並給予具體的行動建議。

[標準作業流程 SOP (基礎)]
1. 觀察使用者的請求，判斷是否需要外部資訊。
2. 若使用者詢問跟天氣、活動安排有關的問題，必須優先呼叫 `get_weather` 工具取得準確的氣象與建議資料。
3. 若使用者需要人生建議、遇到迷惘，或是尋求日常建議時，請呼叫 `get_daily_advice` 工具取得一則金句或建議。
4. 取得工具回傳的結果後，整合資訊並用親切、專業的口吻回覆使用者。
5. 若使用者詢問不屬於工具範圍內的問題，則直接給予最佳的文字回答。

要求：
- 時刻保持禮貌。
- 嚴格遵守基礎 SOP 與任何擴充的 Skill SOP，並確保在需要時精準捕捉城市名稱呼叫 API。
"""

# 將讀取到的 skills 加入 system instruction
skills_addons = load_skills()
SYSTEM_INSTRUCTION = base_instruction
if skills_addons:
    SYSTEM_INSTRUCTION += "\n\n[已加載的進階技能 Skills]\n以下是你具備的進階任務處理流程，請在使用者需求符合時，依照以下流程組合運用 Tool 來完成任務：\n" + skills_addons


# 4. 封裝 Tool 給 Gemini 使用
# 因為 SDK 預設會讀取函式的名字作為 tool 名稱，所以這裡包裝成 get_weather
def get_daily_advice() -> str:
    """取得一則隨機人生建議，回傳一句建議"""
    return advice_tool.run()

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
    tools_list = [get_weather, get_daily_advice]
    
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
            
        # ---------- 完整 Prompt 展示 (高透明度機制) ----------
        print("\n" + "="*60)
        print("📝 [即將發送的完整對話 Prompt]")
        print("【System Instruction (系統提示 / SOP 與 Skills)】")
        print(SYSTEM_INSTRUCTION.strip())
        print("-" * 60)
        print("【Chat History (對話歷史)】")
        if getattr(chat, 'history', None) is None or not chat.history:
            print("  (尚無對話記錄)")
        else:
            for msg in chat.history:
                role = "Agent" if msg.role == "model" else "User"
                print(f"[{role}]:")
                for part in msg.parts:
                    if part.text: 
                        print(f"  {part.text}")
                    elif part.function_call: 
                        args_str = ", ".join(f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in part.function_call.args.items())
                        print(f"  [呼叫 Tool] 🛠️ {part.function_call.name}({args_str})")
                    elif part.function_response: 
                        try:
                            # 嘗試取得 dict 內的 result
                            val = part.function_response.response.get('result', part.function_response.response)
                        except Exception:
                            val = part.function_response.response
                        print(f"  [Tool 回傳] 📥 {part.function_response.name}: {val}")
        print("-" * 60)
        print(f"【New Message (本次使用者輸入)】\n{user_input}")
        print("=" * 60 + "\n")
        # ----------------------------------------------------
            
        print("🔍 [Agent 思考中...]")
        
        try:
            # 送出輸入
            response = chat.send_message(user_input)
            
            # 安全取得 Function Calls 的輔助函式
            def extract_func_calls(resp):
                calls = []
                # 某些版本支援 resp.parts
                parts = getattr(resp, "parts", None)
                if not parts and getattr(resp, "candidates", None) and resp.candidates:
                    parts = resp.candidates[0].content.parts
                
                if parts:
                    for p in parts:
                        if getattr(p, "function_call", None):
                            calls.append(p.function_call)
                return calls
                
            # 高透明度控制機制：處理所有回傳的 Function Calling 請求
            active_calls = extract_func_calls(response)
            
            while active_calls:
                tool_responses = [] # 收集這次觸發的所有工具結果
                
                for fn_call in active_calls:
                    fn_name = fn_call.name
                    # 解析參數 (支援 proto 或 dict 型式)
                    fn_args = {}
                    if hasattr(fn_call.args, "items"):
                        fn_args = {key: val for key, val in fn_call.args.items()}
                    else:
                        fn_args = {key: getattr(fn_call.args, key) for key in fn_call.args}
                    
                    # 顯示透明度 Log
                    print(f"   ⚙️  [觸發 Tool] 名稱: {fn_name}")
                    print(f"   📥  [參數]: {fn_args}")
                    
                    # 實際執行外部工具
                    if fn_name == "get_weather":
                        tool_result = get_weather(**fn_args)
                    elif fn_name == "get_daily_advice":
                        tool_result = get_daily_advice()
                    else:
                        tool_result = f"Error: 找不到對應的工具 {fn_name}"
                        
                    print(f"   📤  [執行結果]:\n       {tool_result}\n")
                    
                    # 將結果存入清單
                    tool_responses.append(
                        {
                            "function_response": {
                                "name": fn_name,
                                "response": {"result": tool_result}
                            }
                        }
                    )
                
                # 將「所有」工具執行的結果一次送回給模型繼續推理
                response = chat.send_message(tool_responses)
                active_calls = extract_func_calls(response)
            
            # 當沒有 function call 需求時，印出最終回覆
            print(f"🤖 Agent: {response.text}\n")
            
        except Exception as e:
            print(f"⚠️ 發生錯誤: {e}\n")

if __name__ == "__main__":
    main()
