import React, { Component } from 'react';

export default class Note extends Component {
  render() {
    return (
      <div>
        <p>
            { this.props.note.text } <span onClick={ () => { this.props.delete( this.props.note ) } }>удалить</span>
        </p>
      </div>
    );
  }
}
