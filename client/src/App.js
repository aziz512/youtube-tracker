import { useEffect } from 'react';
import styled from 'styled-components';

const Title = styled.div`
  font-size: 1.5em;
  text-align: center;
  color: navy;
`;

const App = () => {
  useEffect(() => {
    console.log('some log');
  }, []);

  return (
    <div className="App">
      <Title>Hello World!</Title>
    </div>
  );
};

export default App;
