import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from main import SYSTEM_INSTRUCTION, get_weather, get_daily_advice

app = Flask(__name__, static_folder='.', static_url_path='')

tools_list = [get_weather, get_daily_advice]

# 建立全域的 Chat Session (簡單示範用途)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=tools_list,
    system_instruction=SYSTEM_INSTRUCTION
)
chat = model.start_chat()

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = chat.send_message(user_input)
        
        # 輔助函式：提取所有 function calls
        def extract_func_calls(resp):
            calls = []
            parts = getattr(resp, "parts", None)
            if not parts and getattr(resp, "candidates", None) and resp.candidates:
                parts = resp.candidates[0].content.parts
            if parts:
                for p in parts:
                    if getattr(p, "function_call", None):
                        calls.append(p.function_call)
            return calls
            
        active_calls = extract_func_calls(response)
        tool_logs = []
        
        while active_calls:
            tool_responses = []
            
            for fn_call in active_calls:
                fn_name = fn_call.name
                fn_args = {}
                if hasattr(fn_call.args, "items"):
                    fn_args = {key: val for key, val in fn_call.args.items()}
                else:
                    fn_args = {key: getattr(fn_call.args, key) for key in fn_call.args}
                
                # 紀錄被執行的 Tool，傳給前端顯示動畫
                args_str = ", ".join(f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in fn_args.items())
                tool_logs.append(f"{fn_name}({args_str})")
                
                # 實際執行工具
                if fn_name == "get_weather":
                    tool_result = get_weather(**fn_args)
                elif fn_name == "get_daily_advice":
                    tool_result = get_daily_advice()
                else:
                    tool_result = f"Error: 找不到對應的工具 {fn_name}"
                    
                tool_responses.append(
                    {
                        "function_response": {
                            "name": fn_name,
                            "response": {"result": tool_result}
                        }
                    }
                )
            
            # 再將工具結果送回給模型
            response = chat.send_message(tool_responses)
            active_calls = extract_func_calls(response)
            
        # 回傳最終結果給前端
        import markdown
        html_response = markdown.markdown(response.text)
        
        return jsonify({
            "tools_called": tool_logs,
            "response": html_response # 將 Markdown 直接轉成 HTML
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
