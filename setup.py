"""Build distributions

To build `python setup.py sdist --formats=gztar bdist_wheel --universal`
"""
import os
from setuptools import setup
import requests
import json


# RELEASES_URL = (
#     'https://api.github.com/repos/open-traffic-generator/models/releases'
# )

# response = requests.request('GET', RELEASES_URL, allow_redirects=True)
# assert response.status_code == 200
# releases = json.loads(response.content)
# # get latest release from v0.1.x branch
# MODELS_RELEASES = [r['tag_name'] for r in releases if 'v0.1.' in r['tag_name']]

# OPENAPI_URL = (
#     'https://github.com/open-traffic-generator/models/releases/download/%s'
#     '/openapi.yaml'
# ) % MODELS_RELEASES[0]

# response = requests.request('GET', OPENAPI_URL, allow_redirects=True)
# assert response.status_code == 200

# # put the downloaded file inside docs dir of package
# doc_dir = './snappi_trex/docs'
# if os.path.exists(doc_dir) is False:
#     os.mkdir(doc_dir)
# with open(os.path.join(doc_dir, 'openapi.yaml'), 'wb') as fp:
#     fp.write(response.content)

# read long description and version number
pkg_name = 'snappi_trex'
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'README.md')) as fid:
    long_description = fid.read()
with open(os.path.join(base_dir, 'VERSION')) as fid:
    version_number = fid.read()

setup(
    name=pkg_name,
    version=version_number,
    description='The TRex Open Traffic Generator Python Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/open-traffic-generator',
    author='fredpower44',
    author_email='frederick.zhang@keysight.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='TRex testing open traffic generator automation',
    packages=[pkg_name],
    include_package_data=True,
    python_requires='>=3, <4',
    install_requires=[],
    extras_require={
        'dev': [
            'snappi==0.3.20',
            'pytest',
            'flake8==3.8.4',
            'dpkt==1.9.4',
        ]
    }
)
