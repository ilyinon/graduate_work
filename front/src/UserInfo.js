import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserInfo() {
  const [users, setUserInfo] = useState(null);
  useEffect(() => {

    const token = localStorage.getItem('token');

    // Если токен отсутствует, перенаправляем пользователя на страницу входа
    if (!token) {
      window.location.href = '/login';
      return;
    }
    
    const fetchUserInfo = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost/api/v1/users/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setUserInfo(response.data);
      } catch (error) {
        console.error('Ошибка при получении информации о пользователе:', error);
      }
    };

    fetchUserInfo();
  }, []);


  return (
    <div>
      <pre>{JSON.stringify(users, null, 2)}</pre>
    </div>
  );
}

export default UserInfo;
