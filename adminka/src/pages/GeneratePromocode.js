import React, { useState } from 'react';
import axios from 'axios';

function GeneratePromocode() {
  const [formData, setFormData] = useState({
    discount_percent: 0,
    discount_rubles: 0,
    start_date: '',
    end_date: '',
    usage_limit: null,
    is_active: true,
    is_one_time: true,
  });
  const [generatedCode, setGeneratedCode] = useState(null);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost/api/v1/promocodes/generate/',
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setGeneratedCode(response.data);
      setError('');
    } catch (err) {
      setError('Ошибка при генерации промокода.');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  return (
    <div>
      <h2>Генерация промокода</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {generatedCode ? (
        <div>
          <h3>Промокод сгенерирован:</h3>
          <p>Промокод: {generatedCode.promocode}</p>
          {/* Выводите другие данные по необходимости */}
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div>
            <label>Скидка в процентах:</label>
            <input
              type="number"
              name="discount_percent"
              value={formData.discount_percent}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Скидка в рублях:</label>
            <input
              type="number"
              name="discount_rubles"
              value={formData.discount_rubles}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Дата начала действия:</label>
            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Дата окончания действия:</label>
            <input
              type="date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Лимит использования:</label>
            <input
              type="number"
              name="usage_limit"
              value={formData.usage_limit || ''}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />
              Активен
            </label>
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                name="is_one_time"
                checked={formData.is_one_time}
                onChange={handleChange}
              />
              Одноразовый
            </label>
          </div>
          <button type="submit">Сгенерировать</button>
        </form>
      )}
    </div>
  );
}

export default GeneratePromocode;
