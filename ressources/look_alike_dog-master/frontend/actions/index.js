import axios from 'axios';
import { CHANGE_VIEW, TAKE_SNAPSHOT, UPDATE_RESULT } from './types';
import { RESULT_VIEW } from "../reducers/view_reducer";


const DOMAIN = window.location.hostname;
const PROTOCOL = window.location.protocol;
const PORT = window.location.port;
const API_URL = `${PROTOCOL}//${DOMAIN}:${PORT}/process_img`;

export function takeSnapshot(imgSrc) {
    return {
        type: TAKE_SNAPSHOT,
        payload: imgSrc
    }
}

export function changeView(view) {
    return {
        type: CHANGE_VIEW,
        payload: view
    }
}

export function detectBreed(imgSrc) {
    return function (dispatch) {
        dispatch({
            type: CHANGE_VIEW,
            payload: RESULT_VIEW
        });
        axios.post(API_URL, {'imgSrc': imgSrc})
            .then(function (response) {
                dispatch({
                    type: UPDATE_RESULT,
                    payload: { breed: response.data.breed, loading: false }
                });
            })
            .catch(function (error) {
                console.log(error);
            });
    };
}

export function clearResult() {
    return {
        type: UPDATE_RESULT,
        payload: { loading: true }
    }
}
