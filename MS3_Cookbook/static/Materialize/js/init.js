    document.addEventListener('DOMContentLoaded', function () {
      var elems = document.querySelectorAll('.carousel');
      var instance = M.Carousel.init(elems, {
        dist: 0,
        padding: 0,
        fullWidth: true,
        indicators: true,
        duration: 100,
      });
      var desktopCarousel = instance[1];
      var mobileCarousel = instance[0];


      const FBRM = document.getElementById("btn-right-mob");
      FBRM.addEventListener("click", function () {
        mobileCarousel.next()
      });
      const FBLM = document.getElementById("btn-left-mob");
      FBLM.addEventListener("click", function () {
        mobileCarousel.prev()
      });

      const FBR = document.getElementById("btn-right");
      FBR.addEventListener("click", function () {
        desktopCarousel.next()
      });
      const FBL = document.getElementById("btn-left");
      FBL.addEventListener("click", function () {
        desktopCarousel.prev()
      });
    });