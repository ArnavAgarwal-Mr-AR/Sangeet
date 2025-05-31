// app/components/MainInteractionPanel.tsx
"use client";

import React, { useState, ChangeEvent, useEffect, useRef } from 'react';
import { FaUpload, FaPlay, FaArrowUp, FaPlus, FaTimes } from 'react-icons/fa'; // Using react-icons

interface MainInteractionPanelProps {
  onRun: (data: { prompt: string; vocalFile?: File; beatsFile?: File }) => void;
}

const MainInteractionPanel: React.FC<MainInteractionPanelProps> = ({ onRun }) => {
  console.log("MainInteractionPanel rendered");
  const [prompt, setPrompt] = useState<string>('');
  const [vocalFile, setVocalFile] = useState<File | null>(null);
  const [beatsFile, setBeatsFile] = useState<File | null>(null);
  const [showUploadMenu, setShowUploadMenu] = useState(false);
  const plusButtonRef = useRef<HTMLButtonElement>(null);
  const uploadMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!showUploadMenu) return;
    function handleClickOutside(event: MouseEvent) {
      if (
        uploadMenuRef.current &&
        !uploadMenuRef.current.contains(event.target as Node) &&
        plusButtonRef.current &&
        !plusButtonRef.current.contains(event.target as Node)
      ) {
        setShowUploadMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showUploadMenu]);

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>,
    setFile: React.Dispatch<React.SetStateAction<File | null>>
  ) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleRunClick = () => {
    onRun({
      prompt,
      vocalFile: vocalFile || undefined,
      beatsFile: beatsFile || undefined,
    });
    // Potentially clear inputs after run, or handle based on app flow
    // setPrompt('');
    // setVocalFile(null);
    // setBeatsFile(null);
  };

  return (
    <div className="flex-grow p-6 flex flex-col items-center justify-start pt-55">
      <div className="w-full max-w-2xl space-y-3">
        <div className="text-center space-y-1 mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
            No producer? No problem.
          </h1>
          <p className="text-base text-gray-400">
            Step into the virtual studio, sing over fresh beats, and collaborate instantly with an AI that vibes with your style.
          </p>
        </div>
        {/* Prompt Box with + and Send Button */}
        <div className="flex items-center bg-gray-700 border border-gray-600 rounded-full px-4 py-2 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 ml-3">
          <button
            type="button"
            className="mr-2 text-gray-400 hover:text-blue-400 focus:outline-none flex-shrink-0"
            onClick={() => setShowUploadMenu((v) => !v)}
            ref={plusButtonRef}
          >
            <FaPlus size={20} />
          </button>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask anything"
            className="flex-1 bg-transparent outline-none text-gray-200 placeholder-gray-400 resize-none min-h-[32px] max-h-[120px] py-1 align-middle"
            rows={1}
            style={{ height: '32px', lineHeight: '1.5', display: 'flex', alignItems: 'center' }}
          />
          <button
            onClick={handleRunClick}
            className="ml-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 shadow-md transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 flex-shrink-0"
          >
            <FaArrowUp size={18} />
          </button>
        </div>
        {/* Upload Menu (dropdown) */}
        {showUploadMenu && (
          <div
            ref={uploadMenuRef}
            className="absolute z-30 mt-2 ml-8 bg-gray-800 border border-gray-700 rounded-md shadow-lg flex flex-col min-w-[180px]"
          >
            <label className="flex items-center px-4 py-2 cursor-pointer hover:bg-gray-700 text-gray-200">
              <FaUpload className="mr-2" /> Upload Vocal Audio
              <input
                type="file"
                accept=".wav,.mp3"
                className="hidden"
                onChange={(e) => {
                  handleFileChange(e, setVocalFile);
                  setShowUploadMenu(false);
                }}
              />
            </label>
            <label className="flex items-center px-4 py-2 cursor-pointer hover:bg-gray-700 text-gray-200">
              <FaUpload className="mr-2" /> Upload Beats Audio
              <input
                type="file"
                accept=".wav,.mp3"
                className="hidden"
                onChange={(e) => {
                  handleFileChange(e, setBeatsFile);
                  setShowUploadMenu(false);
                }}
              />
            </label>
          </div>
        )}
        {/* File Chips */}
        <div className="flex flex-wrap gap-2 mt-2 ml-12">
          {vocalFile && (
            <span className="flex items-center bg-blue-900 text-blue-200 px-3 py-1 rounded-full text-xs">
              Vocal: {vocalFile.name}
              <button
                className="ml-2 text-blue-300 hover:text-red-400 focus:outline-none"
                onClick={() => setVocalFile(null)}
                title="Remove"
              >
                <FaTimes size={12} />
              </button>
            </span>
          )}
          {beatsFile && (
            <span className="flex items-center bg-green-900 text-green-200 px-3 py-1 rounded-full text-xs">
              Beats: {beatsFile.name}
              <button
                className="ml-2 text-green-300 hover:text-red-400 focus:outline-none"
                onClick={() => setBeatsFile(null)}
                title="Remove"
              >
                <FaTimes size={12} />
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default MainInteractionPanel;
