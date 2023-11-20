import React, { useState } from 'react';
import EditorToolbar from '../service/editors-toolbar';
import "../css/block.css"

const AssignmentBlock = ({ block, updateBlock, removeBlock }) => {
  const [title, setTitle] = useState(block.title);
  const [choices, setChoices] = useState(block.choices);
  const [minValue, setMinValue] = useState(block.minValue || 0);
  const [maxValue, setMaxValue] = useState(block.maxValue || 10);

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
    updateBlock(block.id, block.content, choices, event.target.value);
  };

  const handleChoiceChange = (index, event) => {
    const newChoices = [...choices];
    newChoices[index] = event.target.value;
    setChoices(newChoices);
    updateBlock(block.id, block.content, newChoices, title);
  };

  const handleMinChange = (change, e) => {
    e.preventDefault()
    const newValue = Math.max(0, minValue + change);
    setMinValue(newValue);
    updateBlock(block.id, block.content, block.choices, title, newValue, maxValue);
  };

  const handleMaxChange = (change, e) => {
    e.preventDefault()
    const newValue = Math.max(minValue, maxValue + change);
    setMaxValue(newValue);
    updateBlock(block.id, block.content, block.choices, title, minValue, newValue);
  };

  const handleNumberChange = (event, type) => {
    const value = parseInt(event.target.value, 10) || 0;
    if (type === "min") {
      setMinValue(value);
      updateBlock(block.id, block.content, block.choices, title, value, maxValue);
    } else {
      setMaxValue(value);
      updateBlock(block.id, block.content, block.choices, title, minValue, value);
    }
  };

  const handleNewChoiceFocus = (event) => {
    if (event.target.value === '') {
      addChoice();
    }
  };

  const addChoice = (newChoice = '') => {
    const newChoices = [...choices, newChoice];
    setChoices(newChoices);
    updateBlock(block.id, block.content, newChoices, title);
  };

  const removeChoice = (index) => {
    const newChoices = choices.filter((_, i) => i !== index);
    setChoices(newChoices);
    updateBlock(block.id, block.content, newChoices, title);
  };

  if (block.type === 'text') {
    return (
      <div className="block">
        <div className='block-header'>
          <input
            type="text"
            value={title}
            onChange={handleTitleChange}
            placeholder="Write question here..."
            className="block-title-input"
          />
          <button type="button" onClick={() => removeBlock(block.id)} className="remove-block-button">
            &#10006; 
          </button>
        </div>
        
        <EditorToolbar editorState={block.content} setEditorState={(newState) => updateBlock(block.id, newState, block.choices)} />
      </div>
    );
  }

  if(block.type === 'range'){
    return (
      <div className="block">
        <div className="control-panel">
          <input
            type="text"
            value={title}
            onChange={handleTitleChange}
            placeholder="Write question here..."
            className="block-title-input"
          />
          <button type="button" onClick={() => removeBlock(block.id)} className="remove-block-button">
            <i class='fa fa-trash-o'></i>
          </button>
        </div>
        <div className="range-inputs">
          <div className="number-input-container">
            <button onClick={(e) => handleMinChange(-1, e)}>-</button>
            <input type="number" value={minValue} onChange={(e) => handleNumberChange(e, "min")} />
            <button onClick={(e) => handleMinChange(1, e)}>+</button>
          </div>
          <div className="number-input-container">
            <button onClick={(e) => handleMaxChange(-1, e)}>-</button>
            <input type="number" value={maxValue} onChange={(e) => handleNumberChange(e, "max")} />
            <button onClick={(e) => handleMaxChange(1, e)}>+</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="block">
      <div className="control-panel">
        <input
          type="text"
          value={title}
          onChange={handleTitleChange}
          placeholder="Write question here..."
          className="block-title-input"
        />
        <button type="button" onClick={() => removeBlock(block.id)} className="remove-block-button">
          <i class='fa fa-trash-o'></i>
        </button>
      </div>
      {choices.map((choice, index) => (
        <div key={index} className="choice-option">
          {block.type === 'multiple' ? (
            <input type="checkbox" name={`block-${block.id}-choice`} />
          ) : (
            <input type="radio" name={`block-${block.id}-choice`} />
          )}
          <input
            type="text"
            value={choice}
            onChange={(event) => handleChoiceChange(index, event)}
            placeholder={`Option ${index + 1}`}
            className="choice-input"
          />
          <button type="button" onClick={() => removeChoice(index)} className="remove-choice-button">
            &#10006; 
          </button>
        </div>
      ))}
      <div className='choice-option'>
        {
          block.type === 'single' ? <input type="radio" disabled style={{ opacity: 0.8 }} /> : <input type="checkbox" disabled style={{ opacity: 0.8 }} /> 
        }
        <input
          type="text"
          value=''
          onFocus={handleNewChoiceFocus}
          placeholder="Add option..."
          style={{ opacity: 0.8 }}
          className="choice-input"
        />
      </div>
      
    </div>
  );
};

export default AssignmentBlock;