import { render, screen } from '@testing-library/react';
import Chatbot from '../Chatbot';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

beforeAll(() => {
  window.HTMLElement.prototype.scrollIntoView = jest.fn();
});

describe('Chatbot page', () => {
  it('renders the chat input', () => {
    render(
      <AuthContext.Provider value={{ user: { username: 'test' }, logout: jest.fn() }}>
        <BrowserRouter>
          <Chatbot />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  });
});
