/**
 * Raíz de la maqueta (`SLDB_ caso Levira, de fuentes a respuesta.html`): cabecera con el caso y las
 * pestañas (Extracción · Grafo · Compositor · Respuesta) y la vista activa debajo. Misma estructura
 * y clases que la maqueta; los datos y las escrituras van al `sldb serve` real.
 *
 * Sirve a los dos stores demo: el del caso Levira (varias fuentes, informe `SalidaDoc`, respuesta) y
 * el anterior (un acta, sin respuesta: la pestaña Respuesta no aparece).
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import type { Acta, Fuente } from "../core/contract";
import { useAtomStore } from "../views/atoms/useAtomStore";
import Compositor from "./views/Compositor";
import Extraccion from "./views/Extraccion";
import Grafo from "./views/Grafo";
import Respuesta from "./views/Respuesta";
import { maquetaHref, parseMaquetaRoute, TABS, type MaquetaTab } from "./tabs";
import type { ViewProps } from "./ViewProps";

const asActa = (f: Fuente): Acta => ({ id: f.id, gid: f.gid, path: f.path, ...(f.version ? { version: f.version } : {}), title: f.title, body: f.body });

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

  const respuesta = store.respuestas[0];
  const proyecto = useMemo(() => {
    const raw = store.documents.find((d) => d.model_name === "RespuestaDoc")?.payload?.["proyecto"];
    return typeof raw === "string" ? raw : "";
  }, [store.documents]);
  const tabs = TABS.filter(([id]) => id !== "respuesta" || respuesta);
  const first = store.fuentes[0];
  const acta = store.actas[0] ?? (first ? asActa(first) : undefined);
  const props: ViewProps | null = acta
    ? {
        store,
        acta,
        fuentes: store.fuentes,
        informe: store.informes[0],
        respuesta,
        caso: respuesta ? { proyecto: proyecto || "caso", caso: respuesta.caso } : null,
        focusId: route.focus,
        setFocusId,
        go,
      }
    : null;

  return (
    <div className="flex h-full flex-col font-ui text-ink">
      <header className="flex flex-wrap items-center gap-x-6 gap-y-1 border-b border-line bg-panel px-4 pt-2">
        <div className="pb-2 text-[13px]">
          <span className="font-semibold">sldb</span>
          <span className="text-ink2">
            {props?.caso ? ` / ${props.caso.proyecto} / ${props.caso.caso}` : ` / actas / ${acta ? acta.path.split("/").pop() : "…"}`}
          </span>
        </div>
        <nav className="flex gap-1" aria-label="Vistas">
          {tabs.map(([id, label]) => (
            <button
              key={id}
              onClick={() => go(id, id === "compositor" || id === "respuesta" ? null : route.focus)}
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
        {store.status === "ok" && !acta && <div className="mq-state">El store no tiene ninguna fuente de texto.</div>}
        {props && route.tab === "extraccion" && <Extraccion {...props} />}
        {props && route.tab === "grafo" && <Grafo {...props} />}
        {props && route.tab === "compositor" && <Compositor {...props} />}
        {props && route.tab === "respuesta" && <Respuesta {...props} />}
      </main>
    </div>
  );
}
