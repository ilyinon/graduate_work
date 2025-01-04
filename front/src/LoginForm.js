import React, { useState } from 'react';
import axios from 'axios';

function LoginForm({ setToken }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const LOGIN_URL = 'http://localhost/api/v1/auth/login';

    try {
      const response = await axios.post(LOGIN_URL, formData);
      const { access_token } = response.data;
      setToken(access_token);
      alert('Вход выполнен успешно!');
    } catch (error) {
      console.error('Ошибка входа:', error);
      alert('Ошибка входа.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email: <input type="email" name="email" onChange={handleChange} required />
      </label><br />
      <label>
        Password: <input type="password" name="password" onChange={handleChange} required />
      </label><br />
      <button type="submit">Войти</button>
    </form>
  );
}

export default LoginForm;
