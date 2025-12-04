from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='text-to-sparql-llm',
    packages=find_packages(),
    version='0.2.0',
    description='Text-to-SPARQL translation using LLMs with RAG and ACE error correction',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Andrei-Stefan20',
    author_email='your.email@example.com',
    url='https://github.com/Andrei-Stefan20/text-to-sparql-llm',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'google-generativeai>=0.3.0',
        'sentence-transformers>=2.2.0',
        'faiss-cpu>=1.7.4',
        'torch>=2.0.0',
        'transformers>=4.30.0',
        'accelerate>=0.20.0',
        'SPARQLWrapper>=2.0.0',
        'rdflib>=6.3.2',
        'pyparsing>=3.0.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'tqdm>=4.65.0',
        'click>=8.1.0',
        'numpy>=1.24.0',
        'matplotlib>=3.7.0',
        'pandas>=2.0.0',
        'seaborn>=0.12.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
