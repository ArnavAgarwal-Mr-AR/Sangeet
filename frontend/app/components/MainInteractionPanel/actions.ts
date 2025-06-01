'use server';

export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:10000';

// Log the backend URL in development
//if (process.env.NODE_ENV === 'development') {
  //console.log('Using backend URL:', BACKEND_URL);
//}

export async function generateBeat(prompt: string) {
    try {
        console.log('Sending request to backend with prompt:', prompt);
        const response = await fetch(`${BACKEND_URL}/generate/beat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();
        console.log('JSON response:', data);

        // If we have a beat_path, fetch the actual audio file
        if (data.beat_path) {
            // Remove any leading slashes from the path
            const cleanPath = data.beat_path.replace(/^\/+/, '');
            console.log('Fetching audio file from path:', cleanPath);
            
            // Construct the full URL for the audio file
            const audioUrl = `${BACKEND_URL}/${cleanPath}`;
            console.log('Full audio URL:', audioUrl);
            
            const audioResponse = await fetch(audioUrl);
            
            if (!audioResponse.ok) {
                throw new Error(`Failed to fetch audio file: ${audioResponse.status} - ${audioUrl}`);
            }

            const audioBlob = await audioResponse.blob();
            console.log('Audio blob received:', {
                size: audioBlob.size,
                type: audioBlob.type
            });

            return {
                audioBlob,
                type: audioBlob.type,
                originalResponse: data
            };
        }

        return data;
    } catch (error) {
        console.error('Error generating beat:', error);
        throw error;
    }
} 