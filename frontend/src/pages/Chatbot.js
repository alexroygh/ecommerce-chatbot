import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import { useAuth } from '../context/AuthContext';

export default function Chatbot() {
  const { user, logout } = useAuth();
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chat_history');
    return saved ? JSON.parse(saved) : [];
  });
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('chat_history', JSON.stringify(messages));
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input, timestamp: new Date().toISOString() };
    setMessages(msgs => [...msgs, userMsg]);
    setLoading(true);
    try {
      const res = await api.post('/api/chat', { message: input });
      setMessages(msgs => [...msgs, { sender: 'bot', text: res.data.reply, timestamp: res.data.timestamp }]);
    } catch (err) {
      console.log(err);
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Error: Could not reach server.', timestamp: new Date().toISOString() }]);
    }
    setInput('');
    setLoading(false);
  };

  const handleReset = () => {
    setMessages([]);
    localStorage.removeItem('chat_history');
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-50">
      <div className="w-full max-w-lg mt-8 bg-white rounded shadow p-4 flex flex-col h-[80vh]">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-xl font-bold">E-commerce Chatbot</h2>
          <button onClick={logout} className="text-sm text-red-500 hover:underline">Logout</button>
        </div>
        <div className="flex-1 overflow-y-auto border rounded p-2 bg-gray-100 mb-2">
          {messages.map((msg, i) => (
            <div key={i} className={`mb-2 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`px-3 py-2 rounded-lg max-w-xs ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-900'}`}>
                <div className="text-xs opacity-60 mb-1">{new Date(msg.timestamp).toLocaleTimeString()}</div>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            className="flex-1 border rounded p-2"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Send</button>
          <button type="button" className="bg-gray-300 px-2 py-2 rounded" onClick={handleReset}>Reset</button>
        </form>
      </div>
    </div>
  );
} 