import { Message } from './message';

export type Room = {
    name: string;
    id: string;
    updated_at: Date | string;
    created_at: Date | string;
    messages: Message[];
};
