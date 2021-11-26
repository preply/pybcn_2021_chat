import { Languages } from './languages';

export type User = {
    id: string;
    name: string;
    is_active: boolean;
    role: string;
    lang: Languages;
    updated_at: Date | string;
    created_at: Date | string;
};
