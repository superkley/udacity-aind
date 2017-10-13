import { CHANGE_VIEW } from '../actions/types';

export const TAKE_SNAPSHOT_VIEW = 'TAKE_SNAPSHOT_VIEW';
export const REVIEW_SNAPSHOT_VIEW = 'REVIEW_SNAPSHOT_VIEW';
export const RESULT_VIEW = 'RESULT_VIEW';

export default function(state = { view: TAKE_SNAPSHOT_VIEW }, action) {
    switch(action.type) {
        case CHANGE_VIEW:
            return { view: action.payload };
    }
    
    return state;
}
