// front/src/components/Counter.js
import React, { Component } from "react";

/**
 * Классовый компонент Counter
 *
 * Отслеживает состояние счётчика (count) и предоставляет три метода:
 * - increment: увеличивает счётчик на 1
 * - decrement: уменьшает счётчик на 1
 * - reset: сбрасывает счётчик на 0
 */
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };

    // Привязка методов к текущему экземпляру
    this.increment = this.increment.bind(this);
    this.decrement = this.decrement.bind(this);
    this.reset = this.reset.bind(this);
  }

  // Метод для увеличения счётчика
  increment() {
    this.setState((prevState) => ({ count: prevState.count + 1 }));
  }

  // Метод для уменьшения счётчика
  decrement() {
    this.setState((prevState) => ({ count: prevState.count - 1 }));
  }

  // Метод для сброса счётчика
  reset() {
    this.setState({ count: 0 });
  }

  render() {
    return (
      <div style={styles.componentContainer}>
        <h3>Счётчик: {this.state.count}</h3>
        <button onClick={this.increment} style={styles.button}>
          Увеличить
        </button>
        <button onClick={this.decrement} style={styles.button}>
          Уменьшить
        </button>
        <button onClick={this.reset} style={styles.button}>
          Сбросить
        </button>
      </div>
    );
  }
}

// Стили для компонента (опционально)
const styles = {
  componentContainer: {
    border: "1px solid #ccc",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "5px",
    backgroundColor: "#f1f1f1",
  },
  button: {
    padding: "5px 10px",
    margin: "5px",
    cursor: "pointer",
  },
};

export default Counter;
