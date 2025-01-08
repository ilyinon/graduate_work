import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [email, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost/api/v1/auth/login', {
        email,
        password,
      });
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      navigate('/dashboard');
    } catch (err) {
      setError('Ошибка при входе. Проверьте логин и пароль.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h2>Вход в систему</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Имя пользователя:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Пароль:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
  );
}

export default LoginPage;
