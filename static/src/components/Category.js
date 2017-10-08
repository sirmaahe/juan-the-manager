import React, { Component } from 'react';

export default class Category extends Component {
  render() {
    return (
        <a>
            { this.props.name }
        </a>
    );
  }
}
