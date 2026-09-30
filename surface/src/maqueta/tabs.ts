/** Pestañas de la maqueta y su ruta por hash: `#/extraccion`, `#/grafo`, `#/compositor`, con `?atom=<id>`. */
export type MaquetaTab = "extraccion" | "grafo" | "compositor";

export const TABS: [MaquetaTab, string][] = [
  ["extraccion", "Extracción"],
  ["grafo", "Grafo"],
  ["compositor", "Compositor"],
];

export interface MaquetaRoute {
  tab: MaquetaTab;
  focus: string | null;
}

export function parseMaquetaRoute(hash: string): MaquetaRoute {
  const [path = "", query = ""] = hash.replace(/^#\/?/, "").split("?");
  const tab = TABS.find(([id]) => id === path)?.[0] ?? "extraccion";
  return { tab, focus: new URLSearchParams(query).get("atom") };
}

export function maquetaHref(route: MaquetaRoute): string {
  return `#/${route.tab}${route.focus ? `?atom=${encodeURIComponent(route.focus)}` : ""}`;
}
