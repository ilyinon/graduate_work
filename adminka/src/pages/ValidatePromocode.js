import React, { useState } from 'react';
import axios from 'axios';

function ValidatePromocode() {
  const [promocode, setPromocode] = useState('');
  const [validationResult, setValidationResult] = useState(null);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(
        `http://localhost/api/v1/promocodes/validate/${promocode}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setValidationResult(response.data);
      setError('');
    } catch (err) {
      setError('Промокод недействителен или произошла ошибка.');
    }
  };

  return (
    <div>
      <h2>Валидация промокода</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {validationResult ? (
        <div>
          <h3>Результат валидации:</h3>
          <p>{JSON.stringify(validationResult)}</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div>
            <label>Промокод:</label>
            <input
              type="text"
              value={promocode}
              onChange={(e) => setPromocode(e.target.value)}
              required
            />
          </div>
          <button type="submit">Проверить</button>
        </form>
      )}
    </div>
  );
}

export default ValidatePromocode;
