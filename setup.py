import os
from setuptools import (
    setup,
    find_packages,
)


_ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_ROOT_FOLDER, "requirements.txt"), "r") as f:
    _REQUIREMENTS = [x for x in f.readlines()]

with open(os.path.join(_ROOT_FOLDER, "README.md"), "r") as f:
    _LONG_DESCRIPTION = f.read()

_CFG = {}
with open(os.path.join(_ROOT_FOLDER, "lto_node_alerts/__init__.py"), "r") as f:
    exec(f.read(), _CFG)


setup(
    python_requires=">=3.6",
    name=_CFG["__title__"],
    version=_CFG["__version__"],
    author_email=_CFG["__email__"],
    maintainer_email=_CFG["__email__"],
    description=_CFG["__description__"],
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "bot=lto_node_alerts.cli:bot",
            "scheduler=lto_node_alerts.cli:scheduler",
        ],
    },
    install_requires=_REQUIREMENTS,
    zip_safe=False,
    license=_CFG["__license__"],
)
