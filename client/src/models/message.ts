import { Languages } from './languages';
import { User } from './user';

export type Message = {
    id: string;
    text: string;
    lang: Languages;
    user: Pick<User, 'id' | 'name'>;
    created_at: Date | string;
};
