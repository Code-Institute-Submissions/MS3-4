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

const FBR = document.getElementById("btn-right");
FBR.addEventListener("click", function(){ instance.next()});
const FBL = document.getElementById("btn-left");
FBL.addEventListener("click", function(){ instance.prev()});
});