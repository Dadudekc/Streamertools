from setuptools import setup, find_packages

setup(
    name="MeTuber",
    version="1.0.0",
    description="A Python-based library for webcam threading and artistic effects.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/metuber",  # Replace with the actual URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opencv-python",
        "numpy",
        "PyQt5",
        "pyvirtualcam",
        "av",
        "pytest",
        "pytest-cov",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "metuber=MeTuber.__main__:main",
        ]
    },
)