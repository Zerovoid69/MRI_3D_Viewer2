#!/usr/bin/env python3
"""
Entry point for the MRI 3D Medical Viewer application.

Run with:

    python run.py

See README.md for full installation instructions (Windows + Visual Studio /
VS Code), including how to install PySide6, PyVista/VTK, SimpleITK, nibabel
and pydicom.
"""

from __future__ import annotations

import sys

from app.utils.logging import get_logger, setup_logging


def main() -> int:
    """Configure logging, create the Qt application, and show the main window."""
    setup_logging()
    logger = get_logger(__name__)

    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print(
            "\nPySide6 is not installed, so the MRI 3D Viewer GUI cannot start.\n"
            "Install the project dependencies first, then try again:\n\n"
            "    pip install -r requirements.txt\n\n"
            "See README.md for full Windows installation instructions.\n"
        )
        return 1

    # Imported after the PySide6 check so a missing-dependency message is
    # shown cleanly instead of a raw ImportError traceback.
    from app.gui.main_window import MainWindow
    from app.utils.config import CONFIG

    app = QApplication(sys.argv)
    app.setApplicationName(CONFIG.app_name)
    app.setOrganizationName("MRI 3D Viewer (Educational Project)")

    window = MainWindow()
    window.show()

    logger.info("MRI 3D Viewer started (version %s).", CONFIG.version)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
