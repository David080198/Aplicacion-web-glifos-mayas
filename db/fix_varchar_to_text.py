"""
Convierte todas las columnas VARCHAR(N) en init.sql a TEXT.

PostgreSQL no tiene penalización de performance entre VARCHAR(N) y TEXT, 
y TEXT no tiene límite de longitud, lo cual evita errores como 
'value too long for type character varying(255)' cuando los datos 
exceden el límite definido en el esquema MySQL original.
"""

import re
import sys
from pathlib import Path


def convert_varchar_to_text(input_path: Path, output_path: Path) -> int:
    """Convierte varchar(N) -> TEXT. Retorna el numero de reemplazos."""
    content = input_path.read_text(encoding="utf-8")
    
    # Match: varchar(123) o VARCHAR(123) con espacios opcionales
    # Reemplaza por TEXT
    pattern = re.compile(r"\bvarchar\s*\(\s*\d+\s*\)", re.IGNORECASE)
    new_content, count = pattern.subn("TEXT", content)
    
    output_path.write_text(new_content, encoding="utf-8")
    return count


def main() -> None:
    base = Path(__file__).parent
    input_file = base / "init.sql"
    
    if not input_file.exists():
        print(f"ERROR: No existe {input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Sobreescribimos el mismo archivo (es la fuente de verdad)
    count = convert_varchar_to_text(input_file, input_file)
    print(f"OK: {count} columnas VARCHAR(N) convertidas a TEXT en {input_file.name}")


if __name__ == "__main__":
    main()
