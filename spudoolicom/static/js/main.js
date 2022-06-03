 (function($) {
   "use strict"; // Start of use strict

   /* ---------------------------------------------
    Scripts initialization
    --------------------------------------------- */

   $(window).load(function() {

    //  /******** Page loader *******/
    //  $(".page-loader div").fadeOut();
    //  $(".page-loader").delay(200).fadeOut("slow");


     /******** fractionSlider *******/

    //  $('.fr-slider').fractionSlider({
    //    'fullWidth': true,
    //    'slideTransition': 'fade',
    //    'slideTransitionSpeed': 650,
    //    'slideEndAnimation': false,
    //    'controls': false,
    //    'pager': true,
    //    'speedOut': 2600,
    //    'timeout': 6000,
    //    'responsive': true,
    //    'increase': true,
    //    'dimensions': '1170 , 600',
    //  });

     var viewportWidth = $(window).width();
     var colWidth = $(".fraction-slider").width();
     var viewportHeight = $(window).height();
     var divideval = 2;
     var marginslidebg = (viewportWidth - colWidth) / divideval + 2;

     $(".slide-bg").css({
       "width": viewportWidth,
       "max-width": viewportWidth,
       "margin-left": "-" + marginslidebg + "px",
     });

    //  $(window).resize(function() {
    //    /******** fractionSlider bg image resize *******/
    //    $(".slide-bg").css({
    //      "width": viewportWidth,
    //      "max-width": viewportWidth,
    //      "margin-left": "-" + marginslidebg + "px",
    //    });

    //  });

     
    
   });


   $(document).ready(function() {


     /******** Nav menu *******/

     $('ul.sf-menu').superfish({
       animation: {
         height: 'show'
       }, // slide-down effect without fade-in
       delay: 100 // 1.2 second delay on mouseout
     });


     /******** Header two menu button *******/

     $("#mobnav-btn").click(function() {
       $(".sf-menu").slideToggle("slow");
     });

     $('.mobnav-subarrow').click(

       function() {
         $(this).siblings(".sub-menu").toggleClass("sub-menu-open");
       });

     $("#search-label").click(function() {
       $(".search-bar").slideToggle("slow");
     });

     $('.nav-button, .overlay-content-wrap').on('click', function() {
       $('.nav-button').toggleClass("active");
       $('.menu-content').fadeToggle();
       $('.overlay-content-wrap').toggleClass("overlay-active");
       $('body').toggleClass("overflow-hidden-header-three");

       var height = $(window).height();
       $(".menu-content-wrap").css('height', height);

     });
   });



   $(window).resize(function() {

     /******** Header size *******/
     var conterner_width = $('.inner-conterner').width();
     $('.header-inner').css({
       "width": conterner_width,
     });

   });



   /********  wow.js *******/
   var wow = new WOW({
     boxClass: 'wow', // animated element css class (default is wow)
     animateClass: 'animated', // animation css class (default is animated)
     offset: 50, // distance to the element when triggering the animation (default is 0) 
     mobile: false
   });
   wow.init();



 })(jQuery)
