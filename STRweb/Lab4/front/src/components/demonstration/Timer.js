// front/src/components/Timer.js
import React, { useState, useEffect } from "react";

/**
 * Компонент Timer
 *
 * Использует хук useState для отслеживания прошедшего времени в секундах.
 * Хук useEffect устанавливает интервал, который обновляет счётчик каждую секунду.
 */
const Timer = () => {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    // Установка интервала для обновления счётчика каждую секунду
    const interval = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);

    // Очистка интервала при размонтировании компонента
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={styles.componentContainer}>
      <h3>Таймер: {seconds} сек.</h3>
    </div>
  );
};

// Стили для компонента (опционально)
const styles = {
  componentContainer: {
    border: "1px solid #ccc",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "5px",
    backgroundColor: "#f0f0f0",
  },
};

export default Timer;
