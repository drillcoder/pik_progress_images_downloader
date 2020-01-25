from cx_Freeze import setup, Executable

setup(
    name='pik_parser',
    version='1',
    author='drillcoder',
    executables=[Executable('pik.py')], requires=['requests']
)
