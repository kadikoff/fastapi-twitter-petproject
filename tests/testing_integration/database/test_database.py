import pytest
from sqlalchemy import inspect

from server.core.models import Base
from tests.conftest import _db_helper


@pytest.mark.asyncio
async def test_tables_created():

    async with _db_helper.engine.connect() as conn:
        table_names = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )

    expected_tables = Base.metadata.tables.keys()

    missing_tables = [
        table for table in expected_tables if table not in table_names
    ]
    assert not missing_tables, f"Tables not created: {missing_tables}"
