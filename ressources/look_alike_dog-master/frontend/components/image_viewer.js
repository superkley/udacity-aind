import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button } from 'reactstrap';

import * as actions from '../actions';
import { TAKE_SNAPSHOT_VIEW } from "../reducers/view_reducer";

class ImageViewer extends Component {
    onDetect() {
        const { imgSrc } = this.props.currentSnapshot;
        this.props.detectBreed(imgSrc);
    }
    
    render() {
        const { imgSrc } = this.props.currentSnapshot;
        if ( imgSrc ) {
            return (
                <div className="text-center">
                    <div className="imageView margin-lr-auto">
                        <span className="helper"></span><img className="center" src={imgSrc} />
                    </div>
                    <Button
                        onClick={() => this.props.changeView(TAKE_SNAPSHOT_VIEW)}    
                        className="mr-2" 
                        color="danger">Back</Button>
                    <Button 
                        onClick={this.onDetect.bind(this)}
                        color="success">
                            Detect breed
                    </Button>
                </div>
            )
        }
        return (
            <div>Take image first.</div>
        );
    }
}

function mapStateToProps(state) {
    return {
        currentSnapshot: state.currentSnapshot
    }
}

export default connect(mapStateToProps, actions)(ImageViewer);
