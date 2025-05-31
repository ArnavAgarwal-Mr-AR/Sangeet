// app/components/SettingsSidebar.tsx
"use client";

import React from 'react';
import { FaTimes } from 'react-icons/fa'; // For close button
import IconButton from '../IconButton'; // Assuming you created this

interface SettingsSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  settings: {
    drumStyle: string;
    systemPrompt: string;
    // Add more settings as needed
  };
  onSettingsChange: (newSettings: Partial<SettingsSidebarProps['settings']>) => void;
}

const drumStyles = ["Pop", "Rock", "Jazz", "Electronic", "Hip-Hop", "Acoustic"];

const SettingsSidebar: React.FC<SettingsSidebarProps> = ({
  isOpen,
  onClose,
  settings,
  onSettingsChange,
}) => {
  if (!isOpen) return null;

  const handleChange = (
    e: React.ChangeEvent<HTMLSelectElement | HTMLTextAreaElement | HTMLInputElement>
  ) => {
    onSettingsChange({ [e.target.name]: e.target.value });
  };

  return (
    <div
      className={`w-80 bg-gradient-to-b from-black via-blue-900/30 to-blue-800/20 p-6 border-r border-gray-700/50 shadow-xl rounded-r-2xl flex-shrink-0 overflow-y-auto transition-all duration-1000 ease-in-out transform ml-2 ${
        isOpen ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0'
      }`}
      style={{ willChange: 'transform, opacity' }}
    >
      <div className="flex justify-between items-center mb-4 bg-black/40 p-3 rounded-lg">
        <h2 className="text-lg font-semibold text-gray-100">Settings</h2>
        <IconButton icon={<FaTimes />} onClick={onClose} className="text-gray-300 bg-black/80 hover:bg-black/60" tooltip="Close Settings" />
      </div>

      <div className="space-y-4">
        {/* Drum Style Setting */}
        <div>
          <label htmlFor="drumStyle" className="block text-sm font-medium text-gray-300 mb-1">
            Drum Style
          </label>
          <select
            id="drumStyle"
            name="drumStyle"
            value={settings.drumStyle}
            onChange={handleChange}
            className="w-full p-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-200"
          >
            {drumStyles.map((style) => (
              <option key={style} value={style.toLowerCase().replace(' ', '-')}>
                {style}
              </option>
            ))}
          </select>
        </div>

        {/* System Prompt Setting */}
        <div>
          <label htmlFor="systemPrompt" className="block text-sm font-medium text-gray-300 mb-1">
            System Prompt (Advanced)
          </label>
          <textarea
            id="systemPrompt"
            name="systemPrompt"
            rows={4}
            value={settings.systemPrompt}
            onChange={handleChange}
            placeholder="e.g., Focus on clear vocals, add reverb..."
            className="w-full p-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-200 placeholder-gray-400"
          />
        </div>

        {/* Temperature Slider */}
        <div>
          <label htmlFor="temperature" className="block text-sm font-medium text-gray-300 mb-1">
            Creativity (Temperature)
          </label>
          <input
            type="range"
            id="temperature"
            name="temperature"
            min="0.1"
            max="1.0"
            step="0.1"
            className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
      </div>

      <button
        onClick={onClose}
        className="mt-6 w-full py-2.5 px-4 bg-gradient-to-r from-blue-600 to-blue-400 hover:from-blue-700 hover:to-blue-500 text-white font-medium rounded-lg shadow-lg transition-all duration-200 ease-in-out transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
      >
        Save Changes
      </button>
    </div>
  );
};

export default SettingsSidebar;