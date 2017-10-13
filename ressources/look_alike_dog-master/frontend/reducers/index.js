import { combineReducers } from 'redux';

import snapshotReducer from './snapshot_reducer';
import viewReducer from './view_reducer';
import resultReducer from './result_reducer';

const rootReducer = combineReducers({
    currentSnapshot: snapshotReducer,
    currentView: viewReducer,
    currentResult: resultReducer
});

export default rootReducer;
