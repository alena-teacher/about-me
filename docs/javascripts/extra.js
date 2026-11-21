/* Плавное появление блоков при прокрутке и мелкие улучшения интерфейса */
(function () {
  "use strict";

  // Автоматически подставляем текущий и следующий год в анонс
  var studyYear = document.getElementById("study-year");
  if (studyYear) {
    var year = new Date().getFullYear();
    studyYear.textContent = year + "/" + (year + 1);
  }

  // Актуальный год в копирайте
  var copyright = document.querySelector(".md-copyright__highlight");
  if (copyright) {
    var copyrightYear = new Date().getFullYear();
    copyright.innerHTML = copyright.innerHTML.replace(/©\s*\d{4}/, "© " + copyrightYear);
  }

  // Декоративные формулы слева: не заходим на шапку и футер
  var mathDecor = document.querySelector(".math-decor");
  var pageFooter = document.querySelector(".md-footer");

  function positionMathDecor() {
    if (!mathDecor) return;

    var header = document.querySelector(".md-header");
    var tabs = document.querySelector(".md-tabs");
    var bottom = 0;

    if (header) bottom = Math.max(bottom, header.getBoundingClientRect().bottom);
    if (tabs) bottom = Math.max(bottom, tabs.getBoundingClientRect().bottom);
    if (bottom > 0) mathDecor.style.top = Math.round(bottom + 16) + "px";
  }

  function toggleMathDecor() {
    if (!mathDecor || !pageFooter) return;

    var footerTop = pageFooter.getBoundingClientRect().top;
    mathDecor.classList.toggle("is-hidden", footerTop < window.innerHeight - 24);
  }

  if (mathDecor) {
    var decorTick = false;

    function updateMathDecor() {
      positionMathDecor();
      toggleMathDecor();
    }

    updateMathDecor();
    window.addEventListener("resize", updateMathDecor);
    window.addEventListener(
      "scroll",
      function () {
        if (decorTick) return;
        decorTick = true;
        requestAnimationFrame(function () {
          updateMathDecor();
          decorTick = false;
        });
      },
      { passive: true }
    );
  }

  // Мягкое свечение за курсором: догоняет и растворяется
  var cursorGlow = document.querySelector(".cursor-glow");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var touchDevice = "ontouchstart" in window || navigator.maxTouchPoints > 0;
  var glowReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (cursorGlow && finePointer && !touchDevice && !glowReduced) {
    var glowX = window.innerWidth / 2;
    var glowY = window.innerHeight / 2;
    var glowTargetX = glowX;
    var glowTargetY = glowY;
    var glowVisible = false;
    var glowFrame = 0;
    var glowIdleTimer = 0;
    var glowSnap = true;
    var glowLastTime = 0;

    function renderCursorGlow(time) {
      var dt = glowLastTime ? Math.min((time - glowLastTime) / 1000, 0.05) : 1 / 60;
      var smoothing = 5.5;
      var ease = 1 - Math.exp(-smoothing * dt);
      var dx = glowTargetX - glowX;
      var dy = glowTargetY - glowY;

      glowLastTime = time;
      glowX += dx * ease;
      glowY += dy * ease;
      cursorGlow.style.transform = "translate3d(" + glowX + "px," + glowY + "px,0)";

      if (glowVisible || Math.abs(dx) > 0.4 || Math.abs(dy) > 0.4) {
        glowFrame = requestAnimationFrame(renderCursorGlow);
      } else {
        glowX = glowTargetX;
        glowY = glowTargetY;
        glowFrame = 0;
        glowLastTime = 0;
      }
    }

    function startCursorGlow() {
      if (!glowFrame) glowFrame = requestAnimationFrame(renderCursorGlow);
    }

    function showCursorGlow() {
      if (!glowVisible) {
        cursorGlow.classList.add("is-visible");
        glowVisible = true;
      }
    }

    function hideCursorGlow() {
      cursorGlow.classList.remove("is-visible");
      glowVisible = false;
      startCursorGlow();
    }

    window.addEventListener(
      "pointermove",
      function (event) {
        if (event.pointerType && event.pointerType !== "mouse") return;

        if (glowSnap) {
          glowX = event.clientX;
          glowY = event.clientY;
          glowSnap = false;
        }

        glowTargetX = event.clientX;
        glowTargetY = event.clientY;
        showCursorGlow();
        startCursorGlow();

        clearTimeout(glowIdleTimer);
        glowIdleTimer = setTimeout(hideCursorGlow, 220);
      },
      { passive: true }
    );

    document.addEventListener("mouseleave", function () {
      clearTimeout(glowIdleTimer);
      hideCursorGlow();
      glowSnap = true;
    });

    window.addEventListener("blur", function () {
      clearTimeout(glowIdleTimer);
      hideCursorGlow();
      glowSnap = true;
    });
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealItems = document.querySelectorAll("[data-reveal]");

  if (!reduceMotion && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    revealItems.forEach(function (item) {
      observer.observe(item);
    });
  } else {
    revealItems.forEach(function (item) {
      item.classList.add("is-visible");
    });
  }

  // Плавная прокрутка к якорям внутри страницы
  document.addEventListener("click", function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link) return;

    var id = link.getAttribute("href");
    if (!id || id === "#") return;

    var target = document.querySelector(id);
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({
      behavior: reduceMotion ? "auto" : "smooth",
      block: "start"
    });
    history.pushState(null, "", id);
  });
})();
