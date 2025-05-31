// app/components/ChatHistoryPanel.tsx
"use client"; // If you plan to have interactive elements or state here

import React from 'react';

// Dummy data for now
const historyItems = [
  { id: 1, title: "My First Track - Pop Beat" },
  { id: 2, title: "Vocal Experiment - Jazz Drums" },
  { id: 3, title: "Beat Idea - Lo-fi" },
];

const ChatHistoryPanel = () => {
  return (
    <div className="w-64 bg-gray-800 p-4 border-r border-gray-700 flex-shrink-0 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4 text-gray-300">History</h2>
      <ul>
        {historyItems.map((item) => (
          <li
            key={item.id}
            className="mb-2 p-2 rounded-md hover:bg-gray-700 cursor-pointer text-sm text-gray-400"
          >
            {item.title}
          </li>
        ))}
      </ul>
      {/* You might add a "New Chat/Project" button here */}
    </div>
  );
};

export default ChatHistoryPanel;