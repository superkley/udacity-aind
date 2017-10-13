import { TAKE_SNAPSHOT } from '../actions/types';

export default function( state = { imgSrc: "http://via.placeholder.com/350x350/" }, action ) {
    switch(action.type) {
        case TAKE_SNAPSHOT:
            return { imgSrc: action.payload }
    }
    
    return state;
}
