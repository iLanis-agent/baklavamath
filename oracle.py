#!/usr/bin/env python3
"""Independent oracle for Baklava math. Mirrors engine.js float ops exactly."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def phyllo_plan(pan_l, pan_w, layers):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (pan_l, pan_w)):
        return {"error": "pan dimensions must be positive"}
    if not (isinstance(layers, (int, float)) and math.isfinite(layers) and layers > 0):
        return {"error": "layer count must be positive"}
    area_cm2 = r1(pan_l * pan_w)
    if pan_l <= 23 and pan_w <= 33 or pan_w <= 23 and pan_l <= 33:
        fit = "fits one labeled 23 x 33 cm sheet per layer"
    elif pan_l <= 33 and pan_w <= 46 or pan_w <= 33 and pan_l <= 46:
        fit = "needs a patched second sheet on the long side (labeled 23 x 33 cm sheets)"
    else:
        fit = "bigger than two labeled 23 x 33 cm sheets - expect patchwork seams"
    boxes = math.ceil(layers / 40)
    spare = boxes * 40 - layers
    return {"panL": r1(pan_l), "panW": r1(pan_w), "layers": layers, "areaCm2": area_cm2,
            "fit": fit, "boxes": boxes, "spare": spare}

def render_phyllo(r):
    if "error" in r: return r["error"]
    bs = "" if r["boxes"] == 1 else "es"
    ss = "" if r["spare"] == 1 else "s"
    return (f"A {num(r['panL'])} x {num(r['panW'])} cm pan ({num(r['areaCm2'])} cm2) {r['fit']}. "
            f"{r['layers']} layers is {r['boxes']} box{bs} of labeled 40-sheet phyllo, {r['spare']} sheet{ss} spare.")

def nut_fill(pan_l, pan_w):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (pan_l, pan_w)):
        return {"error": "pan dimensions must be positive"}
    area_cm2 = pan_l * pan_w
    return {"panL": r1(pan_l), "panW": r1(pan_w), "areaCm2": r1(area_cm2),
            "nutsG": r1(area_cm2 * 0.6), "butterG": r1(area_cm2 * 0.25)}

def render_nuts(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['panL'])} x {num(r['panW'])} cm pan ({num(r['areaCm2'])} cm2) takes about {num(r['nutsG'])}"
            f" g of chopped nuts and {num(r['butterG'])} g of melted butter - labeled 0.6 g and 0.25 g per cm2 of pan.")

def syrup_cut(pan_l, pan_w, diamond_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (pan_l, pan_w)):
        return {"error": "pan dimensions must be positive"}
    if not (isinstance(diamond_cm, (int, float)) and math.isfinite(diamond_cm) and diamond_cm > 0):
        return {"error": "diamond size must be positive"}
    area_cm2 = pan_l * pan_w
    syrup_ml = r1(area_cm2 * 0.32)
    sugar_ml = r1(syrup_ml * 0.5)
    water_ml = r1(syrup_ml * 0.25)
    honey_ml = r1(syrup_ml * 0.25)
    cols = math.floor(pan_l / diamond_cm)
    rows = math.floor(pan_w / diamond_cm)
    if cols < 1 or rows < 1:
        return {"error": "diamond size is bigger than the pan"}
    pieces = cols * rows
    return {"panL": r1(pan_l), "panW": r1(pan_w), "diamondCm": r1(diamond_cm), "syrupMl": syrup_ml,
            "sugarMl": sugar_ml, "waterMl": water_ml, "honeyMl": honey_ml,
            "cols": cols, "rows": rows, "pieces": pieces}

def render_syrup(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['panL'])} x {num(r['panW'])} cm pan cuts {r['cols']} x {r['rows']} = {r['pieces']}"
            f" pieces at {num(r['diamondCm'])} cm, and drinks about {num(r['syrupMl'])} ml of syrup ({num(r['sugarMl'])}"
            f" ml sugar, {num(r['waterMl'])} ml water, {num(r['honeyMl'])} ml honey) - labeled kitchen estimates.")

cases = []
for l, w, ly in [(23, 33, 40), (20, 30, 40), (30, 40, 40), (33, 46, 40), (40, 60, 40),
                 (23, 33, 20), (23, 33, 41), (15, 20, 80), (22.5, 32.5, 40), (0, 33, 40),
                 (23, -5, 40), (23, 33, 0), (33, 45.9, 10), (23.1, 33, 40)]:
    res = phyllo_plan(l, w, ly)
    cases.append({"fn": "phylloPlan", "args": [l, w, ly], "result": res, "render": render_phyllo(res)})
for l, w in [(23, 33), (20, 30), (30, 40), (15, 20), (25, 35), (0, 33), (23, -5),
             (18.5, 26.5), (40, 60), (12, 12)]:
    res = nut_fill(l, w)
    cases.append({"fn": "nutFill", "args": [l, w], "result": res, "render": render_nuts(res)})
for l, w, d in [(23, 33, 5), (20, 30, 5), (30, 40, 6), (23, 33, 4), (15, 20, 3), (40, 60, 8),
                (23, 33, 25), (10, 10, 12), (0, 33, 5), (23, 33, 0), (23, -5, 5), (18.5, 26.5, 4.5)]:
    res = syrup_cut(l, w, d)
    cases.append({"fn": "syrupCut", "args": [l, w, d], "result": res, "render": render_syrup(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
