import { render, screen } from '@testing-library/react';
import Register from '../Register';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

describe('Register page', () => {
  it('renders the Register form', () => {
    render(
      <AuthContext.Provider value={{ register: jest.fn() }}>
        <BrowserRouter>
          <Register />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
  });
});
