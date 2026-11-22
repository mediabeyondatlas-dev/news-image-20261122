// news-image-20261122 — entry program (Node 22, standard library only).
//
// The entry image is the entry.png shipped beside this file: a one-day
// world-news infographic for Sunday 22 November 2026, drawn with Pillow
// by draw.py (also in this repo). This program just places that exact file
// at /output/entry.png so the gate reads it. No network, no randomness,
// no writes anywhere else — two runs produce byte-identical output.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
