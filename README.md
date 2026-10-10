# Baklava math

Baklava pan planning for the pan you actually own. A static site with three calculators:

- **Phyllo plan** - pan dimensions and layers become a sheet-fit verdict and a box count.
- **Nut fill** - pan area becomes chopped-nut grams and melted-butter grams.
- **Syrup and cut** - pan area becomes syrup milliliters with a sugar-water-honey split, and the pan becomes a diamond count.

Live site: https://ilanis-agent.github.io/baklavamath/

## Labeled norms

Labeled kitchen norms from common recipes, not rules:

- Layers: about 40 phyllo sheets per pan, half under the nuts and half over.
- Sheets: a standard store-bought sheet is about 23 x 33 cm; a box holds about 40.
- Nuts: about 0.6 g of chopped nuts per cm2 of pan; butter about 0.25 g per cm2.
- Syrup: about 0.32 ml per cm2 of pan, split roughly 2:1:1 sugar-water-honey by volume.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 36 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 108 checks, 0 failures
```
