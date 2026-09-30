import { describe, expect, it } from "vitest";
import fixture from "../core/__fixtures__/atoms.json";
import { atomsFromDocuments } from "../core/atoms";
import type { Edge, GraphDocument, RelationTypeSpec } from "../core/contract";
import { toMockAtoms, toMockRelations, type MockAtom, type MockRelation } from "./adapter";
import { computeLayout, edgeSides, expandRelations, fuseEdges, nodeCenter, planConnection, regionClass, relationsOfAtom } from "./grafo-logic";

const acta = undefined;
const atoms = toMockAtoms(atomsFromDocuments(fixture.documents as unknown as GraphDocument[]).filter((a) => a.status !== "descartado"), acta);
const byId = (id: string) => atoms.find((a) => a.id === id)!;

const spec = (name: string, src: string[], tgt: string[]): RelationTypeSpec => ({ id: name, name, source_types: src, target_types: tgt, cardinality: "", description: "" });
const types = [spec("motiva", ["AtomDoc", "GrupoDoc"], ["AtomDoc", "GrupoDoc"]), spec("plazo_de", ["AtomDoc"], ["AtomDoc", "GrupoDoc"]), spec("has_model", [], [])];
const rel = (id: string, source: string, target: string, type = "motiva"): MockRelation => ({ id, source, target, type, relationDoc: id, inherited: source.startsWith("g:") || target.startsWith("g:") || undefined });

describe("computeLayout", () => {
  it("una región por grupo raíz, con los tamaños de la maqueta", () => {
    const l = computeLayout(atoms);
    // fixture: infra (a2 a3 a4 a5), reuniones (a1)
    expect(l.regions.map((r) => r.tag)).toEqual(["infra", "reuniones"]);
    const [infra, reuniones] = l.regions;
    expect(infra).toMatchObject({ x: 0, y: 0, w: 240, h: 50 + 4 * 90 });
    expect(reuniones).toMatchObject({ x: 300, y: 0, w: 240, h: 140 });
    expect(l.atoms.a2).toEqual({ tag: "infra", x: 20, y: 50 });
    expect(l.atoms.a5).toEqual({ tag: "infra", x: 20, y: 320 });
  });

  it("ocho átomos: dos columnas (500 de ancho), fila mayor; el resto se apila en la segunda columna", () => {
    const mk = (id: string, tag: string): MockAtom => ({ ...byId("a2"), id, tags: [tag] });
    const many = [...Array.from({ length: 8 }, (_, i) => mk(`i${i}`, "infra.x")), mk("e1", "equipo"), mk("e2", "equipo"), mk("e3", "equipo"), mk("r1", "riesgos")];
    const l = computeLayout(many);
    expect(l.regions.find((r) => r.tag === "infra")).toMatchObject({ x: 0, y: 0, w: 500, h: 410 });
    expect(l.regions.find((r) => r.tag === "equipo")).toMatchObject({ x: 560, y: 0, w: 240, h: 320 });
    expect(l.regions.find((r) => r.tag === "riesgos")).toMatchObject({ x: 560, y: 360, w: 240, h: 140 });
    expect(l.atoms.i1).toEqual({ tag: "infra", x: 260, y: 50 });
    expect(l.atoms.i2).toEqual({ tag: "infra", x: 20, y: 140 });
  });

  it("es determinista", () => {
    expect(computeLayout(atoms)).toEqual(computeLayout([...atoms]));
  });

  it("átomos sin tags van a la región (sin grupo)", () => {
    const l = computeLayout([{ ...byId("a1"), tags: [] }]);
    expect(l.regions[0]!.tag).toBe("(sin grupo)");
  });
});

describe("regionClass", () => {
  it("color propio solo para las regiones de la maqueta", () => {
    expect(regionClass("infra")).toBe("infra");
    expect(regionClass("Equipo")).toBe("equipo");
    expect(regionClass("reuniones")).toBeNull();
  });
});

describe("expandRelations / fuseEdges", () => {
  const relations = [rel("r1", "a5", "a2"), rel("r2", "g:infra.ingesta", "a4"), rel("r3", "g:infra", "g:reuniones")];

  it("una relación sobre un grupo la heredan sus átomos (punteada); grupo-grupo se omite", () => {
    const flat = expandRelations(relations, atoms);
    const inh = flat.filter((f) => f.inherited);
    expect(inh.map((f) => `${f.source}>${f.target}`).sort()).toEqual(["a2>a4", "a3>a4"]);
    expect(flat.filter((f) => !f.inherited).map((f) => `${f.source}>${f.target}`)).toEqual(["a5>a2"]);
  });

  it("no duplica la heredada si ya existe la directa (mismo par y tipo)", () => {
    const flat = expandRelations([rel("r1", "a2", "a4"), rel("r2", "g:infra.ingesta", "a4")], atoms);
    expect(flat.map((f) => `${f.source}>${f.target}:${f.inherited}`).sort()).toEqual(["a2>a4:false", "a3>a4:true"]);
  });

  it("plegar un grupo fusiona las aristas de sus átomos en un nodo y suprime las internas", () => {
    const flat = expandRelations([rel("r1", "a5", "a2"), rel("r2", "a2", "a1"), rel("r3", "a3", "a1", "plazo_de")], atoms);
    const open = fuseEdges(flat, atoms, new Set(), []);
    expect(open).toHaveLength(3);
    const folded = fuseEdges(flat, atoms, new Set(["infra"]), []);
    expect(folded).toHaveLength(1); // a5>a2 queda dentro de infra
    expect(folded[0]).toMatchObject({ source: "g:infra", target: "a1" });
    expect(folded[0]!.list.map((r) => r.id)).toEqual(["r2", "r3"]);
  });

  it("los tipos ocultos no se dibujan", () => {
    const flat = expandRelations([rel("r1", "a5", "a2"), rel("r2", "a2", "a1", "plazo_de")], atoms);
    expect(fuseEdges(flat, atoms, new Set(), ["plazo_de"]).map((f) => f.list[0]!.id)).toEqual(["r1"]);
  });

  it("la heredada y la directa entre los mismos nodos van en aristas separadas", () => {
    const flat = expandRelations([rel("r1", "a2", "a4"), rel("r2", "g:infra", "a4", "plazo_de")], atoms);
    const keys = fuseEdges(flat, atoms, new Set(), []).map((f) => f.key);
    expect(keys).toContain("a2->a4");
    expect(keys).toContain("a2->a4:inh");
  });

  it("toMockRelations + expandRelations con el fixture: 1 directa y las heredadas del grupo infra", () => {
    const rels = toMockRelations(fixture.edges as unknown as Edge[], atomsFromDocuments(fixture.documents as unknown as GraphDocument[]));
    const flat = expandRelations(rels, atoms);
    expect(flat.filter((f) => !f.inherited)).toHaveLength(1);
  });
});

describe("geometría", () => {
  it("edgeSides elige los lados por posición relativa", () => {
    expect(edgeSides([0, 0], [400, 10])).toEqual(["r", "l"]);
    expect(edgeSides([400, 0], [0, 10])).toEqual(["l", "r"]);
    expect(edgeSides([0, 0], [10, 200])).toEqual(["b", "t"]);
    expect(edgeSides([0, 200], [10, 0])).toEqual(["t", "b"]);
  });

  it("nodeCenter: átomo (esquina + 105,32) y grupo plegado", () => {
    const l = computeLayout(atoms);
    const r = l.regions[1]!;
    expect(nodeCenter("a2", l, new Set())).toEqual([0 + 20 + 105, 0 + 50 + 32]);
    expect(nodeCenter("g:reuniones", l, new Set(["reuniones"]))).toEqual([r.x + r.w / 2, r.y + 85]);
    expect(nodeCenter("g:nada", l, new Set())).toBeNull();
  });
});

describe("relationsOfAtom", () => {
  it("incluye las directas y las que caen sobre un grupo del átomo", () => {
    const rs = [rel("r1", "a2", "a1"), rel("r2", "g:infra.ingesta", "a4"), rel("r3", "a4", "a1"), rel("r4", "g:reuniones", "a4")];
    expect(relationsOfAtom(byId("a2"), rs).map((r) => r.id)).toEqual(["r1", "r2"]);
  });
});

describe("planConnection", () => {
  const base = { atoms, types, edges: [] as Edge[], groupLabel: (t: string) => t.toUpperCase() };
  const edge = (source: string, target: string, type: string): Edge => ({ id: "e", source, target, type, origin: "relation_doc", relationDoc: "r1" });

  it("átomo → átomo válido", () => {
    const p = planConnection({ ...base, sourceId: "a2", targetId: "a1", typeName: "motiva" });
    expect(p).toMatchObject({ ok: true, source: { gid: "AtomDoc:a2" }, target: { gid: "AtomDoc:a1" }, type: { name: "motiva" } });
  });

  it("átomo → grupo: extremo GrupoDoc con su tag (para crear el grupo si falta)", () => {
    const p = planConnection({ ...base, sourceId: "a2", targetId: "g:infra", typeName: "motiva" });
    expect(p).toMatchObject({ ok: true, target: { gid: "GrupoDoc:infra", model: "GrupoDoc", tag: "infra", label: "Grupo INFRA" } });
  });

  it("rechaza lo que ya existe, sin crear", () => {
    const p = planConnection({ ...base, edges: [edge("AtomDoc:a2", "AtomDoc:a1", "motiva")], sourceId: "a2", targetId: "a1", typeName: "motiva" });
    expect(p).toMatchObject({ ok: false });
    expect((p as { message: string }).message).toMatch(/Ya existe «motiva»/);
  });

  it("rechaza un tipo que no admite el extremo (grupo como origen de plazo_de) y sugiere los válidos", () => {
    const p = planConnection({ ...base, sourceId: "g:infra", targetId: "a1", typeName: "plazo_de" });
    expect(p.ok).toBe(false);
    expect((p as { message: string }).message).toMatch(/«plazo_de» no es válido.*sirven: motiva/);
  });

  it("no ofrece tipos estructurales (has_model) ni grupo→grupo ni un nodo consigo mismo", () => {
    expect(planConnection({ ...base, sourceId: "a2", targetId: "a1", typeName: "has_model" }).ok).toBe(false);
    expect((planConnection({ ...base, sourceId: "g:infra", targetId: "g:reuniones", typeName: "motiva" }) as { message: string }).message).toMatch(/grupo con otro grupo/);
    expect((planConnection({ ...base, sourceId: "a2", targetId: "a2", typeName: "motiva" }) as { message: string }).message).toMatch(/consigo mismo/);
  });

  it("(sin grupo) no es un grupo real", () => {
    const p = planConnection({ ...base, sourceId: "a2", targetId: "g:(sin grupo)", typeName: "motiva" });
    expect((p as { message: string }).message).toMatch(/no es un grupo real/);
  });
});
