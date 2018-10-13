var $ = require('jquery');
import ScrollReveal from 'scrollreveal';
import 'magnific-popup';
import 'jquery-easing';

(function () {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 56)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 57
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
      $(".nav-icon").removeClass("icon-white");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
      $(".nav-icon").addClass("icon-white");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Scroll reveal calls
  window.sr = ScrollReveal();

  sr.reveal('.img-colette', {
    delay: 150,
    scale: 0
  });
  sr.reveal('.text-colette', {
    delay: 250,
    scale: 0
  });
  sr.reveal('.img-remy', {
    delay: 250,
    scale: 0
  });
  sr.reveal('.text-remy', {
    delay: 350,
    scale: 0
  });
  sr.reveal('.contact-phone', {
    delay: 100,
    distance: '15px',
    origin: 'bottom',
    scale: 0.8
  });
  sr.reveal('.contact-mail', {
    delay: 200,
    scale: 0
  });

  // Magnific popup calls
  // $('.popup-gallery').magnificPopup({
  //   delegate: 'a',
  //   type: 'image',
  //   tLoading: 'Loading image #%curr%...',
  //   mainClass: 'mfp-img-mobile',
  //   gallery: {
  //     enabled: true,
  //     navigateByImgClick: true,
  //     preload: [0, 1]
  //   },
  //   image: {
  //     tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
  //   }
  // });

})(); // End of use strict
