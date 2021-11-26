import { User } from '../../models/user';
import { CoreActions, CoreActionsType } from './core.actions';
import { useSelector } from 'react-redux';
import { State } from '../index';

export type CoreState = {
    user: User | null;
};

const initialState: CoreState = {
    user: null,
};

export const coreReducer = (state = initialState, action: CoreActions): CoreState => {
    switch (action.type) {
        case CoreActionsType.SET_USER:
            return { ...state, user: action.user };
        default:
            return state;
    }
};

export const useCoreUser = () => useSelector((state: State) => state.core.user);
