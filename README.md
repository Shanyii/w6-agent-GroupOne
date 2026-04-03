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
| 楊姍頤 | Skill 整合   | `skills/` | — |
| 楊姍頤 | Agent 主程式 | `main.py` | — |

---

## 專案架構

範例：

```
├── tools/
│   ├── xxx_tool.py   
│   ├── xxx_tool.py   
│   └── xxx_tool.py  
├── skills/
│   └── xxx_skill.py  
├── main.py        
├── requirements.txt
└── README.md
```

---

## 使用方式

範例：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 執行結果

> 貼上程式執行的實際範例輸出

```
（貼上執行結果，例如下的指令與輸出結果）
```

---

## 各功能說明

### [功能名稱]（負責：姓名）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

```python
TOOL = {
    "name": "",
    "description": "",
    "parameters": { ... }
}
```

### [功能名稱]（負責：姓名）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

### [功能名稱]（負責：姓名）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

### Skill：[Skill 名稱]（負責：姓名）

- **組合了哪些 Tool**：
- **執行順序**：

```
Step 1: 呼叫 ___ → 取得 ___
Step 2: 呼叫 ___ → 取得 ___
Step 3: 組合輸出 → 產生 ___
```

---

## 心得

### 遇到最難的問題

> 寫下這次實作遇到最困難的事，以及怎麼解決的

### Tool 和 Skill 的差別

> 用自己的話說說，做完後你怎麼理解兩者的不同

### 如果再加一個功能

> 如果可以多加一個 Tool，你會加什麼？為什麼？
