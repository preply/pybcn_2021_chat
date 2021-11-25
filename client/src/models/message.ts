import { Languages } from './languages';

export type Message = {
    id: string;
    text: string;
    lang: Languages;
    user_id: string;
    created_at: Date | string;
};
