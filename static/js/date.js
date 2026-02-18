(function () {
  function getHicri() {
    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();
    if (month < 2) { year--; month += 12; }
    var a = Math.floor(year / 100);
    var b = 2 - a + Math.floor(a / 4);
    var jd = Math.floor(365.25 * (year + 4716)) + Math.floor(30.6001 * (month + 2)) + day + b - 1524.5;
    var z = Math.floor(jd + 0.5);
    var cyc = Math.floor((z - 1948439.5) / 10631);
    var l = z - 1948439.5 - cyc * 10631;
    var j = Math.floor((l - 1) / 354.36667);
    var m = l - Math.floor(j * 354.36667 + 0.5);
    var hicriYil = cyc * 30 + j + 1;
    var hicriAyIdx = Math.floor((m - 1) / 29.5);
    var hicriGun = Math.floor(m - Math.floor(hicriAyIdx * 29.5 + 0.5));
    var aylar = ["Muharrem", "Safer", "Rebiülevvel", "Rebiülahır", "Cemaziyelevvel", "Cemaziyelahır", "Recep", "Şaban", "Ramazan", "Şevval", "Zilkade", "Zilhicce"];
    return hicriGun + " " + aylar[hicriAyIdx] + " " + hicriYil;
  }

  function yazdir() {
    var miladiEl = document.getElementById('txt-miladi');
    var hicriEl = document.getElementById('txt-hicri');
    if (miladiEl && hicriEl) {
      var simdi = new Date();
      var mOptions = { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' };
      miladiEl.innerText = simdi.toLocaleDateString('tr-TR', mOptions);
      hicriEl.innerText = getHicri();
    }
  }

  // DOM yüklendiğinde çalıştır
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", yazdir);
  } else {
    yazdir();
  }
})();

