import { describe, expect, it } from "vitest";
import { toMockAtoms } from "./adapter";
import type { Acta, Atom } from "../core/contract";
import { anchorKinds, bodyToPm, caseKinds, defaultKind, fuenteFontClass, fuenteIcon, kindClass, nextAtomId, orderFuentes, highlightRanges, orderAtoms, pmToBody, selectionToBodyRange } from "./extraccion-logic";
import { paragraphsOf } from "../core/atom-text";

const body = "Uno dos tres.\n\nCuatro cinco seis.\n\nSiete.";
// párrafos: [0,13) [15,33) [35,41)
const mk = (id: string, start: number, end: number, quote: string, extra: Partial<Atom> = {}): Atom => ({
  id, gid: `AtomDoc:${id}`, path: `docs/atoms/${id}.md`, kind: "hecho", status: "propuesto", source: "ActaDoc:x", source_field: "body",
  start, end, tags: [], text: quote, quote, conf: 0.9, ...extra,
});
const acta = { body } as Acta;

describe("mapeo body <-> ProseMirror", () => {
  const paras = paragraphsOf(body);
  it("cuenta los saltos que se pierden al dividir", () => {
    expect(paras.map((p) => p.start)).toEqual([0, 15, 35]);
    expect(bodyToPm(paras, 0, "start")).toBe(1);
    expect(bodyToPm(paras, 15, "start")).toBe(16);
    expect(bodyToPm(paras, 35, "start")).toBe(36);
    expect(pmToBody(paras, 16)).toEqual({ offset: 15, para: 1 });
    expect(pmToBody(paras, 36 + 5)).toEqual({ offset: 40, para: 2 });
    expect(pmToBody(paras, 15)).toBeNull(); // entre párrafos
  });
  it("selección: offsets reales, rechaza cruces y vacíos", () => {
    const sel = selectionToBodyRange(body, 16 + 7, 16 + 12); // "cinco"
    expect(sel).toEqual({ ok: true, from: 22, to: 27 });
    if (sel.ok) expect(body.slice(sel.from, sel.to)).toBe("cinco");
    const cross = selectionToBodyRange(body, 10, 20);
    expect(cross.ok).toBe(false);
    expect(!cross.ok && cross.reason).toMatch(/párrafo/);
    expect(selectionToBodyRange(body, 5, 5).ok).toBe(false);
  });
});

describe("subrayados", () => {
  const atoms = toMockAtoms(
    [
      mk("a1", 15, 21, "Cuatro"),
      mk("a2", 0, 3, "Siete"), // movida a 35
      mk("a3", 0, 4, "no existe"), // huérfana
      mk("a4", 15, 33, "Cuatro cinco seis.", { status: "confirmado" }),
    ],
    acta,
  );
  const ranges = highlightRanges(body, atoms);
  it("intacta, movida y huérfana", () => {
    expect(anchorKinds(body, atoms)).toEqual(new Map([["a1", "intact"], ["a2", "drifted"], ["a3", "orphan"], ["a4", "intact"]]));
    expect(ranges.map((r) => r.id)).toEqual(["a1", "a2", "a4"]);
    expect(ranges.find((r) => r.id === "a2")).toMatchObject({ from: 36, to: 41, anchor: "drifted" });
    expect(ranges.find((r) => r.id === "a1")).toMatchObject({ from: 16, to: 22, draft: true, layer: 1 });
    expect(ranges.find((r) => r.id === "a4")).toMatchObject({ draft: false, layer: 0 });
  });
  it("ordena por posición, por confianza y filtra por tipo", () => {
    const low = toMockAtoms([mk("b1", 0, 3, "Uno", { conf: 0.9 }), mk("b2", 15, 21, "Cuatro", { conf: 0.2, kind: "riesgo" })], acta);
    const r = highlightRanges(body, low);
    expect(orderAtoms(low, r, null, false).map((a) => a.id)).toEqual(["b1", "b2"]);
    expect(orderAtoms(low, r, null, true).map((a) => a.id)).toEqual(["b2", "b1"]);
    expect(orderAtoms(low, r, "riesgo", false).map((a) => a.id)).toEqual(["b2"]);
  });
});

describe("tipos, fuentes e ids del caso", () => {
  it("descubre los tipos presentes, completa su familia y los ordena", () => {
    expect(caseKinds(["pregunta", "regla"])).toEqual(["regla", "criterio", "logistica", "paciente", "pregunta"]);
    expect(caseKinds(["riesgo", "hecho"])).toEqual(["hecho", "decision", "riesgo", "entidad", "pendiente"].sort((a, b) => ["entidad", "hecho", "decision", "pendiente", "riesgo"].indexOf(a) - ["entidad", "hecho", "decision", "pendiente", "riesgo"].indexOf(b)));
    expect(caseKinds(["zeta"])).toEqual(["zeta"]);
    expect(caseKinds([])).toEqual([]);
  });
  it("tipo por defecto y clase de color", () => {
    expect(defaultKind(["regla", "hecho"])).toBe("regla");
    expect(defaultKind(["hecho", "riesgo"])).toBe("hecho");
    expect(defaultKind(["zeta"])).toBe("zeta");
    expect(defaultKind([])).toBe("hecho");
    expect(kindClass("regla")).toBe("regla");
    expect(kindClass("zeta")).toBe("otro");
  });
  it("ícono y tipografía por tipo de fuente", () => {
    expect(fuenteIcon("prompt")).toBe("\u2699\uFE0F");
    expect(fuenteIcon("folleto")).toBe("\u{1F4C4}");
    expect(fuenteIcon("mensaje")).toBe("\u{1F4AC}");
    expect(fuenteFontClass("prompt")).toBe("src-prompt");
    expect(fuenteFontClass("mensaje")).toBe("src-paciente");
    expect(fuenteFontClass("folleto")).toBe("");
  });
  it("ids nuevos por prefijo de fuente, sin colisión", () => {
    const ids = ["p1", "p7", "f14", "c9", "a2", "pp3"];
    expect(nextAtomId(ids, "prompt")).toBe("p8");
    expect(nextAtomId(ids, "folleto")).toBe("f15");
    expect(nextAtomId(ids, "mensaje")).toBe("c10");
    expect(nextAtomId(ids, "acta")).toBe("a3");
    expect(nextAtomId([], "prompt")).toBe("p1");
  });
});

it("orderFuentes: prompt, folleto, mensaje; estable con el resto", () => {
  const f = [{ tipo: "mensaje", n: 1 }, { tipo: "acta", n: 2 }, { tipo: "folleto", n: 3 }, { tipo: "prompt", n: 4 }, { tipo: "acta", n: 5 }];
  expect(orderFuentes(f).map((x) => x.n)).toEqual([4, 3, 1, 2, 5]);
});
