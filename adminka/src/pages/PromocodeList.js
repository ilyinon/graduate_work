import React, { useEffect, useState } from 'react';
import axios from 'axios';

function PromocodeList() {
  const [promocodes, setPromocodes] = useState([]);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchPromocodes = async () => {
      try {
        const response = await axios.get('http://localhost/api/v1/promocodes/list/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setPromocodes(response.data);
      } catch (err) {
        setError('Ошибка при получении списка промокодов.');
      }
    };

    fetchPromocodes();
  }, [token]);

  return (
    <div>
      <h2>Список промокодов</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {promocodes.length > 0 ? (
        <table border="1">
          <thead>
            <tr>
              <th>ID</th>
              <th>Промокод</th>
              <th>Скидка (%)</th>
              <th>Скидка (руб.)</th>
              <th>Активен</th>
              <th>Одноразовый</th>
              <th>Использовано</th>
              <th>Лимит</th>
            </tr>
          </thead>
          <tbody>
            {promocodes.map((code) => (
              <tr key={code.id}>
                <td>{code.id}</td>
                <td>{code.promocode}</td>
                <td>{code.discount_percent}</td>
                <td>{code.discount_rubles}</td>
                <td>{code.is_active ? 'Да' : 'Нет'}</td>
                <td>{code.is_one_time ? 'Да' : 'Нет'}</td>
                <td>{code.used_count}</td>
                <td>{code.usage_limit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Нет доступных промокодов.</p>
      )}
    </div>
  );
}

export default PromocodeList;
