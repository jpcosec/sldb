/**
 * De los datos reales a la forma que esperan los componentes de la maqueta.
 *
 * La maqueta trabaja con `{id, type, text, tags, anchor:[párrafo, cita], conf, status}` y con
 * relaciones `{id, source, target, type, inherited?}`. Acá se derivan de los átomos y aristas de
 * SLDB, conservando el `Atom` completo (`atom`) para poder persistir por id.
 */
import { paragraphsOf } from "../core/atom-text";
import { linkKind } from "../core/atom-graph";
import { tagOfGroupGid } from "../core/atom-groups";
import { baseOf } from "../core/caso";
import type { Atom, AtomKind, AtomStatus, Edge } from "../core/contract";

export interface MockAtom {
  id: string;
  type: AtomKind;
  text: string;
  /** Tags tal cual (con puntos): `infra.ingesta`. */
  tags: string[];
  /** `[índice de párrafo, cita]`; `[-1, cita]` si el ancla no cae en ningún párrafo. */
  anchor: [number, string];
  conf: number;
  status: AtomStatus;
  /** Base de conocimiento: 1er segmento del primer tag (`paciente`); `""` sin tags. */
  base: string;
  /** Id de la fuente del átomo (`system-prompt`, o el acta), tomado de `atom.source`. */
  sourceId: string;
  /** El átomo real, para persistir. */
  atom: Atom;
}

export interface MockRelation {
  id: string;
  /** `a3` para un átomo, `g:<tag>` para un grupo. */
  source: string;
  target: string;
  type: string;
  /** Relación declarada sobre un grupo: la heredan los átomos del grupo. */
  inherited?: boolean;
  /** RelationDoc que la origina. */
  relationDoc: string | null;
}

/** Párrafo (en `paragraphsOf(body)`) que contiene el offset `start`; `-1` si ninguno. */
export function paragraphIndexAt(body: string, start: number): number {
  return paragraphsOf(body).findIndex((p) => start >= p.start && start < p.end);
}

/** Lo mínimo de una fuente/acta para calcular anclas: `Fuente` y `Acta` calzan. */
export interface BodySource {
  id: string;
  gid: string;
  body: string;
}

/** Id de la fuente en `atom.source` (`FuenteDoc:folleto` -> `folleto`). */
export const sourceIdOf = (source: string): string => source.slice(source.indexOf(":") + 1);

/**
 * `sources` puede ser UNA fuente/acta (se usa para todos los átomos: el caso viejo) o la lista
 * de fuentes del caso: cada átomo se ancla contra el `body` de SU fuente (`atom.source`). Sin
 * fuente, el párrafo es `-1`.
 */
export function toMockAtoms(atoms: Atom[], sources: BodySource | BodySource[] | undefined): MockAtom[] {
  const list = sources === undefined ? [] : Array.isArray(sources) ? sources : [sources];
  return atoms.map((atom) => {
    const src = Array.isArray(sources) ? list.find((f) => f.gid === atom.source) : list[0];
    return {
      id: atom.id,
      type: atom.kind,
      text: atom.text,
      tags: atom.tags,
      anchor: [src ? paragraphIndexAt(src.body, atom.start) : -1, atom.quote],
      conf: atom.conf,
      status: atom.status,
      base: baseOf(atom.tags[0] ?? ""),
      sourceId: sourceIdOf(atom.source),
      atom,
    };
  });
}

const atomIdOf = (end: string) => (end.startsWith("AtomDoc:") ? end.slice("AtomDoc:".length) : null);

/** Aristas de RelationDoc entre átomos (y sobre grupos, marcadas `inherited`); ignora las estructurales. */
export function toMockRelations(edges: Edge[], atoms: Atom[]): MockRelation[] {
  const ids = new Set(atoms.map((a) => a.id));
  const out: MockRelation[] = [];
  for (const e of edges) {
    if (linkKind(e) !== "relation") continue;
    const group = (end: string) => tagOfGroupGid(end, atoms.flatMap((a) => a.tags));
    const s = atomIdOf(e.source) ?? (group(e.source) ? `g:${group(e.source)}` : null);
    const t = atomIdOf(e.target) ?? (group(e.target) ? `g:${group(e.target)}` : null);
    if (!s || !t) continue;
    if ((!s.startsWith("g:") && !ids.has(s)) || (!t.startsWith("g:") && !ids.has(t))) continue;
    out.push({ id: e.id, source: s, target: t, type: e.type, inherited: s.startsWith("g:") || t.startsWith("g:") || undefined, relationDoc: e.relationDoc });
  }
  return out;
}
