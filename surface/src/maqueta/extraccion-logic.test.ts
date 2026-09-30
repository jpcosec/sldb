import { describe, expect, it } from "vitest";
import { toMockAtoms } from "./adapter";
import type { Acta, Atom } from "../core/contract";
import { anchorKinds, bodyToPm, highlightRanges, orderAtoms, pmToBody, selectionToBodyRange } from "./extraccion-logic";
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
