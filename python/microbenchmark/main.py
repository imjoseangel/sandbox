import json
from operator import itemgetter
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from collections import defaultdict


def get_domain(addr):
    domain = urlparse(addr)
    return domain.netloc


def count_domains(data):
    result = defaultdict(int)
    for package in data:
        domain = get_domain(package['info']['home_page'])
        result[domain] += 1

    return result


def count_licenses(data):
    result = defaultdict(int)
    for package in data:
        classifiers = package['info'].get('classifiers', '')
        lic = ''
        if classifiers:
            for classifier in classifiers:
                if 'License' in classifier:
                    lic = classifier.split('::')[-1].strip()
                    result[lic] += 1
    return result


def get_top(data, n=10):
    return sorted(data.items(), key=itemgetter(1), reverse=True)[:n]


def main():
    data = json.load(open('pypicache.json'))
    domains = count_domains(data)
    top_domains = get_top(domains, 10)
    licenses = count_licenses(data)
    top_licenses = get_top(licenses, 10)

    # Print result in a table
    table = Table(title="Project domains")
    table.add_column("Domain")
    table.add_column("Count")
    table.add_column("Percentage")

    for domain, count in top_domains:
        table.add_row(str(domain), str(count), str(count/len(data) * 100))

    console = Console()
    console.print(table)

    table = Table(title="Project licenses")
    table.add_column("License")
    table.add_column("Count")
    table.add_column("Percentage")

    for license, count in top_licenses:
        table.add_row(str(license), str(count), str(count/len(data) * 100))

    console.print(table)


if __name__ == "__main__":
    main()
