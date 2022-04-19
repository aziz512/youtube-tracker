import styled from 'styled-components';
import Home from './components/Home';

const App = () => {
  return (
    <Content>
      <Home></Home>
    </Content>
  );
};

export default App;


const Content = styled.div`
  width: 80%;
  margin: 0 auto;
  padding: 30px 0;
`;