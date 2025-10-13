# Fake Danish Person Data API (Python FastAPI)

En Python FastAPI backend til at generere falske danske personoplysninger til test.

## Opsætning

1.  **Installer Python-afhængigheder:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Database:**
    *   Kør `addresses.sql` i din MySQL/MariaDB.
    *   Opret en `.env` og udfyld med dine MySQL-loginoplysninger.
3.  **Navne-data:**
    *   Sørg for, at `data/person-names.json` eksisterer med navnedata.
4.  **Kør serveren:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

API'en kører nu på `http://localhost:8000`.
