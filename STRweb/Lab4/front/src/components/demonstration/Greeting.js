// front/src/components/Greeting.js
import React from "react";
import PropTypes from "prop-types";

/**
 * Компонент Greeting
 *
 * Принимает два свойства (props):
 * - name: имя пользователя
 * - age: возраст пользователя
 *
 * Если свойства не переданы, используются значения по умолчанию.
 */
function Greeting({ name, age }) {
  return (
    <div style={styles.componentContainer}>
      <h3>Привет, {name}!</h3>
      <p>Тебе {age} лет.</p>
    </div>
  );
}

// Значения по умолчанию для props
Greeting.defaultProps = {
  name: "Гость",
  age: "неизвестно",
};

// Проверка типов props
Greeting.propTypes = {
  name: PropTypes.string,
  age: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

// Стили для компонента (опционально)
const styles = {
  componentContainer: {
    border: "1px solid #ccc",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "5px",
    backgroundColor: "#f9f9f9",
  },
};

export default Greeting;