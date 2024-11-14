gsap.registerPlugin(ScrollTrigger);

// Создаем таймлайн для каждого дома
let tlHouse1 = gsap.timeline({
  scrollTrigger: {
    trigger: ".scene",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});

// Анимация для дома 1
tlHouse1
  .to(".house1", { x: "0px", y: "0px" })
  .to(".house1", { x: "150px", y: "-150px" })
  .to(".house1", { x: "300px", y: "0px" })
  .to(".house1", { x: "150px", y: "150px" })
  .to(".house1", { x: "0px", y: "0px" });
// Анимация для дома 2
let tlHouse2 = gsap.timeline({
  scrollTrigger: {
    trigger: ".scene",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});

tlHouse2
  .to(".house2", { x: "0px", y: "0px" })
  .to(".house2", { x: "150px", y: "150px" })
  .to(".house2", { x: "0px", y: "300px" })
  .to(".house2", { x: "-150px", y: "150px" })
  .to(".house2", { x: "0px", y: "0px" });

// Анимация для дома 3
let tlHouse3 = gsap.timeline({
  scrollTrigger: {
    trigger: ".scene",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});

tlHouse3
  .to(".house3", { x: "0px", y: "0px" })
  .to(".house3", { x: "-150px", y: "150px" })
  .to(".house3", { x: "-300px", y: "0px" })
  .to(".house3", { x: "-150px", y: "-150px" })
  .to(".house3", { x: "0px", y: "0px" });

// Анимация для дома 4
let tlHouse4 = gsap.timeline({
  scrollTrigger: {
    trigger: ".scene",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});

tlHouse4
  .to(".house4", { x: "0px", y: "0px" })
  .to(".house4", { x: "-150px", y: "-150px" })
  .to(".house4", { x: "0px", y: "-300px" })
  .to(".house4", { x: "150px", y: "-150px" })
  .to(".house4", { x: "0px", y: "0px" });

// Анимация перемещения для лупы
let tlMagnifier = gsap.timeline({
  scrollTrigger: {
    trigger: ".scene",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});

tlMagnifier
  .to(".magnifier", { x: "-1350px", y: "-1350px" })
  .to(".magnifier", { x: "210px", y: "-100px" })
  .to(".magnifier", { x: "58px", y: "350px" })
  .to(".magnifier", { x: "-90px", y: "-100px" })
  .to(".magnifier", { x: "60px", y: "53px" });
