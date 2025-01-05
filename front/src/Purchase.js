import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PurchasePage() {
  const [tariffs, setTariffs] = useState([]);
  const [selectedTariff, setSelectedTariff] = useState(null);
  const [promocode, setPromocode] = useState('');
  const [discountedPrice, setDiscountedPrice] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Получаем токен из localStorage
    const token = localStorage.getItem('token');

    // Если токен отсутствует, перенаправляем пользователя на страницу входа
    if (!token) {
      window.location.href = '/login';
      return;
    }

    // Запрашиваем список тарифов
    const fetchTariffs = async () => {
      try {
        const response = await axios.get('http://localhost:9000/api/v1/purchase/tariff', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        setTariffs(response.data.tariffs);
      } catch (error) {
        console.error('Ошибка при получении тарифов:', error);
        setError('Не удалось загрузить тарифы.');
      }
    };

    fetchTariffs();
  }, []);

  const handleTariffSelect = (tariff) => {
    setSelectedTariff(tariff);
    setDiscountedPrice(null); // Сбросим скидку при выборе нового тарифа
    setPromocode(''); // Очистим промокод
    setError('');
  };

  const handlePromocodeApply = async () => {
    if (!promocode) {
      setError('Введите промокод.');
    }

    // Получаем токен из localStorage
    const token = localStorage.getItem('token');

    try {
      const response = await axios.post(
        'http://localhost:9000/api/v1/purchase/checkout',
        {
          tariff_id: selectedTariff.id,
          promocode: promocode,
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      setDiscountedPrice(response.data.amount);
      setError('');
    } catch (error) {
      console.error('Ошибка при применении промокода:', error);
    }
  };

  const handlePurchase = async () => {
    // Получаем токен из localStorage
    const token = localStorage.getItem('token');

    try {
      const response = await axios.post(
        'http://localhost:9000/api/v1/purchase/payment',
        {
          tariff_id: selectedTariff.id,
          promocode: promocode || null,
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      alert('Покупка успешно совершена!');
      // Вы можете перенаправить пользователя или обновить состояние приложения
    } catch (error) {
      console.error('Ошибка при покупке тарифа:', error);
      setError('Не удалось совершить покупку. Попробуйте снова.');
    }
  };

  if (error) {
    return <p>{error}</p>;
  }

  if (tariffs.length === 0) {
    return <p>Загрузка тарифов...</p>;
  }

  return (
    <div>
      <h1>Выберите тариф</h1>
      {!selectedTariff ? (
        <ul>
          {tariffs.map((tariff) => (
            <li key={tariff.id}>
              <h3>{tariff.name}</h3>
              <p>{tariff.description}</p>
              <p>Цена: {tariff.price} руб.</p>
              <button onClick={() => handleTariffSelect(tariff)}>Выбрать</button>
            </li>
          ))}
        </ul>
      ) : (
        <div>
          <h2>Вы выбрали тариф: {selectedTariff.name}</h2>
          <p>{selectedTariff.description}</p>
          <p>
            Цена: {discountedPrice !== null ? discountedPrice : selectedTariff.price} руб.
          </p>

          <div>
            <label>
              Промокод:
              <input
                type="text"
                value={promocode}
                onChange={(e) => setPromocode(e.target.value)}
              />
            </label>
            <button onClick={handlePromocodeApply}>Применить</button>
          </div>

          {error && <p style={{ color: 'red' }}>{error}</p>}

          <button onClick={handlePurchase}>Купить</button>
          <button onClick={() => setSelectedTariff(null)}>Вернуться к списку тарифов</button>
        </div>
      )}
    </div>
  );
}

export default PurchasePage;