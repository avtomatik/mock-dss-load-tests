# =============================================================================
# General
# =============================================================================
SECONDS_TO_MILLISECONDS = 1000

QUERY_DATE = "2025-12-04"


# =============================================================================
# Pre-defined SQL Queries
# =============================================================================
SQL_SELECT_COUNT = """
SELECT count(*)
FROM signatures
WHERE DATE(signed_at) = %s;
"""

SQL_INSERT_DOCUMENT = """
INSERT INTO documents (document_id, content, created_at)
VALUES (%s, %s, NOW());
"""


# =============================================================================
# Logging
# =============================================================================
LOG_FILENAME = "locust_test_logs.log"
LOG_MAX_SIZE = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5
LOG_FORMAT_DETAILED = "%(asctime)s - %(levelname)s - %(message)s"
