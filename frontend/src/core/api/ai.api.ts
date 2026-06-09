import { API_BASE_URL } from '@/core/api/client';

export interface AiChatContext {
  page?: string;
  complex_id?: string;
  complex_name?: string;
  space_id?: string;
}

export interface AiHistoryMessage {
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface AiSpaceCard {
  id: string;
  complex_id: string;
  complex_name?: string;
  building_name?: string;
  stype: string;
  rooms: string;
  area: number;
  floor?: number;
  floors_total?: number;
  price: number;
  metro?: string;
  metro_time?: string;
}

interface AiHistoryResponse {
  session_id: string;
  messages: AiHistoryMessage[];
}

interface StreamHandlers {
  onDelta: (text: string) => void;
  onCards?: (cards: AiSpaceCard[]) => void;
  onError?: (text: string) => void;
  signal?: AbortSignal;
}

export const aiApi = {
  getHistory: async (): Promise<AiHistoryMessage[]> => {
    const response = await fetch(`${API_BASE_URL}/api/ai/history`, {
      credentials: 'include',
    });

    if (!response.ok) {
      return [];
    }

    const data = (await response.json()) as AiHistoryResponse;

    return data.messages ?? [];
  },

  resetHistory: async (): Promise<void> => {
    await fetch(`${API_BASE_URL}/api/ai/history`, {
      method: 'DELETE',
      credentials: 'include',
    });
  },

  streamChat: async (
    message: string,
    context: AiChatContext | undefined,
    handlers: StreamHandlers,
  ): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/api/ai/chat`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context }),
      signal: handlers.signal,
    });

    if (!response.ok || !response.body) {
      handlers.onError?.('Не удалось получить ответ. Попробуйте позже.');
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    const handleEvent = (raw: string) => {
      const line = raw.trim();

      if (!line.startsWith('data:')) {
        return;
      }

      const payload = line.slice('data:'.length).trim();

      if (!payload) {
        return;
      }

      try {
        const event = JSON.parse(payload) as {
          type: string;
          text?: string;
          items?: AiSpaceCard[];
        };

        if (event.type === 'delta' && event.text) {
          handlers.onDelta(event.text);
        } else if (event.type === 'cards' && event.items?.length) {
          handlers.onCards?.(event.items);
        } else if (event.type === 'error') {
          handlers.onError?.(event.text ?? 'Ошибка ответа.');
        }
      } catch {
        // ignore malformed chunk
      }
    };

    for (;;) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      const events = buffer.split('\n\n');
      buffer = events.pop() ?? '';

      events.forEach(handleEvent);
    }

    if (buffer.trim()) {
      handleEvent(buffer);
    }
  },
};
