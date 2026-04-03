# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題：生活顧問

---

## Agent 功能總覽

> 說明這個 Agent 能做什麼，使用者可以輸入哪些指令

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| 天氣 | 呼叫 weather_tool，查詢即時天氣        |  楊姍頤 |
| 活動 | 呼叫 activity_tool，隨機活動建議       |  林瑞城 |
| 建議 | 呼叫 advice_tool，取得隨機建議         |  林瑞城 |

---

## 組員與分工

| 姓名 | 負責功能     | 檔案        | 使用的 API |
| ---- | ------------ | ----------- | ---------- |
| 楊姍頤 |  查詢當地天氣，判斷適合室內還是室外，根據天氣描述決定活動類型  | `tools/`  |  https://wttr.in/{city}?format=j1           |
| 林瑞城 |  取得一則隨機活動建議  | `tools/`  |  https://bored-api.appbrewery.com/random    |
| 林瑞城 |  取得一則今日人生建議  | `tools/`  |  https://api.adviceslip.com/advice          |
| 楊姍頤 & 林瑞城 | Skill 整合   | `skills/` | — |
| 楊姍頤 & 林瑞城 | Agent 主程式 | `main.py` | — |
| 楊姍頤 | 前端網頁 | `index.html` `style.css` `script.js` | — |

---

## 專案架構

```
── tools/
│   ├── activity_tool.py
│   ├── advice_tool.py
│   └── weather_tool.py
├── skills/
│   └── compare_weather.md
├── .env
├── .gitignore
├── app.py
├── index.html
├── main.py
├── requirements.txt
├── script.js
├── style.css
└── README.md
```

---

## 使用方式

範例：

1. **建立環境變數檔案**
   在專案根目錄下建立一個 `.env` 檔案，並填入您的 Gemini API 金鑰：
   ```env
   GEMINI_API_KEY=您的_API_KEY_放在這裡
   ```

2. **安裝所需套件**
   在終端機中執行以下指令來安裝所有依賴套件：
   ```bash
   pip install -r requirements.txt
   ```
   *(Windows 用戶若遇到錯誤，可改用 `py -m pip install -r requirements.txt`)*

3. **啟動 Web 應用程式**
   由於我們已經將代理人整合為網頁版本，請執行 `app.py` 來啟動伺服器：
   ```bash
   python app.py
   ```
   *(Windows 用戶若無法執行，請改用 `py app.py`)*

4. **開始使用**
   當伺服器啟動完成後，在終端機看到 `* Running on http://127.0.0.1:5000` 提示時，請打開您的瀏覽器前往：
   👉 `http://localhost:5000`
   即可開始在美觀的網頁介面上與 AI 生活顧問對話！

---

## 執行結果

> 貼上程式執行的實際範例輸出

```
<img width="2061" height="1220" alt="image" src="https://github.com/user-attachments/assets/2406078a-9357-480b-b8fd-da04990ba14f" />

<img width="1925" height="1182" alt="image" src="https://github.com/user-attachments/assets/7f8940c8-8a69-4335-aef5-fc55794e8374" />

<img width="1946" height="1220" alt="image" src="https://github.com/user-attachments/assets/5b7622c9-2b7c-41f6-b7c6-32f4e4b22223" />

```

---

## 各功能說明

### [查詢天氣]（負責：楊姍頤）

- **Tool 名稱**：get_weather
- **使用 API**：https://wttr.in/{city}?format=j1
- **輸入**：城市名稱：
- **輸出範例**：
- <img width="1296" height="608" alt="image" src="https://github.com/user-attachments/assets/1778aa3c-e776-447c-8f82-c1ed78e94a54" />


```python
TOOL = {
    "name": "",
    "description": "",
    "parameters": { ... }
}
```

### [取得隨機活動建議]（負責：林瑞城）

- **Tool 名稱**：get_random_activity
- **使用 API**：https://bored-api.appbrewery.com/random
- **輸入**：幫我想室內活動
- **輸出範例**：
-<img width="1029" height="550" alt="image" src="https://github.com/user-attachments/assets/ddae8e64-90df-43c7-b526-704ed8400085" />


### [取得隨機人生建議]（負責：林瑞城）

- **Tool 名稱**：get_daily_advice
- **使用 API**：https://api.adviceslip.com/advice
- **輸入**：人生建議
- **輸出範例**：
- <img width="1266" height="485" alt="image" src="https://github.com/user-attachments/assets/e00246d2-42a8-40f3-9308-610b4c1bae96" />


### Skill：比較多個城市的天氣（負責：楊姍頤）

- **組合了哪些 Tool**：`get_weather` (多次呼叫)
- **執行順序**：

```text
Step 1: 辨識使用者句子中提到的所有地點 → 取得 要比較的城市清單
Step 2: 根據清單多次呼叫 get_weather → 取得 個別城市的天氣狀態與溫度
Step 3: 組合所有城市的資料進行氣候條件分析 → 產生 最終比較結果與旅遊活動推薦
```

---

## 心得

### 遇到最難的問題

> 覺得是API的問題，因為每天能使用的次數很少，所以要很把握每次測試的機會，不能一直去嘗試，這大大的增加了我們測試的難度，透過輪流使用組員的google帳號來解決

### Tool 和 Skill 的差別

> Tool就是個一次只能使用一個的工具，而Skill則像是個技能，可以整合各個工具聯合使用，這大大的提升了使用個資源的方便性

### 如果再加一個功能

> 增加隨機生成一個笑話，讓笑來開啟新的一天很重要，過好開心的每一天
