import React, { Component } from 'react';

export default class CategoryInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            category: this.props.category
        }
    }

    render() {
        return (
          <div>
            <input onChange={ (e) => { this.setState({ category: e.target.value }) } }>{ this.state.category }</input>
            <button onClick={ this.props.updateCategory(this.state.category) }>сохранить</button>
          </div>
        );
    }
}
