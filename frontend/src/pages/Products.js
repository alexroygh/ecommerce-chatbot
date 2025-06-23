import React, { useState, useEffect } from 'react';
import api from '../api';
import { useAuth } from '../context/AuthContext';

export default function Products() {
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchProducts();
    // eslint-disable-next-line
  }, [search, category]);

  const fetchProducts = async () => {
    let url = '/api/products?';
    if (search) url += `search=${encodeURIComponent(search)}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    const res = await api.get(url);
    setProducts(res.data);
    // Extract unique categories
    setCategories([...new Set(res.data.map(p => p.category))]);
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-50">
      <div className="w-full max-w-4xl mt-8 bg-white rounded shadow p-4">
        <h2 className="text-2xl font-bold mb-4">Products</h2>
        <div className="flex gap-2 mb-4">
          <input
            className="border rounded p-2 flex-1"
            placeholder="Search products..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <select
            className="border rounded p-2"
            value={category}
            onChange={e => setCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {products.map(product => (
            <div key={product.id} className="border rounded p-4 flex flex-col items-center bg-gray-100">
              <img src={product.image_url} alt={product.name} className="w-24 h-24 object-cover mb-2 rounded" />
              <div className="font-bold text-lg mb-1">{product.name}</div>
              <div className="text-gray-700 mb-1">{product.category}</div>
              <div className="text-gray-900 font-semibold mb-1">${product.price}</div>
              <div className="text-xs text-gray-500 mb-2">Stock: {product.stock}</div>
              <div className="text-sm text-gray-600 mb-2">{product.description}</div>
              <button className="bg-blue-600 text-white px-4 py-1 rounded mt-2" disabled>Buy (Demo)</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 