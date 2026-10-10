// Baklava math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled kitchen norm, not a rule.
(function (root) {
"use strict";

// Labeled norms (common baklava recipes):
// - Layers: about 40 phyllo sheets per pan, half under the nuts and half over.
// - Sheets: a standard store-bought sheet is about 23 x 33 cm; a box holds about 40 sheets.
// - Nuts: about 0.6 g of chopped nuts per cm2 of pan; butter about 0.25 g per cm2.
// - Syrup: about 0.32 ml per cm2 of pan, split roughly 2:1:1 sugar-water-honey by volume.

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function phylloPlan(panL, panW, layers) {
  if (!positive(panL, panW)) return { error: "pan dimensions must be positive" };
  if (!positive(layers)) return { error: "layer count must be positive" };
  var areaCm2 = r1(panL * panW);
  var fit;
  if (panL <= 23 && panW <= 33 || panW <= 23 && panL <= 33) {
    fit = "fits one labeled 23 x 33 cm sheet per layer";
  } else if (panL <= 33 && panW <= 46 || panW <= 33 && panL <= 46) {
    fit = "needs a patched second sheet on the long side (labeled 23 x 33 cm sheets)";
  } else {
    fit = "bigger than two labeled 23 x 33 cm sheets - expect patchwork seams";
  }
  var boxes = Math.ceil(layers / 40);
  var spare = boxes * 40 - layers;
  return { panL: r1(panL), panW: r1(panW), layers: layers, areaCm2: areaCm2, fit: fit, boxes: boxes, spare: spare };
}

function renderPhyllo(r) {
  if (r.error) return r.error;
  return "A " + r.panL + " x " + r.panW + " cm pan (" + r.areaCm2 + " cm2) " + r.fit + ". " +
    r.layers + " layers is " + r.boxes + " box" + (r.boxes === 1 ? "" : "es") +
    " of labeled 40-sheet phyllo, " + r.spare + " sheet" + (r.spare === 1 ? "" : "s") + " spare.";
}

function nutFill(panL, panW) {
  if (!positive(panL, panW)) return { error: "pan dimensions must be positive" };
  var areaCm2 = panL * panW;
  var nutsG = r1(areaCm2 * 0.6);
  var butterG = r1(areaCm2 * 0.25);
  return { panL: r1(panL), panW: r1(panW), areaCm2: r1(areaCm2), nutsG: nutsG, butterG: butterG };
}

function renderNuts(r) {
  if (r.error) return r.error;
  return "A " + r.panL + " x " + r.panW + " cm pan (" + r.areaCm2 + " cm2) takes about " + r.nutsG +
    " g of chopped nuts and " + r.butterG + " g of melted butter - labeled 0.6 g and 0.25 g per cm2 of pan.";
}

function syrupCut(panL, panW, diamondCm) {
  if (!positive(panL, panW)) return { error: "pan dimensions must be positive" };
  if (!positive(diamondCm)) return { error: "diamond size must be positive" };
  var areaCm2 = panL * panW;
  var syrupMl = r1(areaCm2 * 0.32);
  var sugarMl = r1(syrupMl * 0.5);
  var waterMl = r1(syrupMl * 0.25);
  var honeyMl = r1(syrupMl * 0.25);
  var cols = Math.floor(panL / diamondCm);
  var rows = Math.floor(panW / diamondCm);
  if (cols < 1 || rows < 1) return { error: "diamond size is bigger than the pan" };
  var pieces = cols * rows;
  return { panL: r1(panL), panW: r1(panW), diamondCm: r1(diamondCm), syrupMl: syrupMl,
    sugarMl: sugarMl, waterMl: waterMl, honeyMl: honeyMl, cols: cols, rows: rows, pieces: pieces };
}

function renderSyrup(r) {
  if (r.error) return r.error;
  return "A " + r.panL + " x " + r.panW + " cm pan cuts " + r.cols + " x " + r.rows + " = " + r.pieces +
    " pieces at " + r.diamondCm + " cm, and drinks about " + r.syrupMl + " ml of syrup (" + r.sugarMl +
    " ml sugar, " + r.waterMl + " ml water, " + r.honeyMl + " ml honey) - labeled kitchen estimates.";
}

var api = {
  phylloPlan: phylloPlan,
  nutFill: nutFill,
  syrupCut: syrupCut,
  renderPhyllo: renderPhyllo,
  renderNuts: renderNuts,
  renderSyrup: renderSyrup
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BaklavaMath = api;
})(typeof window !== "undefined" ? window : globalThis);
