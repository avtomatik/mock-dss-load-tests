SECONDS_TO_MILLISECONDS = 1000

QUERY_DATE = "2025-12-04"

SQL_SELECT_COUNT = """
SELECT count(*)
FROM signatures
WHERE DATE(signed_at) = %s;
"""

SQL_INSERT_DOCUMENT = """
INSERT INTO documents (document_id, content, created_at)
VALUES (%s, %s, NOW());
"""
