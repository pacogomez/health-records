#!/usr/bin/env python3

import time
import argparse
from stravalib.client import Client
from units.quantity import Quantity

def clean(s):
    return s.strip().replace('\'', '\\\'')

def main() -> None:
    parser: Final = argparse.ArgumentParser(description='Process some input.')
    parser.add_argument(
        '--access-token',
        dest='access_token',
        required=True,
    )
    parser.add_argument(
        '--refresh-token',
        dest='refresh_token',
        required=True,
    )
    parser.add_argument(
        '--since',
        dest='since',
    )

    args: Final = parser.parse_args()
    client = Client()
    client.access_token = args.access_token
    client.refresh_token = args.refresh_token

    athlete = client.get_athlete()

    for a in client.get_activities(after = args.since):
        time.sleep(3)
        activity = client.get_activity(a.id)
        print(f'{activity.start_date.strftime("%Y-%m-%d %I:%M:%S%p")} r \'{clean(activity.name)}\'')
        print(f'  meta.id \'strava-{activity.id}\'')
        print(f'  meta.type \'{activity.type.lower()}\'')
        print(f'  acti.distance.{activity.distance.unit} {activity.distance._num}')
        print(f'  acti.moving.time {activity.moving_time.total_seconds()}')
        print(f'  acti.suffer.score {activity.suffer_score}')
        print(f'  acti.energy.output {activity.kilojoules}')
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

if __name__ == '__main__':
    main()
