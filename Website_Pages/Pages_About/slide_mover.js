
document.addEventListener("DOMContentLoaded", () => {
  const sliders = document.querySelectorAll(".slides");
  sliders.forEach(slideContainer => {
    const slides = slideContainer.querySelectorAll(".slide");
    let index = 0;

    setInterval(() => {
      slides[index].classList.remove("active");
      index = (index + 1) % slides.length;
      slides[index].classList.add("active");
    }, 10000); // Change slide every 10 seconds
  });
});
