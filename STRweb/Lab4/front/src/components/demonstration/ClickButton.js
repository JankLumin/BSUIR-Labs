// front/src/components/ClickButton.js
import React from "react";
import PropTypes from "prop-types";

/**
 * Компонент ClickButton
 *
 * Принимает два свойства (props):
 * - onClick: функция-обработчик клика
 * - label: текст кнопки
 *
 * Если label не передан, используется значение по умолчанию.
 */
const ClickButton = ({ onClick, label }) => {
  return (
    <button onClick={onClick} style={styles.button}>
      {label}
    </button>
  );
};

// Значение по умолчанию для label
ClickButton.defaultProps = {
  label: "Нажми меня",
};

// Проверка типов props
ClickButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  label: PropTypes.string,
};

// Стили для компонента (опционально)
const styles = {
  button: {
    padding: "10px 20px",
    margin: "5px",
    cursor: "pointer",
  },
};

export default ClickButton;
