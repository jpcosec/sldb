import { describe, expect, it } from "vitest";
import fixture from "../core/__fixtures__/atoms.json";
import { atomsFromDocuments } from "../core/atoms";
import type { Edge, GraphDocument, RelationTypeSpec } from "../core/contract";
import { toMockAtoms, toMockRelations, type MockAtom, type MockRelation } from "./adapter";
import { computeLayout, edgeSides, expandRelations, fuseEdges, nodeCenter, planConnection, readingOrder, regionClass, relationsOfAtom, typeLabel } from "./grafo-logic";

const acta = undefined;
const atoms = toMockAtoms(atomsFromDocuments(fixture.documents as unknown as GraphDocument[]).filter((a) => a.status !== "descartado"), acta);
const byId = (id: string) => atoms.find((a) => a.id === id)!;

const spec = (name: string, src: string[], tgt: string[]): RelationTypeSpec => ({ id: name, name, source_types: src, target_types: tgt, cardinality: "", description: "" });
const types = [spec("motiva", ["AtomDoc", "GrupoDoc"], ["AtomDoc", "GrupoDoc"]), spec("plazo_de", ["AtomDoc"], ["AtomDoc", "GrupoDoc"]), spec("has_model", [], [])];
const rel = (id: string, source: string, target: string, type = "motiva"): MockRelation => ({ id, source, target, type, relationDoc: id, inherited: source.startsWith("g:") || target.startsWith("g:") || undefined });

const mk = (id: string, tag: string | string[], start = 0, source = "ActaDoc:acta"): MockAtom => {
  const tags = Array.isArray(tag) ? tag : [tag];
  return { ...byId("a2"), id, tags, atom: { ...byId("a2").atom, id, gid: `AtomDoc:${id}`, tags, start, source } };
};
/** Los 30 átomos de Levira con el orden y los tamaños de la maqueta. */
const levira = (): MockAtom[] => {
  const groups: [string, number][] = [["programa.asistente", 7], ["programa.cuidados", 5], ["programa.beneficios", 2], ["programa.receta", 4], ["programa.red", 3], ["paciente.perfil", 2], ["paciente.situacion", 2], ["paciente.tratamiento", 3], ["paciente.intencion", 2]];
  let n = 0;
  return groups.flatMap(([tag, count]) => Array.from({ length: count }, () => mk(`x${n}`, tag, n++)));
};

describe("computeLayout", () => {
  it("con los 30 átomos de Levira: Programa (21, 830 de ancho) y Paciente (9, 560), con las posiciones de la maqueta", () => {
    const l = computeLayout(levira());
    expect(l.bases.map((b) => [b.tag, b.x, b.y, b.w])).toEqual([["programa", 0, 0, 830], ["paciente", 990, 0, 560]]);
    const [programa, paciente] = l.bases;
    const cell = (b: typeof programa, tag: string) => b!.cells.find((c) => c.tag === tag)!;
    const Rs = (n: number) => 40 + n * 82 + 8;
    expect(cell(programa, "programa.asistente")).toMatchObject({ x: 20, y: 44, h: Rs(7) });
    expect(cell(programa, "programa.cuidados")).toMatchObject({ x: 290, y: 44, h: Rs(5) });
    expect(cell(programa, "programa.beneficios")).toMatchObject({ x: 290, y: 44 + Rs(5) + 16, h: Rs(2) });
    expect(cell(programa, "programa.receta")).toMatchObject({ x: 560, y: 44 });
    expect(cell(programa, "programa.red")).toMatchObject({ x: 560, y: 44 + Rs(4) + 16 });
    expect(programa!.h).toBe(Math.max(...programa!.cells.map((c) => c.y + c.h)) + 20);
    expect(cell(paciente, "paciente.perfil")).toMatchObject({ x: 20, y: 44 });
    expect(cell(paciente, "paciente.situacion")).toMatchObject({ x: 20, y: 44 + Rs(2) + 16 });
    expect(cell(paciente, "paciente.tratamiento")).toMatchObject({ x: 290, y: 44 });
    expect(cell(paciente, "paciente.intencion")).toMatchObject({ x: 290, y: 44 + Rs(3) + 16 });
    // átomos: relativos a su subgrupo, con paso 82
    expect(l.atoms.x0).toEqual({ parent: "g:programa.asistente", base: "programa", x: 20, y: 40 });
    expect(l.atoms.x2).toEqual({ parent: "g:programa.asistente", base: "programa", x: 20, y: 40 + 2 * 82 });
  });

  it("es determinista y sigue el orden de primera aparición (el de la barra lateral)", () => {
    const l = computeLayout(levira());
    expect(computeLayout([...levira()])).toEqual(l);
    expect(l.bases[0]!.cells.map((c) => c.tag)).toEqual(["programa.asistente", "programa.cuidados", "programa.beneficios", "programa.receta", "programa.red"]);
  });

  it("store viejo: el 1er segmento es la base, el 2º un subgrupo y un átomo sin 2º segmento va directo a la base", () => {
    const l = computeLayout(atoms);
    expect(l.bases.map((b) => b.tag)).toEqual(["reuniones", "infra"]); // a1 (Reunión) abre el texto
    const infra = l.bases[1]!;
    expect(infra.cells.map((c) => c.tag)).toEqual([null, "infra.ingesta", "infra.proveedores"]);
    expect(infra).toMatchObject({ x: 450, y: 0, w: 20 + 2 * 270 });
    expect(l.atoms.a2).toEqual({ parent: "g:infra.ingesta", base: "infra", x: 20, y: 40 });
    // a5 tiene por tag solo `infra`: cuelga de la base, en la primera columna
    expect(l.atoms.a5).toEqual({ parent: "g:infra", base: "infra", x: 40, y: 44 });
    expect(l.bases[0]).toMatchObject({ tag: "reuniones", x: 0, w: 290 });
    expect(infra.x).toBe(290 + 160);
  });

  it("un átomo con varios tags va a la base y subgrupo de su PRIMER tag", () => {
    const l = computeLayout([mk("m1", ["programa.red", "paciente.perfil"])]);
    expect(l.bases.map((b) => b.tag)).toEqual(["programa"]);
    expect(l.atoms.m1!.parent).toBe("g:programa.red");
  });

  it("átomos sin tags van a la región (sin grupo), siempre al final", () => {
    const l = computeLayout([{ ...byId("a1"), tags: [] }, mk("z", "zeta.uno")]);
    expect(l.bases.map((b) => b.tag)).toEqual(["zeta", "(sin grupo)"]);
  });

  it("tandas de subgrupos por columna: 1 -> 1; 2 -> 1+1; 4 -> 2+2; 5 -> 1+2+2", () => {
    const of = (n: number) => computeLayout(Array.from({ length: n }, (_, i) => mk(`s${i}`, `b.g${i}`)));
    const cols = (n: number) => of(n).bases[0]!.cells.map((c) => c.x);
    expect(cols(1)).toEqual([20]);
    expect(cols(2)).toEqual([20, 290]);
    expect(cols(4)).toEqual([20, 20, 290, 290]);
    expect(cols(5)).toEqual([20, 290, 290, 560, 560]);
  });
});

describe("readingOrder", () => {
  it("por fuente (prompt, folleto, mensaje) y luego por posición en el texto", () => {
    const fuentes = [{ gid: "FuenteDoc:m", tipo: "mensaje" }, { gid: "FuenteDoc:f", tipo: "folleto" }, { gid: "FuenteDoc:p", tipo: "prompt" }];
    const list = [mk("m1", "a", 5, "FuenteDoc:m"), mk("f2", "a", 9, "FuenteDoc:f"), mk("p1", "a", 50, "FuenteDoc:p"), mk("f1", "a", 1, "FuenteDoc:f")];
    expect(readingOrder(list, fuentes).map((a) => a.id)).toEqual(["p1", "f1", "f2", "m1"]);
  });
});

describe("regionClass / typeLabel", () => {
  it("color propio para las bases conocidas; el resto rota; sin grupo, neutro", () => {
    expect(regionClass("programa")).toBe("infra");
    expect(regionClass("Paciente")).toBe("riesgos");
    expect(regionClass("equipo")).toBe("equipo");
    expect(regionClass("reuniones", 1)).toBe("riesgos");
    expect(regionClass("(sin grupo)")).toBeNull();
  });
  it("el tipo se muestra con espacios", () => {
    expect(typeLabel("consulta_por")).toBe("consulta por");
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

  it("plegar un subgrupo lleva sus átomos a `g:<subgrupo>`; la base plegada gana", () => {
    const flat = expandRelations([rel("r1", "a5", "a2"), rel("r2", "a2", "a1"), rel("r3", "a3", "a2")], atoms);
    const sub = fuseEdges(flat, atoms, new Set(["infra.ingesta"]), []);
    expect(sub.map((f) => `${f.source}>${f.target}`).sort()).toEqual(["a5>g:infra.ingesta", "g:infra.ingesta>a1"]);
    const both = fuseEdges(flat, atoms, new Set(["infra.ingesta", "infra"]), []);
    expect(both.map((f) => `${f.source}>${f.target}`)).toEqual(["g:infra>a1"]);
  });

  it("crossBase: solo las aristas que cruzan de una base a otra", () => {
    const flat = expandRelations([rel("r1", "a5", "a2"), rel("r2", "a2", "a1")], atoms);
    const byKey = Object.fromEntries(fuseEdges(flat, atoms, new Set(), []).map((f) => [f.key, f.crossBase]));
    expect(byKey).toEqual({ "a5->a2": false, "a2->a1": true });
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

  it("nodeCenter: átomo (con su subgrupo), subgrupo y base, plegados o no", () => {
    const l = computeLayout(atoms);
    const [reuniones, infra] = l.bases;
    const ingesta = infra!.cells.find((c) => c.tag === "infra.ingesta")!;
    expect(nodeCenter("a2", l, new Set())).toEqual([infra!.x + ingesta.x + 20 + 105, infra!.y + ingesta.y + 40 + 32]);
    expect(nodeCenter("g:reuniones", l, new Set(["reuniones"]))).toEqual([reuniones!.x + reuniones!.w / 2, reuniones!.y + 85]);
    expect(nodeCenter("g:reuniones", l, new Set())).toEqual([reuniones!.x + reuniones!.w / 2, reuniones!.y + reuniones!.h / 2]);
    expect(nodeCenter("g:infra.ingesta", l, new Set())).toEqual([infra!.x + ingesta.x + 125, infra!.y + ingesta.y + ingesta.h / 2]);
    expect(nodeCenter("g:infra.ingesta", l, new Set(["infra.ingesta"]))).toEqual([infra!.x + ingesta.x + 125, infra!.y + ingesta.y + 50]);
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
    expect(p).toMatchObject({ ok: true, target: { gid: "GrupoDoc:infra", model: "GrupoDoc", tag: "infra", label: "Base INFRA" } });
  });

  it("rechaza lo que ya existe, sin crear", () => {
    const p = planConnection({ ...base, edges: [edge("AtomDoc:a2", "AtomDoc:a1", "motiva")], sourceId: "a2", targetId: "a1", typeName: "motiva" });
    expect(p).toMatchObject({ ok: false });
    expect((p as { message: string }).message).toMatch(/Ya existe «motiva»/);
  });

  it("rechaza un tipo que no admite el extremo (grupo como origen de plazo_de) y sugiere los válidos", () => {
    const p = planConnection({ ...base, sourceId: "g:infra", targetId: "a1", typeName: "plazo_de" });
    expect(p.ok).toBe(false);
    expect((p as { message: string }).message).toMatch(/«plazo de» no admite un grupo o una base.*sirven: motiva/);
  });

  it("un tipo que no lista GrupoDoc se rechaza con aviso claro (subgrupo o base)", () => {
    const only = [spec("activa", ["AtomDoc"], ["AtomDoc"]), spec("restringe", ["AtomDoc", "GrupoDoc"], ["AtomDoc", "GrupoDoc"])];
    const p = planConnection({ ...base, types: only, sourceId: "a2", targetId: "g:infra.ingesta", typeName: "activa" });
    expect((p as { message: string }).message).toMatch(/«activa» no admite un grupo o una base como extremo \(Grupo INFRA\.INGESTA\)\. Con grupos sirven: restringe\./);
    const q = planConnection({ ...base, types: only, sourceId: "a2", targetId: "g:infra", typeName: "restringe" });
    expect(q).toMatchObject({ ok: true, target: { gid: "GrupoDoc:infra", tag: "infra", label: "Base INFRA" } });
    const sub = planConnection({ ...base, types: only, sourceId: "a2", targetId: "g:infra.ingesta", typeName: "restringe" });
    expect(sub).toMatchObject({ ok: true, target: { gid: "GrupoDoc:infra-ingesta", tag: "infra.ingesta" } });
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
