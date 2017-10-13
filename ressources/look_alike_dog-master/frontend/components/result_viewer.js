import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button } from 'reactstrap';

import * as actions from '../actions';
import { TAKE_SNAPSHOT_VIEW } from "../reducers/view_reducer";

class ResultViewer extends Component {
    onTryAgain() {
        this.props.changeView(TAKE_SNAPSHOT_VIEW);
        this.props.clearResult();
    }
    
    render() {
        const { imgSrc } = this.props.currentSnapshot;
        const { loading, breed } = this.props.currentResult;
        
        if (loading) {
            return (
                <div className="text-center">
                    <div className="imageView margin-lr-auto">
                        <span className="helper"></span><img className="center" src={imgSrc} />
                    </div>
                        <Button 
                            className="btnTryAgain"
                            disabled>
                                Try again
                        </Button>
                    <div>Loading...</div>
                </div>
            );
        } else {
            return (
                <div className="text-center">
                    <div className="imageView margin-lr-auto">
                        <span className="helper"></span><img className="center" src={imgSrc} />
                    </div>
                    <Button 
                        className="btnTryAgain"
                        onClick={this.onTryAgain.bind(this)}
                        color="success">
                            Try again
                    </Button>
                    <div>You look like a {this.props.currentResult.breed}.</div>
                </div>
            );
        }
    }
}

function mapStateToProps(state) {
    return {
        currentSnapshot: state.currentSnapshot,
        currentResult: state.currentResult
    }
}

export default connect(mapStateToProps, actions)(ResultViewer);
