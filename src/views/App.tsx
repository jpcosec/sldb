/** Composición de la app: navegación + vista según la ruta. */
import { DocumentView } from "./DocumentView";
import { DistillView } from "./DistillView";
import { ExtractionView } from "./ExtractionView";
import { HealthView } from "./HealthView";
import { ReaderView } from "./ReaderView";
import { useRoute } from "./router";
import { Sidebar } from "./Sidebar";
import { TrayView } from "./TrayView";

export function App() {
  const route = useRoute();
  return (
    <div className="app">
      <Sidebar route={route} />
      <div className="app__main">
        {route.view === "doc" && <DocumentView key={route.id} id={route.id} mode={route.mode} />}
        {route.view === "lector" && <ReaderView />}
        {route.view === "destilacion" && <DistillView />}
        {route.view === "extract" && <ExtractionView />}
        {route.view === "salud" && <HealthView />}
        {route.view === "bandeja" && <TrayView />}
        {route.view === "home" && (
          <div className="empty-state empty-state--home">
            <p>Abre un documento a la izquierda para leerlo y editar sus fields, o extrae fields desde un texto crudo.</p>
          </div>
        )}
      </div>
    </div>
  );
}
