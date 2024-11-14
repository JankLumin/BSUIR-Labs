// front/src/components/DemonstrationPage.js
import React from "react";
import Dashboard from "./demonstration/Dashboard";

/**
 * Компонент DemonstrationPage
 *
 * Отображает заголовок и компонент Dashboard, содержащий все остальные компоненты с метками.
 */
function DemonstrationPage() {
  return (
    <div style={styles.pageContainer}>
      <h2>Демонстрационная страница</h2>
      <p>На этой странице представлены разные компоненты для демонстрации.</p>
      <Dashboard />
    </div>
  );
}

// Стили для компонента (опционально)
const styles = {
  pageContainer: {
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
};

export default DemonstrationPage;
