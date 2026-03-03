import pytest
from cobol_parser_mcp import config


def test_load_config_returns_dict_with_required_keys():
    cfg = config.load_config()
    assert isinstance(cfg, dict)
    for key in ("db_path", "macro_library_path", "gitlab_url", "project_name"):
        assert key in cfg, f"Missing required key: {key}"


def test_load_config_via_env_var(tmp_path, monkeypatch):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("db_path: test.sqlite\nmacro_library_path: macros/\n")
    monkeypatch.setenv("BMAD_PROJECT_ROOT", str(tmp_path))
    cfg = config.load_config()
    assert cfg["db_path"] == "test.sqlite"


def test_load_config_raises_on_missing_config(tmp_path, monkeypatch):
    monkeypatch.setenv("BMAD_PROJECT_ROOT", str(tmp_path))
    with pytest.raises((RuntimeError, FileNotFoundError)):
        config.load_config()


def test_load_config_raises_on_malformed_yaml(tmp_path, monkeypatch):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("key: :\n  bad: [unclosed\n")
    monkeypatch.setenv("BMAD_PROJECT_ROOT", str(tmp_path))
    with pytest.raises(RuntimeError, match="malformed"):
        config.load_config()
