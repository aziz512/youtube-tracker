import React from 'react';
import styled from 'styled-components';

const DeleteButton = ({ name, id, isSubscribed, setIsSubscribed }) => {
  const HOST = 'http://127.0.0.1:5000/';

  const handleDeleteRequest = async () => {
    try {
      const resp = await fetch(`${HOST}/watchlist`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id }),
      }).then((res) => {
        console.log(res);
      });
    } catch (e) {
      console.log(e, 'Failed to delete channel');
    }
    setIsSubscribed(false);
  };

  return (
    <Deletebutton onClick={handleDeleteRequest}>
      <span id="x">Unsubscribe</span>
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
