document.addEventListener('DOMContentLoaded', () => {
  const chatArea = document.getElementById('chatArea');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');

  // 自動捲動到最下面
  const scrollToBottom = () => {
    chatArea.scrollTop = chatArea.scrollHeight;
  };

  // 添加新訊息到畫面
  const addMessage = (content, sender, isTool = false) => {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    if (isTool) {
      // 如果是工具執行的視覺化
      messageDiv.innerHTML = `
        <div class="tool-card">
          <i>⚙️</i> <span>${content}</span>
        </div>
      `;
    } else {
      // 一般對話泡泡
      messageDiv.innerHTML = `
        <div class="bubble">
          ${content}
        </div>
      `;
    }
    
    chatArea.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
  };

  // 添加正在打字的動畫
  const addTypingIndicator = () => {
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'message agent typing-msg';
    indicatorDiv.innerHTML = `
      <div class="bubble">
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    `;
    chatArea.appendChild(indicatorDiv);
    scrollToBottom();
    return indicatorDiv;
  };

  // 處理訊息發送流程
  const handleSend = async () => {
    const text = chatInput.value.trim();
    if (!text) return;

    // 1. 顯示使用者訊息
    addMessage(text, 'user');
    chatInput.value = '';

    // 2. 顯示思考中動畫
    const typingIndicator = addTypingIndicator();

    try {
      // 3. 發送真實 API 請求給 Flask 後端
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();
      
      // 移除思考中動畫
      chatArea.removeChild(typingIndicator);

      if (data.error) {
        addMessage(`錯誤發生: ${data.error}`, 'agent');
        return;
      }

      // 4. 解析回傳資料，顯示工具執行過程
      if (data.tools_called && data.tools_called.length > 0) {
        data.tools_called.forEach(tool => {
          addMessage(`呼叫工具: ${tool}`, 'agent', true);
        });
        
        // 稍微顯示一下思考動畫以假亂真，增加真實感
        const typingIndicator2 = addTypingIndicator();
        await new Promise(r => setTimeout(r, 600));
        chatArea.removeChild(typingIndicator2);
      }

      // 5. 顯示最終回答
      addMessage(data.response, 'agent');

    } catch (error) {
      chatArea.removeChild(typingIndicator);
      addMessage(`網路連線錯誤: ${error.message}`, 'agent');
    }
  };

  // 綁定事件
  sendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
  });
});
