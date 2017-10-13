import React, { Component } from 'react';
import CategoryInput from './CategoryInput'

export default class Note extends Component {
    render() {
        return (
          <div>
            <p>
                { this.props.note.text }
                <span onClick={ () => { this.props.delete( this.props.note ) } }>удалить</span>
                <CategoryInput
                    category={ this.props.category }
                    updateCategory={ (name) => this.props.updateCategory( this.props.note, name )}
                />
            </p>
          </div>
        );
    }
}
