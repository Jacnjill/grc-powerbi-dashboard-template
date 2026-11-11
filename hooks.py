"""Copy downloadable artefacts into docs/downloads before each MkDocs build."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "docs" / "downloads"


def _copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def on_pre_build(config) -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    copies = [
        ROOT / "sample-data" / "Continual_Improvement_Plan_SAMPLE.xlsx",
        ROOT / "sample-data" / "findings.csv",
        ROOT / "sample-data" / "control_maturity.csv",
        ROOT / "sample-data" / "risk_theme_mapping.csv",
        ROOT / "sample-data" / "owners.csv",
        ROOT / "dax" / "measures.dax",
        ROOT / "theme" / "powerbi-theme.json",
        ROOT / "scripts" / "generate_sample_data.py",
    ]
    for src in copies:
        if not src.exists():
            raise FileNotFoundError(f"Expected downloadable file missing: {src}")
        _copy(src, DEST / src.name)
    _copy(ROOT / "powerquery", DEST / "powerquery")


def on_post_build(config) -> None:
    # Stop GitHub Pages running Jekyll over the already-built MkDocs site.
    site_dir = Path(config["site_dir"])
    (site_dir / ".nojekyll").write_text("")
