// BrewLab calculators — all run client-side, no upload.
function num(id){ var v = parseFloat(document.getElementById(id).value); return isNaN(v) ? null : v; }

function solveRatio(){
  var c = num('r-coffee'), w = num('r-water'), r = num('r-ratio');
  var out = document.getElementById('r-out');
  var filled = [c!==null, w!==null, r!==null].filter(Boolean).length;
  if(filled < 2){ out.textContent = 'Fill any two fields to solve the third.'; return; }
  if(c!==null && r!==null && w===null){
    w = c * r; out.textContent = c + ' g coffee × ' + r + ' = ' + Math.round(w) + ' ml water.';
  } else if(w!==null && r!==null && c===null){
    c = w / r; out.textContent = Math.round(w) + ' ml water ÷ ' + r + ' = ' + c.toFixed(1) + ' g coffee.';
  } else if(c!==null && w!==null && r===null){
    r = w / c; out.textContent = Math.round(w) + ' ml ÷ ' + c + ' g = 1:' + r.toFixed(1) + ' ratio.';
  } else {
    out.textContent = 'Recipe: ' + c + ' g coffee, ' + Math.round(w) + ' ml water → 1:' + (w/c).toFixed(1) + '.';
  }
}

function solveCost(){
  var price = num('c-price'), weight = num('c-weight'), dose = num('c-dose'), day = num('c-day');
  var out = document.getElementById('c-out');
  if(price===null || weight===null || dose===null || day===null){
    out.textContent = 'Fill all four fields.'; return;
  }
  var cupsPerBag = weight / dose;
  var perCup = price / cupsPerBag;
  var month = perCup * day * 30;
  out.textContent = '≈ $' + perCup.toFixed(2) + ' per cup · about $' + month.toFixed(0) + '/month at ' + day + ' cup' + (day===1?'':'s') + '/day.';
}

function solveColdBrew(){
  var c = num('cb-coffee'), w = num('cb-water'), r = num('cb-ratio');
  var out = document.getElementById('cb-out');
  var filled = [c!==null, w!==null, r!==null].filter(Boolean).length;
  if(filled < 2){ out.textContent = 'Fill any two fields to solve the third.'; return; }
  if(c!==null && r!==null && w===null){
    w = c * r; out.textContent = c + ' g coffee + ' + Math.round(w) + ' ml water = 1:' + r + ' concentrate. Dilute 1:1 → ~' + (w*2/200).toFixed(1) + ' cups.';
  } else if(w!==null && r!==null && c===null){
    c = w / r; out.textContent = c.toFixed(1) + ' g coffee + ' + Math.round(w) + ' ml water = 1:' + r + ' concentrate. Dilute 1:1 → ~' + (w*2/200).toFixed(1) + ' cups.';
  } else if(c!==null && w!==null && r===null){
    r = (w / c).toFixed(1); out.textContent = c + ' g coffee + ' + Math.round(w) + ' ml water = 1:' + r + ' concentrate. Dilute 1:1 → ~' + (w*2/200).toFixed(1) + ' cups.';
  } else {
    out.textContent = 'Concentrate: ' + c + ' g coffee + ' + Math.round(w) + ' ml water (1:' + (w/c).toFixed(1) + '). Dilute 1:1 → ~' + (w*2/200).toFixed(1) + ' cups.';
  }
}
