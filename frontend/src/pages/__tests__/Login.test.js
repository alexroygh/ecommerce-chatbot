import { render, screen } from '@testing-library/react';
import Login from '../Login';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

describe('Login page', () => {
  it('renders the Login form', () => {
    render(
      <AuthContext.Provider value={{ login: jest.fn() }}>
        <BrowserRouter>
          <Login />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
  });
}); 