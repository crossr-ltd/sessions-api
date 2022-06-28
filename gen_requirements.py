import json


def gen_requirements():
    with open("Pipfile.lock") as fd:
        lock_data = json.load(fd)

        install_requires = []
        for package_name, package_data in lock_data['default'].items():
            if "version" not in package_data:
                raise ValueError(f"Package {package_name} does not have version key: {package_data}")
            install_requires.append(package_name + package_data["version"])
    with open("requirements.txt", mode="wt") as fd:
        fd.write("\n".join(install_requires))


if __name__ == "__main__":
    gen_requirements()
