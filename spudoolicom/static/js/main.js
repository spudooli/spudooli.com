(function ($) {
  "use strict";

  $(window).on('load', function () {

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

  });


  $(document).ready(function () {


    /******** Nav menu *******/

    $('ul.sf-menu').superfish({
      animation: {
        height: 'show'
      }, // slide-down effect without fade-in
      delay: 100 // 1.2 second delay on mouseout
    });


    /******** Header two menu button *******/

    $("#mobnav-btn").click(function () {
      $(".sf-menu").slideToggle("slow");
    });

    $('.mobnav-subarrow').click(

      function () {
        $(this).siblings(".sub-menu").toggleClass("sub-menu-open");
      });

    $("#search-label").click(function () {
      $(".search-bar").slideToggle("slow");
    });

    $('.nav-button, .overlay-content-wrap').on('click', function () {
      $('.nav-button').toggleClass("active");
      $('.menu-content').fadeToggle();
      $('.overlay-content-wrap').toggleClass("overlay-active");
      $('body').toggleClass("overflow-hidden-header-three");

      var height = $(window).height();
      $(".menu-content-wrap").css('height', height);

    });
  });



  $(window).resize(function () {

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
/*! instant.page v5.1.0 - (C) 2019-2020 Alexandre Dieulot - https://instant.page/license */
let t, e; const n = new Set, o = document.createElement("link"), i = o.relList && o.relList.supports && o.relList.supports("prefetch") && window.IntersectionObserver && "isIntersecting" in IntersectionObserverEntry.prototype, s = "instantAllowQueryString" in document.body.dataset, a = "instantAllowExternalLinks" in document.body.dataset, r = "instantWhitelist" in document.body.dataset, c = "instantMousedownShortcut" in document.body.dataset, d = 1111; let l = 65, u = !1, f = !1, m = !1; if ("instantIntensity" in document.body.dataset) { const t = document.body.dataset.instantIntensity; if ("mousedown" == t.substr(0, "mousedown".length)) u = !0, "mousedown-only" == t && (f = !0); else if ("viewport" == t.substr(0, "viewport".length)) navigator.connection && (navigator.connection.saveData || navigator.connection.effectiveType && navigator.connection.effectiveType.includes("2g")) || ("viewport" == t ? document.documentElement.clientWidth * document.documentElement.clientHeight < 45e4 && (m = !0) : "viewport-all" == t && (m = !0)); else { const e = parseInt(t); isNaN(e) || (l = e) } } if (i) { const n = { capture: !0, passive: !0 }; if (f || document.addEventListener("touchstart", function (t) { e = performance.now(); const n = t.target.closest("a"); if (!h(n)) return; v(n.href) }, n), u ? c || document.addEventListener("mousedown", function (t) { const e = t.target.closest("a"); if (!h(e)) return; v(e.href) }, n) : document.addEventListener("mouseover", function (n) { if (performance.now() - e < d) return; const o = n.target.closest("a"); if (!h(o)) return; o.addEventListener("mouseout", p, { passive: !0 }), t = setTimeout(() => { v(o.href), t = void 0 }, l) }, n), c && document.addEventListener("mousedown", function (t) { if (performance.now() - e < d) return; const n = t.target.closest("a"); if (t.which > 1 || t.metaKey || t.ctrlKey) return; if (!n) return; n.addEventListener("click", function (t) { 1337 != t.detail && t.preventDefault() }, { capture: !0, passive: !1, once: !0 }); const o = new MouseEvent("click", { view: window, bubbles: !0, cancelable: !1, detail: 1337 }); n.dispatchEvent(o) }, n), m) { let t; (t = window.requestIdleCallback ? t => { requestIdleCallback(t, { timeout: 1500 }) } : t => { t() })(() => { const t = new IntersectionObserver(e => { e.forEach(e => { if (e.isIntersecting) { const n = e.target; t.unobserve(n), v(n.href) } }) }); document.querySelectorAll("a").forEach(e => { h(e) && t.observe(e) }) }) } } function p(e) { e.relatedTarget && e.target.closest("a") == e.relatedTarget.closest("a") || t && (clearTimeout(t), t = void 0) } function h(t) { if (t && t.href && (!r || "instant" in t.dataset) && (a || t.origin == location.origin || "instant" in t.dataset) && ["http:", "https:"].includes(t.protocol) && ("http:" != t.protocol || "https:" != location.protocol) && (s || !t.search || "instant" in t.dataset) && !(t.hash && t.pathname + t.search == location.pathname + location.search || "noInstant" in t.dataset)) return !0 } function v(t) { if (n.has(t)) return; const e = document.createElement("link"); e.rel = "prefetch", e.href = t, document.head.appendChild(e), n.add(t) }


function benchleds(a) {
  benchledsstate = arguments[0];

  // Change the kitchen led state
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/webcam/benchleds", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    onoroff: benchledsstate
  }));
};


function mancavepcleds(a) {
  mancavepcledscolour = arguments[0];

  // Change the mancave led state
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/webcam/mancaveleds", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    mancaveleds: mancavepcledscolour
  }));
};

