import React from 'react';
import { Link, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import GeneratePromocode from './GeneratePromocode';
import ValidatePromocode from './ValidatePromocode';
import PromocodeList from './PromocodeList';
import AssignPromocode from './AssignPromocode';

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div>
      <h1>Админка</h1>
      <nav>
        <Link to="/dashboard/generate">Генерация промокода</Link> |{' '}
        <Link to="/dashboard/validate">Валидация промокода</Link> |{' '}
        <Link to="/dashboard/list">Список промокодов</Link> |{' '}
        <Link to="/dashboard/assign">Назначить промокод пользователю</Link> |{' '}
        <button onClick={handleLogout}>Выйти</button>
      </nav>

      <Routes>
        <Route path="/" element={<Navigate to="generate" />} />
        <Route path="generate" element={<GeneratePromocode />} />
        <Route path="validate" element={<ValidatePromocode />} />
        <Route path="list" element={<PromocodeList />} />
        <Route path="assign" element={<AssignPromocode />} />
      </Routes>
    </div>
  );
}

export default Dashboard;
