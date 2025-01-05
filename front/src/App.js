import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RegistrationForm from './RegistrationForm';
import LoginForm from './LoginForm';
import Menu from './Menu';
import UserInfo from './UserInfo';
import Purchase from './Purchase';

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '');

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const isLoggedIn = !!token;

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    alert('Вы вышли из системы');
  };

  return (
    <Router>
      <div className="App">
        <Menu isLoggedIn={isLoggedIn} handleLogout={handleLogout} />

        <Routes>
          <Route path="/" element={<h1>Главная страница</h1>} />

          {!isLoggedIn && (
            <>
              <Route
                path="/register"
                element={
                  <>
                    <h1>Регистрация</h1>
                    <RegistrationForm />
                  </>
                }
              />
              <Route
                path="/login"
                element={
                  <>
                    <h1>Вход</h1>
                    <LoginForm setToken={setToken} />
                  </>
                }
              />
            </>
          )}

          {isLoggedIn && (
            <>
              <Route path="/profile" element={<UserInfo />} />
              <Route path="/checkout" element={<Purchase />} />

            </>
          )}

          <Route path="*" element={<h1>Страница не найдена</h1>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;