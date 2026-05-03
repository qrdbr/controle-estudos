import sqlite3
from typing import Any, Dict, List, Optional, Tuple

class ControlRepository:
    """
    Repositório SQLite enxuto para operações CRUD nas tabelas trilha, curso e atividades_estudo.
    """
    def __init__(self, db_path: str = "controle_estudos.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trilha (
                    id_trilha INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao_trilha TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS curso (
                    id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_trilha INTEGER NOT NULL,
                    descricao_curso TEXT NOT NULL,
                    FOREIGN KEY (id_trilha) REFERENCES trilha(id_trilha)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS atividades_estudo (
                    id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_curso INTEGER NOT NULL,
                    descricao_atividade TEXT NOT NULL,
                    estudo_concluido INTEGER NOT NULL DEFAULT 0,
                    revisao_finalizada INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
                )
            """)
            conn.commit()

    # --- Trilhas ---
    def create_trilha(self, descricao_trilha: str) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO trilha (descricao_trilha) VALUES (?)", (descricao_trilha,))
            conn.commit()
            return cur.lastrowid

    def list_trilhas(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_trilha, descricao_trilha FROM trilha")
            return [
                {"id_trilha": row[0], "descricao_trilha": row[1]}
                for row in cur.fetchall()
            ]

    def get_trilha_by_id(self, id_trilha: int) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_trilha, descricao_trilha FROM trilha WHERE id_trilha = ?", (id_trilha,))
            row = cur.fetchone()
            if row:
                return {"id_trilha": row[0], "descricao_trilha": row[1]}
            return None

    def update_trilha(self, id_trilha: int, descricao_trilha: str) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE trilha SET descricao_trilha = ? WHERE id_trilha = ?", (descricao_trilha, id_trilha))
            conn.commit()
            return cur.rowcount > 0

    def delete_trilha(self, id_trilha: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM trilha WHERE id_trilha = ?", (id_trilha,))
            conn.commit()
            return cur.rowcount > 0

    # --- Cursos ---
    def create_curso(self, descricao_curso: str, id_trilha: int) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO curso (descricao_curso, id_trilha) VALUES (?, ?)", (descricao_curso, id_trilha))
            conn.commit()
            return cur.lastrowid

    def list_cursos(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_curso, id_trilha, descricao_curso FROM curso")
            return [
                {"id_curso": row[0], "id_trilha": row[1], "descricao_curso": row[2]}
                for row in cur.fetchall()
            ]

    def get_curso_by_id(self, id_curso: int) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_curso, id_trilha, descricao_curso FROM curso WHERE id_curso = ?", (id_curso,))
            row = cur.fetchone()
            if row:
                return {"id_curso": row[0], "id_trilha": row[1], "descricao_curso": row[2]}
            return None

    def update_curso(self, id_curso: int, descricao_curso: str, id_trilha: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE curso SET descricao_curso = ?, id_trilha = ? WHERE id_curso = ?", (descricao_curso, id_trilha, id_curso))
            conn.commit()
            return cur.rowcount > 0

    def delete_curso(self, id_curso: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM curso WHERE id_curso = ?", (id_curso,))
            conn.commit()
            return cur.rowcount > 0

    # --- Atividades de Estudo ---
    def create_atividade(self, descricao_atividade: str, id_curso: int, estudo_concluido: bool = False, revisao_finalizada: bool = False) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO atividades_estudo (descricao_atividade, id_curso, estudo_concluido, revisao_finalizada) VALUES (?, ?, ?, ?)",
                (descricao_atividade, id_curso, int(estudo_concluido), int(revisao_finalizada))
            )
            conn.commit()
            return cur.lastrowid

    def list_atividades(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_atividade, id_curso, descricao_atividade, estudo_concluido, revisao_finalizada FROM atividades_estudo")
            return [
                {
                    "id_atividade": row[0],
                    "id_curso": row[1],
                    "descricao_atividade": row[2],
                    "estudo_concluido": bool(row[3]),
                    "revisao_finalizada": bool(row[4])
                }
                for row in cur.fetchall()
            ]

    def get_atividade_by_id(self, id_atividade: int) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_atividade, id_curso, descricao_atividade, estudo_concluido, revisao_finalizada FROM atividades_estudo WHERE id_atividade = ?", (id_atividade,))
            row = cur.fetchone()
            if row:
                return {
                    "id_atividade": row[0],
                    "id_curso": row[1],
                    "descricao_atividade": row[2],
                    "estudo_concluido": bool(row[3]),
                    "revisao_finalizada": bool(row[4])
                }
            return None

    def update_atividade(self, id_atividade: int, descricao_atividade: str, id_curso: int, estudo_concluido: bool, revisao_finalizada: bool) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE atividades_estudo SET descricao_atividade = ?, id_curso = ?, estudo_concluido = ?, revisao_finalizada = ? WHERE id_atividade = ?",
                (descricao_atividade, id_curso, int(estudo_concluido), int(revisao_finalizada), id_atividade)
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_atividade(self, id_atividade: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM atividades_estudo WHERE id_atividade = ?", (id_atividade,))
            conn.commit()
            return cur.rowcount > 0
