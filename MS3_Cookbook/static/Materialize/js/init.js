    document.addEventListener('DOMContentLoaded', function() {
      var elems = document.querySelector('.carousel');
      var instance = M.Carousel.init(elems, {
        dist: 0,
        padding: 0,
        fullWidth: true,
        indicators: true,
        duration: 100,
      });
      var desktopCarousel = instance;
});