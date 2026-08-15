// AdSense (optional, disabled by default).
// To enable later: get a Google AdSense account, then in config set
// window.BREW_ADS = { pub: "ca-pub-XXXX", slot: "YYYY" } and this will inject the tag.
// Left inert on purpose — a fresh site needs established traffic before AdSense approves.
(function(){
  if (typeof window.BREW_ADS === "undefined" || !window.BREW_ADS.pub) return;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + window.BREW_ADS.pub;
  document.head.appendChild(s);
})();
