import { createStore, combineReducers } from 'redux';
import { CoreState, coreReducer as core } from './core/core.reducer';

export type State = {
    core: CoreState;
};

export const reducers = combineReducers({
    core,
});

export default createStore(reducers);
