# pytest 测试模式参考 (Test Pattern Reference)

> 本文件供 `test` 技能（以及 `code` 技能在 TDD 环节）生成测试用例时参考。

## 标准异步 MCP 工具测试模式

```python
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_get_redmine_example_success():
    """Test successful retrieval of a resource."""
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 1, "subject": "Test Issue"}

    with patch("src.redmine_mcp_server.xxx.client", mock_client):
        result = await get_redmine_example(example_id=1)

    assert result["id"] == 1
    assert "subject" in result
    mock_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_redmine_example_not_found():
    """Test handling of non-existent resource."""
    mock_client = AsyncMock()
    mock_client.get.side_effect = ResourceNotFoundError("Not found")

    with patch("src.redmine_mcp_server.xxx.client", mock_client):
        result = await get_redmine_example(example_id=99999)

    assert "error" in result
```

## 使用 `RealDictCursor` 的数据库测试模式

```python
@pytest.mark.asyncio
async def test_warehouse_query():
    """Test warehouse data retrieval with dict-style access."""
    mock_row = {"sys_id": 1, "subject": "Test", "created_at": "2026-01-01"}
    mock_db = AsyncMock()
    mock_db.fetchone.return_value = mock_row

    result = await some_warehouse_function(db=mock_db, issue_id=1)

    # ✅ 正确：通过列名访问
    assert result["subject"] == "Test"
    # ❌ 禁止：通过索引访问 result[1]
```
