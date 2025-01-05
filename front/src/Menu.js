import React from 'react';
import { Link } from 'react-router-dom';

function Menu({ isLoggedIn, handleLogout }) {
  return (
    <nav>
      <ul>
        <li><Link to="/">Главная</Link></li>
        {!isLoggedIn && (
          <>
            <li><Link to="/register">Регистрация</Link></li>
            <li><Link to="/login">Вход</Link></li>
          </>
        )}
        {isLoggedIn && (
          <>
            <li><Link to="/profile">Профиль</Link></li>
            <li><Link to="/checkout">Покупка</Link></li>
            <li><button onClick={handleLogout}>Выйти</button></li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Menu;