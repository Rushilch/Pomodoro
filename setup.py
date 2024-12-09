from cx_Freeze import setup, Executable

setup(
    name="PomodoroTimer",
    version="1.0",
    description="Pomodoro Timer Application",
    options={'build_exe': {'include_files': ['logo.png', 'arrow.png']}},
    executables=[Executable("Pomodoro.py", base="Win32GUI")]
)
