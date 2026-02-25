import "./App.css";
import { useState } from "react";

export default function App(){

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const urlParams = new URLSearchParams(window.location.search);
  const prolificId = urlParams.get('PROLIFIC_PID');
  const sessionId = urlParams.get('SESSION_ID');
  const [turnId, setTurnId] = useState(1);

  const changeEvent = async () =>
  {
    if(input.trim() === "") return;

    const userMessage = { sender : "user", text: input}
    setMessages(prev => [...prev, userMessage]);

    try{
      const response = await fetch("http://127.0.0.1:8000/chat",{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_message: input,
          client_turn_id: turnId.toString(),
          chat_session_id: "XYZ"
        })
      });

      const data = await response.json();
      const botMessage = { sender: "bot", text: data.response };
      setMessages(prevMessages => [...prevMessages, botMessage]);
      setTurnId(prevTurnId => prevTurnId + 1);
      setInput("");
    }
    catch(error){
      const errorMessage = { sender: "error", text: "Error sending message." };
      setMessages(prev => [...prev, errorMessage]);
      console.error("Error sending message:", error);
    }
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