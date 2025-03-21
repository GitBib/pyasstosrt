import importlib.util
from unittest import mock

import pytest


def test_module_import_error():
    with mock.patch.dict('sys.modules', {'typer': None}):
        with pytest.raises(ImportError) as excinfo:
            spec = importlib.util.find_spec('pyasstosrt.batch')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        
        assert "pyasstosrt was installed without the cli extra" in str(excinfo.value)
