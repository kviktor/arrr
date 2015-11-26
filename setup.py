from os import chdir, getcwd, walk
from os.path import join
from setuptools import find_packages, setup


requirements = [line.strip() for line in open('requirements/base.txt', 'r')]

package_root = join('arrr', 'arrr')

def files_in(root_dir, path):
    orig_cwd = getcwd()
    chdir(root_dir)
    result = []
    for dirpath, dirnames, filenames in walk(path):
        result.extend([join(dirpath, fn) for fn in filenames])
    chdir(orig_cwd)
    return result

package_data_list = files_in(package_root, 'templates') + files_in(package_root, 'static')


setup(
    # package metadata
    name="arrr",
    version="1.0.0",
    author="Dudás Ádám, Kálmán Viktor",
    author_email="sir.dudas.adam@gmail.com, viktorvector@gmail.com",
    description="Reserving rooms like a sane person.",
    long_description="TODO: read from README",
    license="See LICENSE.rst.",
    keywords="almighty room reserver reserve book",
    url="https://github.com/kviktor/arrr",
    # package data
    packages=find_packages(where='arrr'),
    package_dir={'arrr': package_root},
    include_package_data=True,
    install_requires=requirements,
    scripts=['arrr/runnarrr'],
    package_data={'arrr': package_data_list},
)
