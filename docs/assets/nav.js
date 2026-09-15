/* Méga-menu Neur.on : ouverture au survol et au clic, fermeture par Échap ou clic extérieur,
   navigation au clavier, menu mobile en accordéon. Aucune dépendance. */
(function () {
  var nav = document.getElementById("siteNav");
  if (!nav) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var btns = [].slice.call(nav.querySelectorAll(".nav-btn"));
  var open = null, closeTimer = null, openTimer = null;

  function panelOf(btn) { return document.getElementById(btn.getAttribute("aria-controls")); }

  function show(btn) {
    clearTimeout(closeTimer);
    if (open === btn) return;
    if (open) hide(open, true);
    var p = panelOf(btn);
    if (!p) return;
    p.hidden = false;
    if (reduce) { p.classList.add("on"); }
    else { requestAnimationFrame(function () { requestAnimationFrame(function () { p.classList.add("on"); }); }); }
    btn.setAttribute("aria-expanded", "true");
    open = btn;
  }

  function hide(btn, now) {
    var p = panelOf(btn);
    btn.setAttribute("aria-expanded", "false");
    if (open === btn) open = null;
    if (!p) return;
    p.classList.remove("on");
    if (now || reduce) { p.hidden = true; return; }
    setTimeout(function () { if (!p.classList.contains("on")) p.hidden = true; }, 180);
  }

  function hideAll(now) { btns.forEach(function (b) { if (b.getAttribute("aria-expanded") === "true") hide(b, now); }); }

  btns.forEach(function (btn, i) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      if (btn.getAttribute("aria-expanded") === "true") hide(btn); else show(btn);
    });
    btn.addEventListener("mouseenter", function () {
      clearTimeout(closeTimer);
      openTimer = setTimeout(function () { show(btn); }, open ? 0 : 110);
    });
    btn.addEventListener("mouseleave", function () { clearTimeout(openTimer); scheduleClose(); });
    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault(); show(btn);
        var first = panelOf(btn) && panelOf(btn).querySelector("a:not(.soon)");
        if (first) first.focus();
      } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        e.preventDefault();
        var n = btns[(i + (e.key === "ArrowRight" ? 1 : btns.length - 1)) % btns.length];
        n.focus();
      }
    });
    var p = panelOf(btn);
    if (p) {
      p.addEventListener("mouseenter", function () { clearTimeout(closeTimer); });
      p.addEventListener("mouseleave", scheduleClose);
    }
  });

  function scheduleClose() {
    clearTimeout(closeTimer);
    closeTimer = setTimeout(function () { hideAll(); }, 220);
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && open) { var b = open; hideAll(true); b.focus(); }
  });
  document.addEventListener("click", function (e) {
    if (open && !nav.contains(e.target)) hideAll(true);
  });
  document.addEventListener("focusin", function (e) {
    if (open && !nav.contains(e.target)) hideAll(true);
  });

  /* Menu mobile */
  var burger = document.getElementById("navBurger"), mob = document.getElementById("navMobile");
  if (burger && mob) {
    burger.addEventListener("click", function () {
      var willOpen = burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", willOpen ? "true" : "false");
      burger.setAttribute("aria-label", willOpen ? "Fermer le menu" : "Ouvrir le menu");
      mob.hidden = !willOpen;
      document.body.classList.toggle("nav-open", willOpen);
      if (willOpen) hideAll(true);
    });
    [].forEach.call(mob.querySelectorAll(".nm-head"), function (h) {
      h.addEventListener("click", function () {
        var on = h.getAttribute("aria-expanded") === "true";
        h.setAttribute("aria-expanded", on ? "false" : "true");
        h.nextElementSibling.classList.toggle("on", !on);
      });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 940 && !mob.hidden) {
        mob.hidden = true; burger.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      }
    });
  }
})();
