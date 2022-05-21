import React from 'react';
import styled from 'styled-components';

const DeleteButton = ({ handleDeleteRequest }) => {
  return (
    <Deletebutton onClick={handleDeleteRequest}>
      <span>Unsubscribe</span>
    </Deletebutton>
  );
};

export default DeleteButton;

const Deletebutton = styled.div`
  background: #7b7fda;
  color: #fff;
  font-family: 'Helvetica', 'Arial', sans-serif;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  width: fit-content;
  height: 16px;
  border-radius: 5px;
  margin-left: 1em;
  padding: 3px;
  &:hover {
    background-color: red;
    cursor: pointer;
  }
`;
