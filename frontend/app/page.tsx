// app/page.tsx
"use client"; // This page needs client-side interactivity

import React, { useState } from 'react';
import NavBar from './components/NavBar/NavBar';
import ChatHistoryPanel from './components/ChatHistory/ChatHistoryPanel';
import MainInteractionPanel from './components/MainInteractionPanel/MainInteractionPanel';
import SettingsSidebar from './components/Settings/SettingsSidebar';
import IconButton from './components/IconButton'; // Assuming you created this
import { FaBars, FaHistory } from 'react-icons/fa'; // For hamburger and history icons

// Define a type for your settings
interface AppSettings {
  drumStyle: string;
  systemPrompt: string;
  // Add more settings here
}

export default function VocaliqAppPage() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  // const [isChatHistoryOpen, setIsChatHistoryOpen] = useState(false);
  const [settings, setSettings] = useState<AppSettings>({
    drumStyle: 'pop', // Default drum style
    systemPrompt: 'Generate high-quality audio.', // Default system prompt
  });

  const toggleSettingsSidebar = () => {
    console.log('Toggling settings sidebar, current state:', isSettingsOpen);
    setIsSettingsOpen(prev => !prev);
  };

  // const toggleChatHistory = () => {
  //   setIsChatHistoryOpen(!isChatHistoryOpen);
  // };

  const handleSettingsChange = (newSettings: Partial<AppSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const handleRun = (data: { prompt: string; vocalFile?: File; beatsFile?: File }) => {
    console.log("Running with:", {
      ...data,
      settings,
    });
    // Here you would make an API call to your backend/AI service
    // For now, we just log it.
    // You might want to add the result to the ChatHistoryPanel
  };

  return (
    <div className="flex flex-col min-h-screen bg-black text-gray-100">
      <NavBar />
      <main className="flex flex-1 overflow-hidden pt-[80px]">
        <SettingsSidebar
          isOpen={isSettingsOpen}
          onClose={() => {
            console.log('Settings close triggered');
            setIsSettingsOpen(false);
          }}
          settings={settings}
          onSettingsChange={handleSettingsChange}
        />
        <div className="flex-1 flex flex-col relative overflow-y-auto">
          {!isSettingsOpen && (
            <div className="absolute top-4 left-6 z-20">
              <IconButton
                icon={<FaBars size={20} />}
                onClick={toggleSettingsSidebar}
                className="text-gray-400 hover:text-gray-200 rounded-full hover:bg-black/20 transition-all duration-200"
                tooltip="Open Settings"
              />
            </div>
          )}
          {/* <div className="absolute top-4 left-4 z-20">
            <IconButton
              icon={<FaHistory size={20} />}
              onClick={toggleChatHistory}
              className="text-gray-400 hover:text-gray-200 bg-gray-750 hover:bg-gray-600"
              tooltip="Chat History"
            />
          </div> */}
          <MainInteractionPanel onRun={handleRun} />
        </div>
      </main>
      {/* Overlay for when sidebars are open */}
      {(isSettingsOpen /* || isChatHistoryOpen */) && (
        <div
          className={`fixed inset-0 bg-black transition-all duration-1000 ease-in-out ${
            isSettingsOpen ? 'opacity-50' : 'opacity-0'
          } z-20 md:hidden`}
          style={{ willChange: 'opacity' }}
          onClick={() => {
            if (isSettingsOpen) toggleSettingsSidebar();
            // if (isChatHistoryOpen) toggleChatHistory();
          }}
        ></div>
      )}
    </div>
  );
}