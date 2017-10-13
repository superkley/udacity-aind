import React, { Component } from 'react';
import Webcam from 'react-webcam';
import { connect } from 'react-redux';
import { Button } from 'reactstrap';

import * as actions from '../actions';
import { REVIEW_SNAPSHOT_VIEW } from "../reducers/view_reducer";

class WebcamCapture extends Component {
    setRef = (webcam) => {
        this.webcam = webcam;
    }
 
    capture = () => {
        const imageSrc = this.webcam.getScreenshot();
        this.props.takeSnapshot(imageSrc);
        this.props.changeView(REVIEW_SNAPSHOT_VIEW);
    };
 
    render() {
        return (
            <div className="text-center">
                <div className="videoPlayer margin-lr-auto">
                    <Webcam
                        audio={false}
                        height={350}
                        width={350}
                        ref={this.setRef}
                        screenshotFormat="image/jpeg"
                    />
                </div>
                <Button 
                    onClick={this.capture} 
                    color="primary"
                    >
                        Take snapshot
                </Button>
            </div>
        );
    }
}

export default connect(null, actions)(WebcamCapture);
