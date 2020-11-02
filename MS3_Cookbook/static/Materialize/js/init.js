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

      const FBR = document.getElementById("btn-right");
      if (FBR != null) {
        FBR.addEventListener("click", function () {
          desktopCarousel.next()
        });
      }
      const FBL = document.getElementById("btn-left");
      if (FBL != null) {

        FBL.addEventListener("click", function () {
          desktopCarousel.prev()
        });

      }

      var elem = document.querySelectorAll('.sidenav');
      var instances = M.Sidenav.init(elem, {});

      let tabsEl = document.getElementById("login-tabs");
      var tabs = M.Tabs.init(tabsEl, {});


      var el = document.getElementById('user-dropdown-trigger');
      var instancess = M.Dropdown.init(el, {});

    });