/**
 * Raíz de la maqueta (`SLDB_ extracción, grafo y compositor.html`): cabecera con el documento de
 * trabajo y las tres pestañas, y la vista activa debajo. Misma estructura y clases que la maqueta;
 * la diferencia es que los datos y las escrituras van al `sldb serve` real.
 */
import { useCallback, useEffect, useState } from "react";
import { useAtomStore } from "../views/atoms/useAtomStore";
import Compositor from "./views/Compositor";
import Extraccion from "./views/Extraccion";
import Grafo from "./views/Grafo";
import { maquetaHref, parseMaquetaRoute, TABS, type MaquetaTab } from "./tabs";

export function MaquetaApp() {
  const store = useAtomStore();
  const [route, setRoute] = useState(() => parseMaquetaRoute(window.location.hash));
  useEffect(() => {
    const onChange = () => setRoute(parseMaquetaRoute(window.location.hash));
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  const go = useCallback((tab: MaquetaTab, atomId: string | null = null) => {
    window.location.hash = maquetaHref({ tab, focus: atomId });
  }, []);
  const setFocusId = useCallback((id: string | null) => {
    window.history.replaceState(null, "", maquetaHref({ tab: route.tab, focus: id }));
    setRoute((r) => ({ ...r, focus: id }));
  }, [route.tab]);

  const acta = store.actas[0];
  const props = acta ? { store, acta, focusId: route.focus, setFocusId, go } : null;

  return (
    <div className="flex h-full flex-col font-ui text-ink">
      <header className="flex flex-wrap items-center gap-x-6 gap-y-1 border-b border-line bg-panel px-4 pt-2">
        <div className="pb-2 text-[13px]">
          <span className="font-semibold">sldb</span>
          <span className="text-ink2"> / actas / {acta ? acta.path.split("/").pop() : "…"}</span>
        </div>
        <nav className="flex gap-1" aria-label="Vistas">
          {TABS.map(([id, label]) => (
            <button
              key={id}
              onClick={() => go(id, id === "compositor" ? null : route.focus)}
              aria-current={route.tab === id ? "page" : undefined}
              className={`-mb-px border-b-2 px-3 pb-2 pt-1 text-[14px] ${route.tab === id ? "border-ink font-semibold" : "border-transparent text-ink2 hover:text-ink"}`}
            >
              {label}
            </button>
          ))}
        </nav>
      </header>
      <main className="min-h-0 flex-1">
        {store.status === "loading" && !acta && <div className="mq-state" role="status">Cargando…</div>}
        {store.status === "error" && !acta && (
          <div className="mq-error" role="alert">
            No se pudo leer el store: {store.error}. <button onClick={() => void store.reload()}>Reintentar</button>
          </div>
        )}
        {store.status === "ok" && !acta && <div className="mq-state">El store no tiene ningún acta.</div>}
        {props && route.tab === "extraccion" && <Extraccion {...props} />}
        {props && route.tab === "grafo" && <Grafo {...props} />}
        {props && route.tab === "compositor" && <Compositor {...props} />}
      </main>
    </div>
  );
}
