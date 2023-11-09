// Добавляем интерактивность: форма будет "следить" за курсором мыши
document.addEventListener('mousemove', function(e) {
  let xAxis = (window.innerWidth / 2 - e.pageX) / 25;
  let yAxis = (window.innerHeight / 2 - e.pageY) / 25;
  document.querySelector('form').style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
});
