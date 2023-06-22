import json
import subprocess
import pybadges


def get_coverage_attributes():
    subprocess.check_output(['coverage',
                             'json',
                             '-q',
                             '-o',
                             'coverage.json'])
    with open('coverage.json', 'r') as file_pointer:
        data = json.load(file_pointer)
    return data


def get_percentage(cov_output):
    return cov_output['totals']['percent_covered_display']


def create_coverage_badge(percentage):
    if 80 <= int(percentage) <= 100:
        color = 'green'
    elif 50 <= int(percentage) <= 79:
        color = 'yellow'
    else:
        color = 'red'

    badge_svg = pybadges.badge(left_text='coverage',
                               right_text=f"{str(percentage)}%",
                               right_color=color)
    with open('coverage_badge.svg', 'w') as file_pointer:
        file_pointer.write(badge_svg)


if __name__ == '__main__':
    coverage = get_coverage_attributes()
    percentage = get_percentage(coverage)
    create_coverage_badge(percentage)
