import os

TOOL = {
    "name": "review_code",
    "description": "讀取指定程式碼資料夾(預設為 code/)中的所有檔案內容，用於進行程式碼審查",
    "parameters": {
        "type": "object",
        "properties": {
            "folder_path": {
                "type": "string",
                "description": "要檢查的程式碼資料夾路徑，預設請輸入 'code'"
            }
        },
        "required": ["folder_path"]
    }
}

def run(folder_path: str = "code") -> str:
    """讀取資料夾中所有 .py 檔的內容並回傳"""
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return f"錯誤：找不到資料夾 {folder_path}"

    files_content = []
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".py"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    files_content.append(f"====== File: {filename} ======\n{content}\n")
        
        if not files_content:
            return f"找不到任何 .py 檔案於目錄: {folder_path}"
            
        result = "以下是該資料夾中的程式碼內容：\n\n" + "\n".join(files_content)
        return result
        
    except Exception as e:
        return f"讀取程式碼資料夾時發生錯誤: {str(e)}"

if __name__ == "__main__":
    print(run("../code"))
