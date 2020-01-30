from setuptools import find_packages, setup

setup(
    name='Spotify_part_player',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
    ],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'server': ('static/sass', 'static/css', '/static/css')
    },
    tests_require=[
    ],
)
