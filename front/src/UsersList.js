import React, { useState } from 'react';
import axios from 'axios';

function UsersList({ token }) {
  const [users, setUsers] = useState([]);

  const getUsers = async () => {
    if (!token) {
      alert('Сначала необходимо войти в систему.');
      return;
    }

    const USERS_URL = 'http://localhost/api/v1/users/';

    try {
      const response = await axios.get(USERS_URL, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Ошибка получения пользователей:', error);
      alert('Ошибка получения пользователей.');
    }
  };

  return (
    <div>
      <button onClick={getUsers}>Получить пользователей</button>
      <pre>{JSON.stringify(users, null, 2)}</pre>
    </div>
  );
}

export default UsersList;
