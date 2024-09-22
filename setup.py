from setuptools import setup

setup(
    name= "venv-manager",
    version="1.0",
    py_modules=["venv_manager"],
    entry_points={
        "console_scripts": [
            "vm=venv_manager:main",  # 'pm' is the command to call the tool
        ]
    },
)
