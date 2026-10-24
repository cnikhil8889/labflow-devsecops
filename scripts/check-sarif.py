# CNK | Nikhil Kumar Choudavarapu
"""Fail closed on missing reports or actionable SARIF results."""
import json
import sys
from pathlib import Path


def check(directory):
    reports = sorted(Path(directory).glob('*.sarif'))
    if not reports:
        raise ValueError('No SARIF reports were generated')
    findings = []
    for report in reports:
        data = json.loads(report.read_text())
        if data.get('version') != '2.1.0' or not data.get('runs'):
            raise ValueError(f'Invalid or empty SARIF report: {report}')
        for run in data['runs']:
            for invocation in run.get('invocations', []):
                if invocation.get('executionSuccessful') is False:
                    raise ValueError('SARIF reports an unsuccessful analysis')
            rules = {r['id']: r for r in run['tool']['driver'].get('rules', [])}
            for result in run.get('results', []):
                rule = rules.get(result.get('ruleId'), {})
                level = result.get('level', rule.get('defaultConfiguration', {}).get('level', 'warning'))
                if level in ('warning', 'error'):
                    findings.append(result.get('ruleId', 'unknown-rule'))
    print(f'CNK | Checked {len(reports)} SARIF report(s); actionable findings: {len(findings)}')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(check(sys.argv[1]))
