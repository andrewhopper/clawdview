import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import { configureAmplify } from '@/lib/amplify';
import '@/styles/globals.css';

// Configure Amplify for Cognito authentication
configureAmplify();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
