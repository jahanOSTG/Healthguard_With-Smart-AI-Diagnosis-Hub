
  document.addEventListener('DOMContentLoaded', function() {
    var myCarousel = document.querySelector('#hospitalCarousel');
    if (myCarousel) {
      var carousel = new bootstrap.Carousel(myCarousel, {
        interval: 2000,  // 2 seconds
        ride: 'carousel', // auto-start
        pause: false     // do not pause on hover
      });
    }
  });

