# Carpeta Data

Esta carpeta es para tus archivos personales cuando uses Docker.

## Uso

Copia tus archivos de trabajo y CVs aquí:

```powershell
Copy-Item ruta\tu_trabajo.txt data\
Copy-Item ruta\tu_cv.txt data\
```

Luego evalúa con:

```powershell
docker-compose run --rm resume-evaluator --jd /data/tu_trabajo.txt --cv /data/tu_cv.txt
```

## Nota

- Esta carpeta se monta como volumen en Docker
- Los archivos aquí son accesibles desde el contenedor en `/data/`
- No versiones información sensible (CVs reales)
