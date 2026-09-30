import { describe, expect, it } from "vitest";
import fixture from "../core/__fixtures__/atoms.json";
import { atomsFromDocuments, informesFromDocuments } from "../core/atoms";
import type { GraphDocument, InformeSlot } from "../core/contract";
import { addQueryFilter, filterChips, isIncluded, newBySlot, newPaths, slotItems } from "./compositor-logic";

const docs = fixture.documents as unknown as GraphDocument[];
const atoms = atomsFromDocuments(docs);
const slot = (p: Partial<InformeSlot>): InformeSlot => ({ atomos: [], query: "", pins: [], excluidos: [], modo: "viñetas", ...p });
const A = (n: number) => `docs/atoms/a${n}.md`;

describe("newPaths", () => {
  it("trae lo que calza con la consulta y no está en lista, pins ni excluidos", () => {
    expect(newPaths(slot({ query: "tipo:hecho" }), atoms)).toEqual([A(3)]);
    expect(newPaths(slot({ query: "tipo:hecho", atomos: [A(3)] }), atoms)).toEqual([]);
    expect(newPaths(slot({ query: "tipo:hecho", pins: [A(3)] }), atoms)).toEqual([]);
    expect(newPaths(slot({ query: "tipo:hecho", excluidos: [A(3)] }), atoms)).toEqual([]);
  });
  it("ignora los descartados", () => {
    expect(newPaths(slot({ query: "tag:infra.proveedores" }), atoms)).toEqual([A(4)]);
  });
  it("una consulta vacía o sin filtros válidos no trae nada", () => {
    expect(newPaths(slot({ query: "" }), atoms)).toEqual([]);
    expect(newPaths(slot({ query: "tipo:foo" }), atoms)).toEqual([]);
  });
  it("newBySlot calcula los cuatro slots", () => {
    const informe = informesFromDocuments(docs)[0]!;
    informe.slots.resumen.query = "tipo:hecho";
    const nb = newBySlot(informe, atoms);
    expect(nb.resumen).toEqual([A(3)]);
    expect(Object.keys(nb)).toEqual(["resumen", "decisiones", "riesgos", "pendientes"]);
  });
});

describe("slotItems", () => {
  it("nuevos primero, luego lista (pin o regla) y excluidos", () => {
    const items = slotItems(slot({ atomos: [A(1), A(2)], pins: [A(2)], excluidos: [A(6)] }), [A(3)]);
    expect(items).toEqual([
      { path: A(3), state: "nuevo" },
      { path: A(1), state: "regla" },
      { path: A(2), state: "pin" },
      { path: A(6), state: "excluido" },
    ]);
    expect(items.filter((i) => isIncluded(i.state))).toHaveLength(2);
  });
  it("un pin fuera de la lista también cuenta; no repite rutas", () => {
    const items = slotItems(slot({ atomos: [A(1)], pins: [A(5), A(1)] }), []);
    expect(items).toEqual([
      { path: A(1), state: "pin" },
      { path: A(5), state: "pin" },
    ]);
  });
});

describe("chips de filtro", () => {
  it("salen de los tokens que no son texto, con su posición", () => {
    expect(filterChips("hechos tipo:hecho tag:infra.ingesta tipo:foo")).toEqual([
      { index: 1, label: "Tipo", value: "hecho", active: true },
      { index: 2, label: "Tag", value: "infra.ingesta", active: true },
      { index: 3, label: "Tipo", value: "foo", active: false },
    ]);
  });
  it("agregar un filtro lo suma al final", () => {
    expect(addQueryFilter("texto", "estado", "confirmado")).toBe("texto estado:confirmado");
    expect(addQueryFilter("", "tipo", "hecho")).toBe("tipo:hecho");
  });
});
