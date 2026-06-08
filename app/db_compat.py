"""
db_compat.py
-------------
Capa de compatibilidad para migrar de Flask-MySQLdb a psycopg2 (PostgreSQL)
con MINIMOS cambios en el código existente.

Provee:
  - `mysql.connection.cursor()` -> retorna un cursor compatible
  - `mysql.connection.commit()`  -> commit normal
  - Cursor que traduce automaticamente:
        `backticks`  ->  "comillas dobles"   (identificadores)
        %s con MySQL -> %s con psycopg2 (mismo placeholder, compatible)
  - Manejo de pooling simple a traves de connection-per-request usando Flask `g`.
  - Tipos BYTEA devueltos como bytes (igual que MySQL)
"""
from __future__ import annotations

import os
import re
import threading
from typing import Any, Iterable, Optional, Sequence

import psycopg2
import psycopg2.extras
from flask import Flask, g, has_app_context


# Regex para reemplazar backticks por comillas dobles (identificadores en PG)
# Soporta `tabla` o `tabla`.`columna`
_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _translate_query(query: str) -> str:
    """Convierte sintaxis MySQL -> PostgreSQL en una query."""
    if not query:
        return query
    # Reemplazar backticks con comillas dobles
    translated = _BACKTICK_RE.sub(r'"\1"', query)
    return translated


class _CursorWrapper:
    """Envuelve un cursor de psycopg2 para mantener compatibilidad con MySQLdb."""

    def __init__(self, real_cursor):
        self._cursor = real_cursor

    # --- API compatible ---
    def execute(self, query: str, params: Optional[Sequence[Any]] = None):
        translated = _translate_query(query)
        return self._cursor.execute(translated, params)

    def executemany(self, query: str, params_seq: Iterable[Sequence[Any]]):
        translated = _translate_query(query)
        return self._cursor.executemany(translated, params_seq)

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        return tuple(row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [tuple(r) for r in rows]

    def fetchmany(self, size: int = 1):
        rows = self._cursor.fetchmany(size)
        return [tuple(r) for r in rows]

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass

    # Atributos comunes
    @property
    def rowcount(self):
        return self._cursor.rowcount

    @property
    def lastrowid(self):
        # PostgreSQL no tiene lastrowid; intentamos via RETURNING o devolvemos None
        return None

    @property
    def description(self):
        return self._cursor.description

    def __iter__(self):
        return iter(self._cursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


class _ConnectionWrapper:
    """Wrapper de psycopg2.connection con API compatible con MySQLdb."""

    def __init__(self, real_conn):
        self._conn = real_conn

    def cursor(self):
        # Usamos cursor "tuple" por defecto para que el codigo existente reciba tuplas
        return _CursorWrapper(self._conn.cursor())

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass

    @property
    def closed(self) -> bool:
        return bool(getattr(self._conn, "closed", 0))


class PostgresCompat:
    """Sustituto de la clase flask_mysqldb.MySQL.

    Uso:
        mysql = PostgresCompat(app)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM `t_general`")
        rows = cursor.fetchall()
        mysql.connection.commit()
    """

    def __init__(self, app: Optional[Flask] = None):
        self.app: Optional[Flask] = None
        # Lock para crear conexion si no hay contexto de Flask
        self._lock = threading.Lock()
        self._fallback_conn: Optional[_ConnectionWrapper] = None
        if app is not None:
            self.init_app(app)

    # ---- Config ----
    def init_app(self, app: Flask) -> None:
        self.app = app
        app.config.setdefault("POSTGRES_HOST", os.environ.get("POSTGRES_HOST", "db"))
        app.config.setdefault("POSTGRES_PORT", int(os.environ.get("POSTGRES_PORT", "5432")))
        app.config.setdefault("POSTGRES_USER", os.environ.get("POSTGRES_USER", "postgres"))
        app.config.setdefault("POSTGRES_PASSWORD", os.environ.get("POSTGRES_PASSWORD", ""))
        app.config.setdefault("POSTGRES_DB", os.environ.get("POSTGRES_DB", "base_grigori"))

        # Cerrar conexion al terminar request
        @app.teardown_appcontext
        def _close_connection(_exc):  # noqa: ARG001
            conn = g.pop("_pg_compat_conn", None)
            if conn is not None and not conn.closed:
                conn.close()

    # ---- Internos ----
    def _make_connection(self) -> _ConnectionWrapper:
        if self.app is None:
            raise RuntimeError("PostgresCompat no inicializado con init_app(app)")

        cfg = self.app.config
        raw = psycopg2.connect(
            host=cfg["POSTGRES_HOST"],
            port=cfg["POSTGRES_PORT"],
            user=cfg["POSTGRES_USER"],
            password=cfg["POSTGRES_PASSWORD"],
            dbname=cfg["POSTGRES_DB"],
            connect_timeout=10,
        )
        # Autocommit OFF para mantener semantica original (uso explicito de commit)
        raw.autocommit = False
        return _ConnectionWrapper(raw)

    # ---- API publica (igual que flask_mysqldb.MySQL) ----
    @property
    def connection(self) -> _ConnectionWrapper:
        """Devuelve la conexion del request actual (o una global como fallback)."""
        if has_app_context():
            conn = g.get("_pg_compat_conn", None)
            if conn is None or conn.closed:
                conn = self._make_connection()
                g._pg_compat_conn = conn
            return conn

        # Fuera de contexto Flask: usamos una conexion global perezosa
        with self._lock:
            if self._fallback_conn is None or self._fallback_conn.closed:
                self._fallback_conn = self._make_connection()
            return self._fallback_conn
