import React, { Component } from 'react';

export default class CategoryInput extends Component {
  render() {
    return (
      <div>
        <input onChange={ (e) => { this.setState({ category: e.target.value }) } }>{ this.state.category }</input>
        <button onClick={ this.props.updateCategory(this.state.category) }>сохранить</button>
      </div>
    );
  }
}
