import React from 'react';
import ReactDOM from 'react-dom';
import reduxThunk from 'redux-thunk';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';

import App from './components/app';
import reducers from './reducers'


const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);
const store = createStoreWithMiddleware(reducers, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

ReactDOM.render(
    <Provider store={store}>
        <div>
            <App />
        </div>
    </Provider>
    , document.querySelector('.container-fluid'));
