// app/components/IconButton.tsx
import React from 'react';

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  tooltip?: string;
}

const IconButton: React.FC<IconButtonProps> = ({ icon, tooltip, className, ...props }) => {
  return (
    <button
      title={tooltip}
      className={`p-2 rounded-md hover:bg-black/20 focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
      {...props}
    >
      {icon}
    </button>
  );
};

export default IconButton;