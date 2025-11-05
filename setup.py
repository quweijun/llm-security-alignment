from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="llm-security-alignment",
    version="0.1.0",
    author="AI Safety Team",
    author_email="safety@example.com",
    description="Comprehensive security and alignment framework for large language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "llm-security-demo=examples.comprehensive_security_demo:comprehensive_security_demo",
            "llm-red-team=examples.red_teaming_demo:red_teaming_demo",
            "llm-safety-eval=examples.safety_finetuning_demo:safety_evaluation_demo",
        ],
    },
)