import React, { useState } from 'react';
import RegistrationForm from './RegistrationForm';
import LoginForm from './LoginForm';
import UsersList from './UsersList';

function App() {
  const [token, setToken] = useState('');

  return (
    <div className="App">
      <h1>Регистрация</h1>
      <RegistrationForm />

      <h1>Вход</h1>
      <LoginForm setToken={setToken} />

      <h1>Пользователи</h1>
      <UsersList token={token} />
    </div>
  );
}

export default App;
