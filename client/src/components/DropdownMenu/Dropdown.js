import React from 'react';
import './DropdownStyles.css';

const Dropdown = ({ people }) => {
  return (
    <div class="dropdown">
      <div href="#" class="dropbtn">
        Contact
      </div>
      <div class="dropdown-content">
        {people.map((person) => {
          return (
            <li>
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
