'use client';

import { Chat } from '@/components/chat/chat';

export default function Home() {
  return (
    <div suppressHydrationWarning>
      <Chat />
    </div>
  );
}
