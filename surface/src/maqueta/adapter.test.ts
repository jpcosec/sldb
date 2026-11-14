import { describe, expect, it } from "vitest";
import fixture from "../core/__fixtures__/atoms.json";
import { actasFromDocuments, atomsFromDocuments } from "../core/atoms";
import type { Edge, GraphDocument } from "../core/contract";
import { paragraphIndexAt, toMockAtoms, toMockRelations } from "./adapter";

const docs = fixture.documents as unknown as GraphDocument[];
const edges = fixture.edges as unknown as Edge[];
const atoms = atomsFromDocuments(docs);
const acta = actasFromDocuments(docs)[0];

describe("adapter de la maqueta", () => {
  it("cada átomo lleva su párrafo y su cita", () => {
    const mock = toMockAtoms(atoms, acta);
    expect(mock).toHaveLength(atoms.length);
    for (const m of mock) {
      expect(m.anchor[1]).toBe(m.atom.quote);
      expect(m.id).toBe(m.atom.id);
    }
    expect(paragraphIndexAt("uno\n\ndos", 5)).toBe(1);
    expect(paragraphIndexAt("uno\n\ndos", 3)).toBe(-1);
  });
  it("solo entran relaciones (RelationDoc) entre átomos existentes", () => {
    const rel = toMockRelations(edges, atoms);
    expect(rel.length).toBeGreaterThan(0);
    expect(rel.every((r) => r.relationDoc !== null || r.type.length > 0)).toBe(true);
    const ids = new Set(atoms.map((a) => a.id));
    expect(rel.every((r) => r.source.startsWith("g:") || ids.has(r.source))).toBe(true);
  });
  it("cada átomo se ancla contra el body de SU fuente y trae base y sourceId", () => {
    const fu = (id: string, body: string) => ({ id, gid: `FuenteDoc:${id}`, body });
    const mk = (id: string, source: string, start: number, tags: string[]) => ({ ...atoms[0]!, id, gid: `AtomDoc:${id}`, source, start, tags, quote: "q" });
    const mock = toMockAtoms(
      [mk("a", "FuenteDoc:uno", 5, ["programa.asistente"]), mk("b", "FuenteDoc:dos", 5, ["paciente.perfil"]), mk("c", "FuenteDoc:otra", 0, [])],
      [fu("uno", "xx\n\nyyyy"), fu("dos", "aaaaaaaaaaaa")],
    );
    expect(mock.map((m) => [m.anchor[0], m.base, m.sourceId])).toEqual([[1, "programa", "uno"], [0, "paciente", "dos"], [-1, "", "otra"]]);
  });
});
