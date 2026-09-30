import { describe, expect, it, vi } from "vitest";
import type { DocumentSegments, GraphDocument, Segment } from "./contract";
import { SldbHttpError, type SldbClient } from "./client";
import { collectHealth, undeclaredHeadings } from "./health";

const doc: GraphDocument = { id: "spec", model_name: "DomainAtom", path: "domain/spec.md", payload: {} };

const field = (path: string, marker: string, text: string, children: Segment[] = []): Segment =>
  ({ type: "field", path, marker, text, start: 0, end: text.length, traits: [], editable: marker !== "render", display: "block", source: null, children }) as Segment;

const literal = (text: string): Segment =>
  ({ type: "literal", text, start: 0, end: text.length }) as Segment;

const segments = (tree: Segment[], canonical: boolean | null = true): DocumentSegments =>
  ({ id: "spec", doc: "spec", model: "DomainAtom", path: "domain/spec.md", text: "", canonical, payload: {}, segments: tree });

describe("undeclaredHeadings", () => {
  it("cuenta los headings dentro del valor de un field rev, no los del template", () => {
    const data = segments([
      literal("# "),
      field("title", "render", "Spec de cobranza"),
      literal("\n\n## Answer\n\n"),
      field("answer", "rev", "intro\n\n## Entidades\n\ntexto\n\n## Herramientas trazadas\n\nmás"),
    ]);
    expect(undeclaredHeadings(data)).toEqual(["Entidades", "Herramientas trazadas"]);
  });

  it("encuentra headings anidados y en optrev, y acepta todos los niveles", () => {
    const data = segments([
      field("body", "optrev", "### Medición 1 — consultable\n\n#### detalle"),
      field("outer", "rev", "", [field("inner", "optrev", "## Consultas de verificación (M1)")]),
    ]);
    expect(undeclaredHeadings(data)).toEqual(["Medición 1 — consultable", "detalle", "Consultas de verificación (M1)"]);
  });

  it("ignora `#` sin espacio y los fields no editables", () => {
    const data = segments([
      field("render_field", "render", "# no cuenta"),
      field("answer", "rev", "#nohesheading\nlínea normal"),
    ]);
    expect(undeclaredHeadings(data)).toEqual([]);
  });
});

describe("collectHealth", () => {
  const clientWith = (segments: SldbClient["segments"]) => ({ segments } as unknown as SldbClient);

  it("clasifica ruido estructural, no canónico y errores de schema", async () => {
    const client = clientWith(
      vi.fn(async () => segments([field("answer", "rev", "## Entidades\n\ntexto")], false)) as unknown as SldbClient["segments"],
    );
    const report = await collectHealth(client, [doc], [{ model: "DomainAtom", error: "x" }]);

    expect(report.checked).toBe(1);
    expect(report.structural).toEqual([{ doc: "spec", model: "DomainAtom", path: "domain/spec.md", headings: ["Entidades"] }]);
    expect(report.noncanonical.map((f) => f.doc)).toEqual(["spec"]);
    expect(report.unreadable).toEqual([]);
    expect(report.modelErrors).toEqual([{ model: "DomainAtom", error: "x" }]);
  });

  it("no marca ruido cuando no hay headings dentro de fields", async () => {
    const client = clientWith(vi.fn(async () => segments([field("answer", "rev", "solo prosa")])) as unknown as SldbClient["segments"]);
    const report = await collectHealth(client, [doc]);
    expect(report.structural).toEqual([]);
    expect(report.noncanonical).toEqual([]);
  });

  it("documentos ilegibles no se presentan como ruido estructural", async () => {
    const client = clientWith(
      vi.fn(async () => {
        throw new SldbHttpError("SLDB respondió 422", 422, null);
      }) as unknown as SldbClient["segments"],
    );
    const report = await collectHealth(client, [doc]);
    expect(report.structural).toEqual([]);
    expect(report.unreadable).toEqual([{ doc: "spec", model: "DomainAtom", path: "domain/spec.md", detail: "SLDB respondió 422" }]);
  });
});
