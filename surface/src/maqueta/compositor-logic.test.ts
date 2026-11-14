import { describe, expect, it } from "vitest";
import fixture from "../core/__fixtures__/atoms.json";
import { atomsFromDocuments, informesFromDocuments } from "../core/atoms";
import type { GraphDocument, InformeSlot } from "../core/contract";
import type { Edge } from "../core/contract";
import { addQueryFilter, filterChips, filterOptions, isIncluded, newBySlot, newPaths, queryOptions, slotItems } from "./compositor-logic";

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
    informe.slotList[0]!.query = "tipo:hecho";
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
      { index: 1, label: "Tipo: Hecho", prefix: "Tipo", value: "Hecho", active: true },
      { index: 2, label: "Tag: Ingesta", prefix: "Tag", value: "Ingesta", active: true },
      { index: 3, label: "Tipo: Foo", prefix: "Tipo", value: "Foo", active: false },
    ]);
  });
  it("los tokens nuevos: base, distancia, relación, con títulos de grupo", () => {
    const grupos = [{ tag: "paciente", title: "Paciente" }] as never;
    const chips = filterChips("base:paciente distancia:1 tag:asistente relacion:activa,detalla libre", { grupos });
    expect(chips.map((c) => c.label)).toEqual(["Base: Paciente", "Distancia: 1 salto", "Tag: Asistente", "Relación: activa, detalla"]);
    expect(chips.map((c) => c.index)).toEqual([0, 1, 2, 3]);
  });
  it("agregar un filtro lo suma al final", () => {
    expect(addQueryFilter("texto", "estado", "confirmado")).toBe("texto estado:confirmado");
    expect(addQueryFilter("", "tipo", "hecho")).toBe("tipo:hecho");
  });
});

describe("nuevos con aristas (distancia y relación)", () => {
  const mk = (n: number, tags: string[], kind = "regla") => ({ ...atoms[0]!, id: `x${n}`, gid: `g${n}`, path: `docs/x${n}.md`, kind, tags, status: "propuesto" });
  const pool = [mk(1, ["programa.asistente"]), mk(2, ["paciente.situacion"]), mk(3, ["paciente.situacion"])] as never[];
  const edge = (source: string, target: string, type: string) => ({ source, target, type, origin: "relation", relationDoc: "r" }) as unknown as Edge;
  it("distancia amplía las semillas por relaciones", () => {
    const edges = [edge("g1", "g2", "activa")];
    expect(newPaths(slot({ query: "base:programa" }), pool, edges)).toEqual(["docs/x1.md"]);
    expect(newPaths(slot({ query: "base:programa distancia:1" }), pool, edges)).toEqual(["docs/x1.md", "docs/x2.md"]);
  });
  it("relacion filtra por tipo de relación", () => {
    const edges = [edge("g1", "g2", "activa"), edge("g2", "g3", "cerca_de")];
    expect(newPaths(slot({ query: "relacion:cerca_de" }), pool, edges)).toEqual(["docs/x2.md", "docs/x3.md"]);
  });
});

describe("filterOptions", () => {
  it("ofrece valores válidos de los datos", () => {
    const a = atoms.slice(0, 3);
    expect(filterOptions("tipo", { atoms: a }).length).toBeGreaterThan(0);
    expect(filterOptions("estado", { atoms: a }).map((o) => o.value)).toEqual(["propuesto", "confirmado", "descartado"]);
    expect(filterOptions("distancia", { atoms: a }).map((o) => o.value)).toEqual(["0", "1", "2", "3"]);
    expect(filterOptions("base", { atoms: a }).map((o) => o.value)).toContain("infra");
    expect(queryOptions(a).kinds).toContain("regla");
  });
});
