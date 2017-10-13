import { UPDATE_RESULT } from '../actions/types';

export default function( state = { loading: true }, action ) {
    switch(action.type) {
        case UPDATE_RESULT:
            return action.payload
    }
    
    return state;
}
