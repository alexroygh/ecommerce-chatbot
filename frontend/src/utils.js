import * as Yup from 'yup';

export const usernameValidation = Yup.string()
  .required('Username is required')
  .min(3, 'Username must be at least 3 characters')
  .matches(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores');

export const passwordValidation = Yup.string()
  .required('Password is required')
  .min(6, 'Password must be at least 6 characters')
  .matches(/[A-Za-z]/, 'Password must contain at least one letter')
  .matches(/\d/, 'Password must contain at least one digit');

export const loginRegisterSchema = Yup.object().shape({
  username: usernameValidation,
  password: passwordValidation,
}); 