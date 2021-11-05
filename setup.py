"""A Streamlit sample
based on
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='nb_plot_streamlit',
    version='0.0.1',
    description='A sample Streamlit app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zettsu-t/nbinomPlotPy',
    author='Zettsu Tatsuya',
    author_email='zettsu.tatsuya@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='streamlit, sample, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9, <4',
    install_requires=['matplotlib', 'numpy', 'pandas',
                      'scipy', 'streamlit', 'pyyaml'],
    extras_require={
        'dev': ['autopep8', 'check-manifest', 'flake8', 'mypy', 'pep8',
                'pipenv', 'pylint', 'py_pkg',
                'sphinx', 'sphinx_rtd_theme',
                'types-PyYAML', 'types-requests'],
        'test': ['chromedriver-binary-auto', 'coverage', 'opencv-python',
                 'pytest', 'pytest-cov', 'seleniumbase'],
    },

    package_data={
        'config': ['config/config.yml'],
    },

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/zettsu-t/nbinomPlotPy/issues',
        'Source': 'https://github.com/zettsu-t/nbinomPlotPy',
    },
)
