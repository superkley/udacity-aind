import React, { Component } from 'react';
import { connect } from 'react-redux';

import WebcamCapture from './webcam_capture';
import ImageViewer from './image_viewer';
import ResultViewer from './result_viewer';
import { RESULT_VIEW, REVIEW_SNAPSHOT_VIEW, TAKE_SNAPSHOT_VIEW } from "../reducers/view_reducer";

class App extends Component {
    render() {
        const { view } = this.props.currentView;
        switch(view) {
            case TAKE_SNAPSHOT_VIEW:
                return <WebcamCapture />
            case REVIEW_SNAPSHOT_VIEW:
                return <ImageViewer />
            case RESULT_VIEW:
                return <ResultViewer />
        }
    }
}

function mapStateToProps(state) {
    return {
        currentView: state.currentView
    }
}

export default connect(mapStateToProps)(App); 
