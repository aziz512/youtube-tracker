import { useState } from 'react';
import styled from 'styled-components';
import { HOST } from '../common';

const AddChannel = ({ onChannelAdded }) => {
  const [channelUrl, setChannelUrl] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();

    try {
      const resp = await fetch(`${HOST}/watchlist`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: channelUrl }),
      });
      const channelData = await resp.json();
      onChannelAdded(channelData);
      setChannelUrl('');
    } catch (error) {
      setErrorMsg('Invalid channel URL or server unresponsive.');
    }
  };

  const onValueChange = (event) => {
    setChannelUrl(event.target.value);
    setErrorMsg('');
  };

  return (
    <Container>
      <form onSubmit={onSubmit}>
        <Input
          value={channelUrl}
          placeholder="Enter channel url"
          onChange={onValueChange}
          onSubmit={onSubmit}
        />
        <Button type="submit">Add</Button>
        <ErrorMessage>{errorMsg ? errorMsg : undefined}</ErrorMessage>
      </form>
    </Container>
  );
};

export default AddChannel;

const Container = styled.div`
  margin: 0 auto;
  width: fit-content;
`;

const Input = styled.input`
  height: 40px;
  width: 300px;
  box-sizing: border-box;
`;

const Button = styled.button`
  height: 40px;
  width: 90px;
  margin-left: 5px;
  background-color: #764ABD;
  color:white;
`;

const ErrorMessage = styled.span`
  display: block;
  font-size: 14px;
  color: red;
`;
