// news-image-20261118: the entry image is drawn by draw.py and held in this
// repository as entry.png. This program copies it into the output directory
// the grader provides, so both runs write byte-identical files.
// (draw.py runs at build time only; the grader runs this file with no
// network, standard library only, so the image ships in the repo.)
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
const dest = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), dest);

const size = statSync(dest).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
console.log(`wrote ${dest} (${size} bytes)`);
