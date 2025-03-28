import './App.css';
import { Container } from '@mui/material';
import MembersList from './components/MembersList';

function App() {
  return (
    <Container
      sx={{ width: '100%' }}
      disableGutters
    >
      <MembersList />
    </Container>
  );
}

export default App;
