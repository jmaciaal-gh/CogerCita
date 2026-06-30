# CogerCita

Agente modular para automatizar la preparación de cita previa del SEPE en la URL oficial fija:

`https://sede.sepe.gob.es/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo/cita-previa`

## Arquitectura

- `cogercita/config.py`: configuración desacoplada por variables de entorno y valores por defecto.
- `cogercita/agent.py`: orquestación del flujo, validaciones, selección de oficina/canal/trámite y confirmación previa al envío.
- `cogercita/scheduler.py`: lógica de selección de fecha/hora (objetivo +7 días +1 hora y reglas de fallback).
- `cogercita/navigator.py`: interfaz de automatización web para desacoplar drivers.
- `cogercita/playwright_navigator.py`: implementación concreta con selectores robustos y fallback por etiqueta.
- `cogercita/state.py`: gestión de estado conversacional y de ejecución.
- `cogercita/errors.py`: errores de dominio y manejo explícito de casos no permitidos (CAPTCHA/autenticación oficial).
- `cogercita/logging_config.py`: logging estructurado.
- `cogercita/cli.py`: entrada de ejemplo.

## Reglas clave implementadas

- URL del SEPE fija en configuración.
- Datos personales precargados automáticamente con posibilidad de override por variables de entorno.
- Selección estricta de oficina/canal/trámites configurados sin fallback silencioso.
- Selección automática de `AMBOS` para trámite asociado cuando aparece.
- Selección de cita por prioridad:
  1. exacta al objetivo,
  2. primera posterior,
  3. más cercana si no hay posteriores.
- Resumen previo al envío y necesidad de confirmación explícita.
- Detección de CAPTCHA/autenticación oficial para detener el proceso y pedir intervención humana.

## Variables de entorno (opcionales)

- `COGERCITA_DNI`
- `COGERCITA_FULL_NAME`
- `COGERCITA_POSTAL_CODE`
- `COGERCITA_PHONE`
- `COGERCITA_EMAIL`
- `COGERCITA_PROCEDURE_TYPE`
- `COGERCITA_OFFICE_TYPE`
- `COGERCITA_OFFICE`
- `COGERCITA_CHANNEL`
- `COGERCITA_RELATED_CHANNEL`
- `COGERCITA_PROCEDURE`
- `COGERCITA_SUBPROCEDURE`
- `COGERCITA_LINKED_PROCEDURE_CHOICE`
- `COGERCITA_LOAD_TIMEOUT`

## Pruebas

```bash
python -m unittest discover -s tests -v
```

## Ejecución

```bash
python -m cogercita.cli
```

Para automatización real, usa `PlaywrightNavigator` o cualquier implementación compatible de `BrowserNavigator` y conéctala a `SepeAppointmentAgent`.
