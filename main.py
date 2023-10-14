import argparse
import json

from requests import Session, Response
from typing import Optional, Generator


def main(domain: str, api_key: str, search: dict, proxies: Optional[dict] = None) -> Generator[dict, None, None]:
    session = Session()

    headers: dict = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'api-version': 'v1',
        'api-secret-key': api_key,
    }

    # url_params: dict = {
    #     'expand': 'all',
    # }

    body_params: dict = {
        'maxItems': 10,
        'searchCriteria': [search]
    }

    try:
        resp_entity: Response = session.post(
            url=f'https://{domain}/api/computers/search',
            # params=url_params,
            headers=headers,
            json=body_params,
            proxies=proxies,
        )
        resp_entity.raise_for_status()
        data_entity: dict = resp_entity.json()
        resources: list = data_entity.get('computers')
        for resource in resources:
            yield resource
    except Exception as exc_entity:
        print(f'{exc_entity}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--api_key',
        type=str,
        help='The API key',
        required=True,
        default=None
    )
    parser.add_argument(
        '--host_id',
        type=str,
        help='The hostname to query for',
        required=False,
        default=None
    )
    parser.add_argument(
        '--criteria',
        type=str,
        help='The query filter to use to filter the agent ID query results',
        required=False,
        default=None
    )
    parser.add_argument(
        '--domain',
        type=str,
        help="The FQDN for your Deep Security account's API",
        required=False,
        default='app.deepsecurity.trendmicro.com'
    )
    parser.add_argument(
        '--proxies',
        type=str,
        help="JSON structure specifying 'http' and 'https' proxy URLs",
        required=False,
    )
    args = parser.parse_args()

    search_criteria: Optional[dict] = None
    if args.host_id and not args.criteria:
        search_criteria: dict = {
            'idValue': args.host_id,
            'idTest': 'equal',
        }
    elif args.filter:
        search_criteria = args.filter

    proxies: Optional[dict] = None
    if args.proxies:
        proxies = json.loads(args.proxies)

    for device in main(
        domain=args.domain,
        api_key=args.api_key,
        search=search_criteria,
        proxies=proxies
    ):
        print(f'device info: {device}')
    print('End of devices')
