document.addEventListener("DOMContentLoaded", () => {
  const timerElement = document.createElement("div");
  timerElement.className = "timer";
  document.body.appendChild(timerElement);

  function startCountdown(endTime) {
    function updateCountdown() {
      const now = Date.now();
      const remainingTime = endTime - now;

      if (remainingTime <= 0) {
        timerElement.textContent = "Время истекло!";
        clearInterval(timerInterval);
        localStorage.removeItem("endTime");
        return;
      }
      const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
      timerElement.textContent = `${hours}ч ${minutes}м ${seconds}с`;
    }

    updateCountdown();
    const timerInterval = setInterval(updateCountdown, 1000);
  }

  let endTime = localStorage.getItem("endTime");

  if (!endTime) {
    // чтобы обновить таймер написать if(endTime)
    endTime = Date.now() + 60 * 60 * 1000;
    localStorage.setItem("endTime", endTime);
  } else {
    endTime = parseInt(endTime);
  }

  startCountdown(endTime);
});
