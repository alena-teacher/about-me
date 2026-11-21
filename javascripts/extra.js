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
