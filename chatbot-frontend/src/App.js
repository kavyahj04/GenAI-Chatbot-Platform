import "./App.css";
import { useState } from "react";

export default function App(){

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const changeEvent = () =>
  {
    if(input.trim() === "") return;

    const userMessage = { sender : "user", text: input}
    const botMessage = { sender: "bot", text: "I am a bot!" };
    setMessages([...messages, userMessage, botMessage]);
    setInput("");
  }

  const handleEndChat = () => {
    alert("redirection to survey soon.");
  }

  return(
    <div className="app">
      <div className="main">
       <div className="chat-header">
          <h3>Research Chat</h3>
          <button className="end-chat-btn" onClick={handleEndChat}>
            End Chat
          </button>
        </div>
        
         <div className="chat-box">
         {messages.length === 0 && (
            <div className="empty-state">
              <h2>How can I help you today?</h2>
            </div>
          )}
          {messages.map((messages, index) => (
            <div key = {index} className={`message ${messages.sender}`}>
              <div className="avatar">
              {messages.sender === "user" ? "👤" : "🤖"}
              </div>
              <div className="message">
                {messages.text}
              </div>
            </div>
          ))}
        </div>

         <div className="input-area">
          <input type="text" 
          placeholder="Message chatbot..."  
          value={input}
          onChange={(e) => setInput(e.target.value)}
          />
          <button disabled={!input.trim()} onClick={changeEvent}>➤</button>
        </div>
      </div>
    </div>
  )
}