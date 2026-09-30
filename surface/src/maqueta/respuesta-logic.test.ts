import { describe, expect, it } from "vitest";
import { respuestaProvenance } from "../core/caso";
import type { Atom, Informe, InformeSlotEntry } from "../core/contract";
import {
  checkLargoYCierre,
  checkTeleconsultaAntes,
  countWords,
  estadoLabel,
  frasesConEstado,
  includedIds,
  messageParagraphs,
  nuevosPorSlot,
  orderBases,
  pendientes,
  RULE_CHECKS,
  ruleResults,
  slotAtomIds,
  slotByName,
  type Frase,
} from "./respuesta-logic";

const atom = (id: string, over: Partial<Atom> = {}): Atom => ({
  id,
  gid: `AtomDoc:${id}`,
  path: `docs/atoms/${id}.md`,
  kind: "criterio",
  status: "confirmado",
  source: "FuenteDoc:x",
  source_field: "body",
  start: 0,
  end: 1,
  tags: ["programa.asistente"],
  text: `texto ${id}`,
  quote: "q",
  conf: 1,
  ...over,
});
const atoms = ["p1", "p5", "p7", "f3", "f5", "f4"].map((id) => atom(id));
const P = (id: string) => `docs/atoms/${id}.md`;
const slot = (over: Partial<InformeSlotEntry> = {}): InformeSlotEntry => ({
  name: "respuesta",
  titulo: "Respuesta al paciente",
  rotulo: "",
  atomos: [],
  query: "",
  pins: [],
  excluidos: [],
  modo: "prosa",
  ...over,
});
const informe = (slots: InformeSlotEntry[]): Informe =>
  ({ id: "s", path: "docs/s.md", modelName: "SalidaDoc", slots: {} as never, slotList: slots, payload: {} }) as Informe;
const frase = (texto: string, ids: string[], stale = false): Frase => ({ n: 1, texto, ids, missing: [], stale });

describe("slot de la respuesta", () => {
  it("lista + pins menos excluidos, resueltos a ids, sin repetir", () => {
    const s = slot({ atomos: [P("f3"), P("f5"), P("p1")], pins: [P("f4"), P("f3")], excluidos: [P("f5")] });
    expect(slotAtomIds(s, atoms)).toEqual(["f3", "p1", "f4"]);
    expect(slotAtomIds(undefined, atoms)).toEqual([]);
  });
  it("incluidos: los descartados no cuentan", () => {
    const withDiscard = [...atoms.filter((a) => a.id !== "f3"), atom("f3", { status: "descartado" })];
    expect([...includedIds(slot({ atomos: [P("f3"), P("p1")] }), withDiscard)]).toEqual(["p1"]);
  });
  it("slotByName", () => {
    expect(slotByName(informe([slot(), slot({ name: "otro" })]), "otro")?.name).toBe("otro");
    expect(slotByName(undefined, "x")).toBeUndefined();
  });
  it("párrafos del mensaje", () => {
    expect(messageParagraphs("uno\n\ndos\n\n\n\ntres")).toEqual(["uno", "dos", "tres"]);
  });
});

describe("frases stale", () => {
  const resp = { frases: [{ texto: "A", atomos: ["f3", "p5"] }, { texto: "B", atomos: ["f4"] }, { texto: "C", atomos: ["zz"] }, { texto: "D", atomos: [] }] };
  const prov = respuestaProvenance(resp, atoms);
  it("stale si un átomo salió del slot, no existe o está descartado", () => {
    const fs = frasesConEstado(prov, new Set(["f3", "p5", "f4"]));
    expect(fs.map((f) => f.stale)).toEqual([false, false, true, false]);
    expect(fs[2]!.missing).toEqual(["zz"]);
    expect(frasesConEstado(prov, new Set(["f3", "f4"])).map((f) => f.stale)).toEqual([true, false, true, false]);
  });
});

describe("verificaciones reales", () => {
  it("p5: teleconsulta antes que centros", () => {
    expect(checkTeleconsultaAntes([frase("a", ["f3"]), frase("b", ["f5"])]).ok).toBe(true);
    expect(checkTeleconsultaAntes([frase("a", ["f5"]), frase("b", ["f3"])])).toMatchObject({ ok: false, label: "La teleconsulta tiene que ir antes que los centros" });
    expect(checkTeleconsultaAntes([frase("a", ["f3"])]).ok).toBe(true);
    expect(checkTeleconsultaAntes([frase("a", ["f5"])]).ok).toBe(false);
    expect(checkTeleconsultaAntes([]).ok).toBe(false);
  });
  it("p5 ignora las frases stale", () => {
    expect(checkTeleconsultaAntes([frase("a", ["f3"], true), frase("b", ["f5"])]).ok).toBe(false);
    expect(checkTeleconsultaAntes([frase("a", ["f5"], true), frase("b", ["f3"])]).ok).toBe(true);
  });
  it("p7: menos de 150 palabras y cierra con pregunta", () => {
    const ok = checkLargoYCierre([frase("Hola uno dos.", []), frase("¿Algo más?", [])]);
    expect(ok).toEqual({ ok: true, label: "Largo: 5 palabras (máximo 150); cierra ofreciendo ayuda" });
    expect(checkLargoYCierre([frase("Hola.", [])]).ok).toBe(false);
    expect(checkLargoYCierre([frase("palabra ".repeat(150) + "?", [])]).ok).toBe(false);
    expect(checkLargoYCierre([frase("palabra ".repeat(148) + "?", [])]).ok).toBe(true);
    expect(checkLargoYCierre([]).ok).toBe(false);
    expect(countWords([frase("  a   b\nc ", [])])).toBe(3);
  });
  it("solo p5 y p7 tienen verificación; el resto sale sin ✓", () => {
    expect(Object.keys(RULE_CHECKS).sort()).toEqual(["p5", "p7"]);
    const rs = ruleResults(atoms.filter((a) => a.id.startsWith("p")).map((a) => ({ atom: a })), [frase("¿Hola?", ["f3"])]);
    expect(rs.map((r) => [r.atom.id, r.check === null ? null : r.check.ok])).toEqual([["p1", null], ["p5", true], ["p7", true]]);
    // ids heredados del prototipo no cuentan como verificación
    expect(ruleResults([{ atom: atom("constructor") }], []).map((r) => r.check)).toEqual([null]);
  });
});

describe("antes de enviar", () => {
  it("nuevos por slot: consulta menos lista/pins/excluidos; consulta vacía = nada", () => {
    const inf = informe([
      slot({ name: "a", query: "tag:programa", atomos: [P("p1")], pins: [P("p5")], excluidos: [P("f3")] }),
      slot({ name: "b", query: "" }),
    ]);
    const all = atoms.map((a) => (a.id.startsWith("p") ? a : { ...a, tags: ["programa.red"] }));
    const n = nuevosPorSlot(inf, all);
    expect(n.b).toEqual([]);
    expect(n.a!.sort()).toEqual([P("f4"), P("f5"), P("p7")]);
    expect(nuevosPorSlot(undefined, all)).toEqual({});
  });
  it("Enviar solo sin nuevos ni stale", () => {
    expect(pendientes(0, 0)).toMatchObject({ canSend: true, avisos: [] });
    expect(pendientes(1, 0)).toMatchObject({ canSend: false, avisos: ["1 átomo nuevo sin revisar en el Compositor"] });
    expect(pendientes(0, 1).avisos).toEqual(["1 frase depende de átomos que ya no están"]);
    expect(pendientes(2, 2)).toMatchObject({ canSend: false });
    expect(pendientes(2, 2).avisos).toHaveLength(2);
  });
  it("estado", () => {
    expect(estadoLabel("borrador")).toBe("Borrador, todavía no se envía.");
    expect(estadoLabel("enviada")).toContain("no hay canal de entrega");
  });
});

describe("orden de bases", () => {
  it("por el orden de las fuentes, no por el del slot", () => {
    const paciente = atom("c1", { source: "FuenteDoc:m" });
    const prog = atom("p1", { source: "FuenteDoc:prompt" });
    const bases = [
      { base: "paciente", title: "Paciente", atoms: [{ atom: paciente, frases: [] }] },
      { base: "programa", title: "Programa", atoms: [{ atom: prog, frases: [] }] },
    ];
    expect(orderBases(bases, [{ gid: "FuenteDoc:prompt" }, { gid: "FuenteDoc:m" }]).map((b) => b.base)).toEqual(["programa", "paciente"]);
    expect(orderBases(bases, []).map((b) => b.base)).toEqual(["paciente", "programa"]);
  });
});
