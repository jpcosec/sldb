import { describe, expect, it } from "vitest";
import { hrefFor, parseRoute, type Route } from "./router";

describe("router", () => {
  const cases: [string, Route][] = [
    ["#/", { view: "home" }],
    ["#/doc/a%20b/compose", { view: "doc", id: "a b", mode: "compose" }],
    ["#/salud", { view: "salud" }],
    ["#/atomos/texto/acta", { view: "atomos-texto", id: "acta" }],
    ["#/atomos/grafo", { view: "atomos-grafo" }],
    ["#/atomos/informe/inf%201", { view: "atomos-informe", id: "inf 1" }],
  ];
  it.each(cases)("%s <-> ruta", (hash, route) => {
    expect(parseRoute(hash)).toEqual(route);
    expect(hrefFor(route)).toBe(hash);
  });
  it("rutas de átomos incompletas o desconocidas caen a home", () => {
    expect(parseRoute("#/atomos/texto")).toEqual({ view: "home" });
    expect(parseRoute("#/atomos/informe")).toEqual({ view: "home" });
    expect(parseRoute("#/atomos/otra")).toEqual({ view: "home" });
  });
});
