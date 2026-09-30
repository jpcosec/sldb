/** Rutas por hash: #/lector, #/destilacion, #/doc/<id>, #/doc/<id>/compose, #/extract, #/salud, #/bandeja,
 * #/atomos/texto/<actaId>, #/atomos/grafo, #/atomos/informe/<id>. */
import { useEffect, useState } from "react";

export type Route =
  | { view: "home" }
  | { view: "doc"; id: string; mode: "document" | "compose" }
  | { view: "lector" }
  | { view: "destilacion" }
  | { view: "extract" }
  | { view: "salud" }
  | { view: "bandeja" }
  | { view: "atomos-texto"; id: string }
  | { view: "atomos-grafo" }
  | { view: "atomos-informe"; id: string };

export function parseRoute(hash: string): Route {
  const parts = hash.replace(/^#\/?/, "").split("/").map(decodeURIComponent);
  if (parts[0] === "doc" && parts[1]) return { view: "doc", id: parts[1], mode: parts[2] === "compose" ? "compose" : "document" };
  if (parts[0] === "lector") return { view: "lector" };
  if (parts[0] === "destilacion") return { view: "destilacion" };
  if (parts[0] === "extract") return { view: "extract" };
  if (parts[0] === "salud") return { view: "salud" };
  if (parts[0] === "bandeja") return { view: "bandeja" };
  if (parts[0] === "atomos") {
    if (parts[1] === "texto" && parts[2]) return { view: "atomos-texto", id: parts[2] };
    if (parts[1] === "grafo") return { view: "atomos-grafo" };
    if (parts[1] === "informe" && parts[2]) return { view: "atomos-informe", id: parts[2] };
  }
  return { view: "home" };
}

export function hrefFor(route: Route): string {
  if (route.view === "doc") return `#/doc/${encodeURIComponent(route.id)}${route.mode === "compose" ? "/compose" : ""}`;
  if (route.view === "lector") return "#/lector";
  if (route.view === "destilacion") return "#/destilacion";
  if (route.view === "extract") return "#/extract";
  if (route.view === "salud") return "#/salud";
  if (route.view === "bandeja") return "#/bandeja";
  if (route.view === "atomos-texto") return `#/atomos/texto/${encodeURIComponent(route.id)}`;
  if (route.view === "atomos-grafo") return "#/atomos/grafo";
  if (route.view === "atomos-informe") return `#/atomos/informe/${encodeURIComponent(route.id)}`;
  return "#/";
}

export function useRoute(): Route {
  const [route, setRoute] = useState(() => parseRoute(window.location.hash));
  useEffect(() => {
    const onChange = () => setRoute(parseRoute(window.location.hash));
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return route;
}

export function navigate(route: Route): void {
  window.location.hash = hrefFor(route);
}
