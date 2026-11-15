"""`DEPLOYMENT_ENDS`: los extremos que admite cada conexión de despliegue."""

from __future__ import annotations

# extremos que admite cada tipo de conexion de despliegue (origen, destino); communication entre
# artefactos se mantiene por compatibilidad, UML la define entre nodos
DEPLOYMENT_ENDS = {
    "communication": {("node", "node"), ("artifact", "artifact")},
    "deploy": {("artifact", "node")},
    "manifest": {("artifact", "node"), ("artifact", "artifact")},
}
