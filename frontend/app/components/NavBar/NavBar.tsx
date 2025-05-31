'use client';

import React, { useState, useEffect } from 'react';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { LogOut, User, Mail } from 'lucide-react';

const NavBar = () => {
  const [user, setUser] = useState<any>(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const router = useRouter();
  const supabase = createClientComponentClient();

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    };

    getUser();

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, [supabase.auth]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push('/login');
    router.refresh();
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (showDropdown && !(event.target as Element).closest('.profile-dropdown')) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showDropdown]);

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 z-50 bg-[#0A0A0A]/90 backdrop-blur-md flex items-center px-4 shadow-lg border-b border-gray-800/30">
      <div className="w-full mx-auto flex items-center justify-between">
        <h1 className="font-['Product_Sans',_'Google_Sans',_'Helvetica_Neue',_sans-serif] text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent m-0 tracking-tight whitespace-nowrap min-w-max hover:opacity-90 transition-opacity ml-4">
          Vocaliq AI
        </h1>

        {user && (
          <div className="relative profile-dropdown">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="flex items-center space-x-2 focus:outline-none hover:opacity-80 transition-opacity"
            >
              {user.user_metadata?.avatar_url ? (
                <Image
                  src={user.user_metadata.avatar_url}
                  alt="Profile"
                  width={36}
                  height={36}
                  className="rounded-full border-2 border-blue-500/50"
                />
              ) : (
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white border-2 border-blue-500/50">
                  {user.email?.[0]?.toUpperCase() || 'U'}
                </div>
              )}
            </button>

            {showDropdown && (
              <div className="absolute right-0 mt-2 w-64 rounded-lg shadow-xl bg-[#1A1A1A] border border-gray-800/50 backdrop-blur-xl">
                <div className="p-4 border-b border-gray-800/50">
                  <div className="flex items-center space-x-3">
                    {user.user_metadata?.avatar_url ? (
                      <Image
                        src={user.user_metadata.avatar_url}
                        alt="Profile"
                        width={40}
                        height={40}
                        className="rounded-full border-2 border-blue-500/50"
                      />
                    ) : (
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white border-2 border-blue-500/50">
                        {user.email?.[0]?.toUpperCase() || 'U'}
                      </div>
                    )}
                    <div>
                      <p className="text-sm font-medium text-gray-200">
                        {user.user_metadata?.full_name || 'User'}
                      </p>
                      <p className="text-xs text-gray-400 truncate max-w-[180px]">
                        {user.email}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-2">
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-800/50 rounded-md transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
