import React, { useState } from 'react';
import axios from 'axios';

function AssignPromocode() {
  const [user_email, setUserEmail] = useState('');
  const [promocode, setPromocode] = useState('');
  const [message, setMessage] = useState('');

  const token = localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost/api/v1/promocodes/assign/',
        {
          user_email: user_email,
          promocode: promocode,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      setMessage(response.data.message);
    } catch (err) {
      if (err.response) {
        setMessage(err.response.data.detail);
      } else {
        setMessage('Произошла ошибка');
      }
    }
  };

  return (
    <div>
      <h2>Назначение промокода пользователю</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email пользователя:</label>
          <input
            type="text"
            value={user_email}
            onChange={(e) => setUserEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Промокод:</label>
          <input
            type="text"
            value={promocode}
            onChange={(e) => setPromocode(e.target.value)}
            required
          />
        </div>
        <button type="submit">Назначить промокод</button>
      </form>
    </div>
  );
}

export default AssignPromocode;
