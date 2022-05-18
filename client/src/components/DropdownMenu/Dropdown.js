import React from 'react';
import './DropdownStyles.css';

const Dropdown = ({ people }) => {
  return (
    <div className="dropdown">
      <div href="#" className="dropbtn">
        Contact
      </div>
      <div className="dropdown-content">
        {people.map((person, index) => {
          return (
            <li key={index}>
              <a href={person.link} target="_blank" rel="noreferrer">
                {person.name}
              </a>
            </li>
          );
        })}
      </div>
    </div>
  );
};

export default Dropdown;
