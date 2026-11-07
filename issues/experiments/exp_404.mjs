// Two classic <script>s in one realm: a foreign `const port` + miminet's sloppy write.
import vm from "node:vm";
const ctx = vm.createContext({});
vm.runInContext("const port = 'injected-by-other-script';", ctx);
const miminet = (decl) => `function l2SwitchPortUid(){ for (let n=1;n<3;n++){ ${decl}port = 'sw_' + n; return port; } } l2SwitchPortUid();`;
try { console.log("as in main:", vm.runInContext(miminet(""), ctx)); } catch (e) { console.log("as in main:", e.constructor.name, e.message); }
console.log("with let:  ", vm.runInContext(miminet("let "), ctx));
