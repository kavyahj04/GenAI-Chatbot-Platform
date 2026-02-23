import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'Research ChatBot',
    description: 'LLM-powered research chatbot with session and message logging.',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
