// Find writes to identifiers that are not declared anywhere (implicit globals)
// across a set of classic <script> files sharing one global scope.
import fs from "node:fs";
import path from "node:path";
import * as espree from "espree";
import * as eslintScope from "eslint-scope";

const files = process.argv.slice(2);
const declared = new Set();
const writes = [];

for (const f of files) {
  const code = fs.readFileSync(f, "utf8");
  let ast;
  try {
    ast = espree.parse(code, { ecmaVersion: "latest", sourceType: "script", loc: true, range: true });
  } catch (e) {
    console.error(`PARSE FAIL ${f}: ${e.message}`);
    continue;
  }
  const sm = eslintScope.analyze(ast, { ecmaVersion: 2022, sourceType: "script" });
  const g = sm.globalScope;
  for (const v of g.variables) declared.add(v.name);
  for (const ref of g.through) {
    if (ref.isWrite()) {
      writes.push({ file: path.basename(f), name: ref.identifier.name, line: ref.identifier.loc.start.line });
    }
  }
}

const implicit = writes.filter((w) => !declared.has(w.name));
const byName = {};
for (const w of implicit) (byName[w.name] ??= []).push(`${w.file}:${w.line}`);
for (const [name, locs] of Object.entries(byName).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`${name}\t${locs.length}\t${locs.slice(0, 6).join(", ")}${locs.length > 6 ? " ..." : ""}`);
}
console.log(`TOTAL implicit-global writes: ${implicit.length}, distinct names: ${Object.keys(byName).length}`);
