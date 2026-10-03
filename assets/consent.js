/* Bandeau de consentement et Google Analytics 4 (mode « basic » : rien n'est chargé avant l'accord).
   Le choix est gardé dans le navigateur du visiteur ; « Préférences cookies » en pied de page le rouvre. */
(function () {
  var me = document.currentScript;
  var GA = me && me.getAttribute("data-ga4");
  if (!GA) { return; }
  var PRIV = (me && me.getAttribute("data-privacy")) || "https://neur-on.ai/privacy-policy/";
  var KEY = "neuron-consent";
  // textes du bandeau dans la langue de la page (le nom du lien « Préférences cookies » est cité dans chaque politique)
  var TX = {
    fr: {aria: "Cookies de mesure d'audience", txt: "Nous aimerions mesurer la fréquentation du site avec Google Analytics. Aucun cookie de mesure n'est déposé sans votre accord.",
         priv: "Protection des données", non: "Refuser", oui: "Accepter", pref: "Préférences cookies"},
    de: {aria: "Cookies zur Reichweitenmessung", txt: "Wir möchten die Nutzung der Website mit Google Analytics messen. Ohne Ihre Einwilligung wird kein Mess-Cookie gesetzt.",
         priv: "Datenschutz", non: "Ablehnen", oui: "Akzeptieren", pref: "Cookie-Einstellungen"},
    it: {aria: "Cookie di misurazione del pubblico", txt: "Vorremmo misurare la frequentazione del sito con Google Analytics. Nessun cookie di misurazione viene installato senza il vostro consenso.",
         priv: "Protezione dei dati", non: "Rifiutare", oui: "Accettare", pref: "Preferenze cookie"},
    en: {aria: "Analytics cookies", txt: "We would like to measure site traffic with Google Analytics. No analytics cookie is set without your consent.",
         priv: "Privacy policy", non: "Decline", oui: "Accept", pref: "Cookie preferences"}
  };
  var tx = TX[(document.documentElement.lang || "fr").slice(0, 2)] || TX.fr;
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
    b.setAttribute("aria-label", tx.aria);
    b.innerHTML =
      '<p>' + tx.txt + ' <a href="' + PRIV + '">' + tx.priv + '</a></p>' +
      '<div class="ck-btns"><button type="button" class="btn-outline ck-no">' + tx.non + '</button>' +
      '<button type="button" class="btn btn-blue ck-yes">' + tx.oui + '</button></div>';
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
    a.textContent = tx.pref;
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
