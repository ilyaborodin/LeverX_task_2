import functools
import re


@functools.total_ordering
class Version:
    def __init__(self, version):
        self.version = version
        self.splitted_version_this = self._get_list_from_version(self.version)

    def __eq__(self, other):
        splitted_version_this = self.splitted_version_this
        splitted_version_other = self._get_list_from_version(other.version)
        return splitted_version_this == splitted_version_other

    def __lt__(self, other):
        splitted_version_this = self.splitted_version_this
        splitted_version_other = self._get_list_from_version(other.version)
        splitted_version_this += ["-"]
        splitted_version_other += ["-"]
        priority_list = ["a", "b", "r", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        rez = False
        for index in range(0, len(splitted_version_this)):
            if splitted_version_this[index] == splitted_version_other[index]:
                continue
            if splitted_version_this[index].isdigit() and splitted_version_other[index].isdigit():
                rez = int(splitted_version_this[index]) < int(splitted_version_other[index])
                break
            rez = priority_list.index(splitted_version_this[index][0]) < \
                  priority_list.index(splitted_version_other[index][0])
            break
        return rez

    def _get_list_from_version(self, str_version: str) -> list:
        return re.findall(r"\d{1,}|(?<![a-zA-Z])[a-zA-Z]", str_version)


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()
