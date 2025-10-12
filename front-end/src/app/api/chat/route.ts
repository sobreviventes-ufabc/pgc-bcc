import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  console.log('[API] Received chat request at:', new Date().toISOString());
  
  // Check if BACKEND_URL is configured
  if (!process.env.BACKEND_URL) {
    console.error('[API] BACKEND_URL environment variable is not configured');
    return NextResponse.json(
      { error: 'Backend URL not configured' },
      { status: 500 }
    );
  }
  
  try {
    const body = await request.json();
    console.log('[API] Request body:', JSON.stringify(body, null, 2));
    
    const backendUrl = `${process.env.BACKEND_URL}/chat`;
    console.log('[API] Forwarding request to backend:', backendUrl);
    
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    
    console.log('[API] Backend response status:', response.status);
    
    if (!response.ok) {
      console.error('[API] Backend error:', response.status, response.statusText);
      return NextResponse.json(
        { error: 'Backend request failed' },
        { status: response.status }
      );
    }
    
    const data = await response.json();
    console.log('[API] Backend response data:', JSON.stringify(data, null, 2));
    
    console.log('[API] Successfully proxied request');
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('[API] Error proxying request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}