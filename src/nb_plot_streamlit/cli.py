"""
A launcher
"""

import subprocess
import tempfile


def main():
    """Launch a Streamlit app as a command"""

    script = ["from nb_plot_streamlit.ui import draw\n", "draw()\n"]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as file:
        file.writelines(script)
        command = f"yes | streamlit run {file.name}"
        file.flush()
        return subprocess.run(command, shell=True, check=False)


if __name__ == '__main__':
    main()
