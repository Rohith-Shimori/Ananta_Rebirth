from features.code_executor import CodeExecutor


def test_execute_python_simple():
    executor = CodeExecutor()
    res = executor.execute_python("print('ok')")
    assert res.get("return_code") == 0
    assert "ok" in res.get("stdout", "")
