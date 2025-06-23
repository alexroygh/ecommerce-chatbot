import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import { Formik, Form, Field } from 'formik';
import { toast } from 'react-toastify';
import { loginRegisterSchema } from '../utils';

export default function Register() {
  const [success, setSuccess] = React.useState('');
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Formik
        initialValues={{ username: '', password: '' }}
        validationSchema={loginRegisterSchema}
        validateOnBlur={true}
        validateOnChange={true}
        onSubmit={async (values, { setSubmitting, resetForm }) => {
          setSuccess('');
          try {
            await api.post('/api/auth/register', values);
            setSuccess('Registration successful! Redirecting to login...');
            setTimeout(() => navigate('/login'), 1500);
            resetForm();
          } catch (err) {
            toast.error(err.response?.data?.msg || 'Registration failed');
          }
          setSubmitting(false);
        }}
      >
        {({ isSubmitting, errors, touched }) => (
          <Form className="bg-white p-8 rounded shadow-md w-full max-w-sm">
            <h2 className="text-2xl font-bold mb-4">Register</h2>
            {success && <div className="text-green-600 mb-2">{success}</div>}
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
              autoComplete="new-password"
            />
            {touched.password && errors.password && (
              <div className="text-red-500 text-sm mb-4">{errors.password}</div>
            )}
            <button
              className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Registering...' : 'Register'}
            </button>
            <div className="mt-4 text-center">
              <Link to="/login" className="text-blue-600 hover:underline">
                Login
              </Link>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}
