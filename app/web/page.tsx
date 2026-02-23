'use client';

import { useState } from 'react';
import { Message } from '@/types/chat';
import ChatHeader from '@/components/ChatHeader';
import ChatBox from '@/components/ChatBox';
import ChatInput from '@/components/ChatInput';

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);

    const handleSend = (text: string) => {
        const userMessage: Message = { sender: 'user', text };
        const botMessage: Message = { sender: 'bot', text: 'I am a bot!' };
        setMessages((prev) => [...prev, userMessage, botMessage]);
    };

    const handleEndChat = () => {
        alert('Redirecting to survey soon.');
    };

    return (
        <div className="app">
            <div className="main">
                <ChatHeader onEndChat={handleEndChat} />
                <ChatBox messages={messages} />
                <ChatInput onSend={handleSend} />
            </div>
        </div>
    );
}
