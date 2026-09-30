/** Rutas por hash: #/lector, #/doc/<id>, #/doc/<id>/compose, #/extract, #/salud, #/bandeja. */
import { useEffect, useState } from "react";

export type Route =
  | { view: "home" }
  | { view: "doc"; id: string; mode: "document" | "compose" }
  | { view: "lector" }
  | { view: "extract" }
  | { view: "salud" }
  | { view: "bandeja" };

export function parseRoute(hash: string): Route {
  const parts = hash.replace(/^#\/?/, "").split("/").map(decodeURIComponent);
  if (parts[0] === "doc" && parts[1]) return { view: "doc", id: parts[1], mode: parts[2] === "compose" ? "compose" : "document" };
  if (parts[0] === "lector") return { view: "lector" };
  if (parts[0] === "extract") return { view: "extract" };
  if (parts[0] === "salud") return { view: "salud" };
  if (parts[0] === "bandeja") return { view: "bandeja" };
  return { view: "home" };
}

export function hrefFor(route: Route): string {
  if (route.view === "doc") return `#/doc/${encodeURIComponent(route.id)}${route.mode === "compose" ? "/compose" : ""}`;
  if (route.view === "lector") return "#/lector";
  if (route.view === "extract") return "#/extract";
  if (route.view === "salud") return "#/salud";
  if (route.view === "bandeja") return "#/bandeja";
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
