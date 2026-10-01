/* Bandeau de consentement et Google Analytics 4 (mode « basic » : rien n'est chargé avant l'accord).
   Le choix est gardé dans le navigateur du visiteur ; « Préférences cookies » en pied de page le rouvre. */
(function () {
  var me = document.currentScript;
  var GA = me && me.getAttribute("data-ga4");
  if (!GA) { return; }
  var PRIV = (me && me.getAttribute("data-privacy")) || "https://neur-on.ai/privacy-policy/";
  var KEY = "neuron-consent";
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadGA() {
    if (window.__ga4) { return; }
    window.__ga4 = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA, { anonymize_ip: true });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA);
    document.head.appendChild(s);
  }

  function banner() {
    if (document.getElementById("ckBar")) { return; }
    var b = document.createElement("div");
    b.id = "ckBar";
    b.className = "ck-bar";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookies de mesure d'audience");
    b.innerHTML =
      '<p>Nous aimerions mesurer la fréquentation du site avec Google Analytics. Aucun cookie de mesure n\'est déposé sans votre accord. ' +
      '<a href="' + PRIV + '">Protection des données</a></p>' +
      '<div class="ck-btns"><button type="button" class="btn-outline ck-no">Refuser</button>' +
      '<button type="button" class="btn btn-blue ck-yes">Accepter</button></div>';
    document.body.appendChild(b);
    b.querySelector(".ck-yes").addEventListener("click", function () { set("granted"); b.remove(); loadGA(); });
    b.querySelector(".ck-no").addEventListener("click", function () { set("denied"); b.remove(); });
    b.querySelector(".ck-yes").focus({ preventScroll: true });
  }

  function footerLink() {
    var links = document.querySelector(".footer-bottom .links");
    if (!links || document.getElementById("ckPref")) { return; }
    var a = document.createElement("button");
    a.type = "button";
    a.id = "ckPref";
    a.className = "ck-pref";
    a.textContent = "Préférences cookies";
    a.addEventListener("click", banner);
    links.appendChild(a);
  }

  function start() {
    footerLink();
    var c = get();
    if (c === "granted") { loadGA(); }
    else if (c !== "denied") { banner(); }
  }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", start); } else { start(); }
})();
