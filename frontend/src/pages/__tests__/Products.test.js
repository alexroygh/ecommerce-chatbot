import { render, screen } from '@testing-library/react';
import Products from '../Products';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

describe('Products page', () => {
  it('renders the Products heading', () => {
    render(
      <AuthContext.Provider value={{ user: { username: 'test' } }}>
        <BrowserRouter>
          <Products />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    expect(screen.getByText(/products/i)).toBeInTheDocument();
  });
});
