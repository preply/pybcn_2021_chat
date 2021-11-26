import { User } from '../../models/user';

export enum CoreActionsType {
    SET_USER = '[User] set user data',
}

export type SetUser = {
    type: CoreActionsType.SET_USER;
    user: User;
};

export type CoreActions = SetUser;

export const setUser = (user: User): CoreActions => ({
    type: CoreActionsType.SET_USER,
    user,
});
