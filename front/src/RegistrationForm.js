import React, { useState } from 'react';
import axios from 'axios';

function RegistrationForm() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
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

    const SIGNUP_URL = 'http://localhost/api/v1/auth/signup';

    try {
      const response = await axios.post(SIGNUP_URL, formData);
      alert('Регистрация прошла успешно!');
    } catch (error) {
      console.error('Ошибка регистрации:', error);
      alert('Ошибка регистрации.');
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
      <button type="submit">Зарегистрироваться</button>
    </form>
  );
}

export default RegistrationForm;
