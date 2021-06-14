#!/usr/bin/env python3

import time
import argparse
from stravalib.client import Client
from units.quantity import Quantity
from urllib.parse import urlparse, parse_qs
import sys

def clean(s):
    return s.strip().replace('\'', '\\\'')

def main() -> None:
    parser: Final = argparse.ArgumentParser(description='Process some input.')
    parser.add_argument(
        '--client-id',
        dest='client_id',
        required=False,
    )
    parser.add_argument(
        '--client-secret',
        dest='client_secret',
        required=False,
    )
    parser.add_argument(
        '--access-token',
        dest='access_token',
        required=False,
    )
    parser.add_argument(
        '--refresh-token',
        dest='refresh_token',
        required=False,
    )
    parser.add_argument(
        '--after',
        dest='after',
    )
    parser.add_argument(
        '--before',
        dest='before',
    )

    args: Final = parser.parse_args()
    client = Client()
    if args.client_id is not None:
        authorize_url = client.authorization_url(client_id=args.client_id, redirect_uri='http://localhost:8282/authorized')
        print(authorize_url)
        code_url = input('enter URL with code:')
        o = urlparse(code_url)
        code = parse_qs(o.query)['code']
        token_response = client.exchange_code_for_token(client_id=args.client_id, client_secret=args.client_secret, code=code)
        print(f'export ACCESS_TOKEN={token_response["access_token"]}')
        print(f'export REFRESH_TOKEN={token_response["refresh_token"]}')
    else:
        client.access_token = args.access_token
        client.refresh_token = args.refresh_token

    athlete = client.get_athlete()

    for a in client.get_activities(after = args.after, before = args.before):
        activity = client.get_activity(a.id)
        print(f'{activity.start_date.strftime("%Y-%m-%d %I:%M:%S%p")} r \'{clean(activity.name)}\'')
        print(f'  meta.id \'strava-{activity.id}\'')
        print(f'  meta.type \'{activity.type.lower()}\'')
        print(f'  acti.distance.{activity.distance.unit} {activity.distance._num}')
        print(f'  acti.moving.time {activity.moving_time.total_seconds()}')
        if activity.suffer_score:
            print(f'  acti.suffer.score {activity.suffer_score}')
        if activity.kilojoules:
            print(f'  acti.energy.output {activity.kilojoules}')
        if activity.average_watts:
            print(f'  acti.power.average {activity.average_watts}')
        print(f'  acti.calories {activity.calories}')
        if activity.has_heartrate:
            print(f'  acti.heart.rate.average {activity.average_heartrate}')
            print(f'  acti.heart.rate.max {activity.max_heartrate}')
        if activity.location_city:
            print(f'  acti.city \'{activity.location_city}\'')
        if activity.location_state:
            print(f'  acti.state \'{activity.location_state}\'')
        print(f'  acti.country \'{activity.location_country}\'')
        print('')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
