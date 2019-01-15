from setuptools import setup

setup(
        name='kiwishot',
        version='1.0',
        author='Sean Dunbar',
        author_email='sean@sdunbar.me',
        url='https://github.com/AJubatus/Kiwishot',
        packages=setuptools.find_packages(),
        entry_points='''
        [console_scripts]
        kiwishot=kiwishot.kiwishot:run_main
        ''',
)
