/** Rutas por hash: #/doc/<id>, #/doc/<id>/compose, #/extract. */
import { useEffect, useState } from "react";

export type Route = { view: "home" } | { view: "doc"; id: string; mode: "document" | "compose" } | { view: "extract" };

export function parseRoute(hash: string): Route {
  const parts = hash.replace(/^#\/?/, "").split("/").map(decodeURIComponent);
  if (parts[0] === "doc" && parts[1]) return { view: "doc", id: parts[1], mode: parts[2] === "compose" ? "compose" : "document" };
  if (parts[0] === "extract") return { view: "extract" };
  return { view: "home" };
}

export function hrefFor(route: Route): string {
  if (route.view === "doc") return `#/doc/${encodeURIComponent(route.id)}${route.mode === "compose" ? "/compose" : ""}`;
  return route.view === "extract" ? "#/extract" : "#/";
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
