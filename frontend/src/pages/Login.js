import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';
import { Formik, Form, Field } from 'formik';
import { toast } from 'react-toastify';
import { loginRegisterSchema } from '../utils';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Formik
        initialValues={{ username: '', password: '' }}
        validationSchema={loginRegisterSchema}
        validateOnBlur={true}
        validateOnChange={true}
        onSubmit={async (values, { setSubmitting }) => {
          try {
            const res = await api.post('/api/auth/login', values);
            login(res.data.access_token);
            navigate('/chat');
          } catch (err) {
            toast.error(err.response?.data?.msg || 'Login failed');
          }
          setSubmitting(false);
        }}
      >
        {({ isSubmitting, errors, touched }) => (
          <Form className="bg-white p-8 rounded shadow-md w-full max-w-sm">
            <h2 className="text-2xl font-bold mb-4">Login</h2>
            <Field
              className="w-full p-2 mb-1 border rounded"
              name="username"
              placeholder="Username"
              autoComplete="username"
            />
            {touched.username && errors.username && (
              <div className="text-red-500 text-sm mb-2">{errors.username}</div>
            )}
            <Field
              className="w-full p-2 mb-1 border rounded"
              name="password"
              type="password"
              placeholder="Password"
              autoComplete="current-password"
            />
            {touched.password && errors.password && (
              <div className="text-red-500 text-sm mb-4">{errors.password}</div>
            )}
            <button
              className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
            <div className="mt-4 text-center">
              <Link to="/register" className="text-blue-600 hover:underline">
                Register
              </Link>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}
