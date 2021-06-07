#!/usr/bin/env python3

# adapted from https://github.com/vangorra/python_withings_api

import argparse
import os
from os import path
import pickle
from typing import cast
from urllib import parse
from datetime import datetime, timedelta
import time

from dateutil import parser as dateutil_parser
import sys

import arrow
from oauthlib.oauth2.rfc6749.errors import MissingTokenError
from typing_extensions import Final
from withings_api import AuthScope, WithingsApi, WithingsAuth
from withings_api.common import CredentialsType, GetSleepField, GetSleepSummaryField, MeasureType, MeasureGetMeasGroupCategory

CREDENTIALS_FILE: Final = path.abspath(
    path.join(path.dirname(path.abspath(__file__)), "./withings-credentials")
)


def save_credentials(credentials: CredentialsType) -> None:
    """Save credentials to a file."""
    print("Saving credentials in:", CREDENTIALS_FILE, file=sys.stderr)
    with open(CREDENTIALS_FILE, "wb") as file_handle:
        pickle.dump(credentials, file_handle)


def load_credentials() -> CredentialsType:
    """Load credentials from a file."""
    print("Using credentials saved in:", CREDENTIALS_FILE, file=sys.stderr)
    with open(CREDENTIALS_FILE, "rb") as file_handle:
        return cast(CredentialsType, pickle.load(file_handle))


def main() -> None:
    """Run main function."""
    parser: Final = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--client-id",
        dest="client_id",
        help="Client id provided by withings.",
        required=True,
    )
    parser.add_argument(
        "--consumer-secret",
        dest="consumer_secret",
        help="Consumer secret provided by withings.",
        required=True,
    )
    parser.add_argument(
        "--callback-uri",
        dest="callback_uri",
        help="Callback URI configured for withings application.",
        required=True,
    )
    parser.add_argument(
        "--live-data",
        dest="live_data",
        action="store_true",
        help="Should we run against live data? (Removal of .credentials file is required before running)",
    )
    parser.add_argument(
        "--days",
        dest="days",
        type=int,
        default=30,
        help="days to download.",
    )

    args: Final = parser.parse_args()

    if path.isfile(CREDENTIALS_FILE):
        print("Attempting to load credentials from:", CREDENTIALS_FILE, file=sys.stderr)
        api = WithingsApi(load_credentials(), refresh_cb=save_credentials)
        try:
            api.user_get_device()
        except MissingTokenError:
            os.remove(CREDENTIALS_FILE)
            print("Credentials in file are expired. Re-starting auth procedure...", file=sys.stderr)

    if not path.isfile(CREDENTIALS_FILE):
        print("Attempting to get credentials...", file=sys.stderr)
        auth: Final = WithingsAuth(
            client_id=args.client_id,
            consumer_secret=args.consumer_secret,
            callback_uri=args.callback_uri,
            mode=None if args.live_data else "demo",
            scope=(
                AuthScope.USER_ACTIVITY,
                AuthScope.USER_METRICS,
                AuthScope.USER_INFO,
                AuthScope.USER_SLEEP_EVENTS,
            ),
        )

        authorize_url: Final = auth.get_authorize_url()
        print("Goto this URL in your browser and authorize:", authorize_url, file=sys.stderr)
        print(
            "Once you are redirected, copy and paste the whole url"
            "(including code) here.", file=sys.stderr
        )
        redirected_uri: Final = input("Provide the entire redirect uri: ")
        redirected_uri_params: Final = dict(
            parse.parse_qsl(parse.urlsplit(redirected_uri).query)
        )
        auth_code: Final = redirected_uri_params["code"]

        print("Getting credentials with auth code", auth_code, file=sys.stderr)
        save_credentials(auth.get_credentials(auth_code))

        api = WithingsApi(load_credentials(), refresh_cb=save_credentials)

    # This only tests the refresh token. Token refresh is handled automatically by the api so you should not
    # need to use this method so long as your code regularly (every 3 hours or so) requests data from withings.
    orig_access_token = api.get_credentials().access_token
    print("Refreshing token...", file=sys.stderr)
    api.refresh_token()
    assert orig_access_token != api.get_credentials().access_token

    n = datetime.now()
    d = n - timedelta(days=args.days)
    s = int(time.mktime(d.timetuple()))

    meas = api.measure_get_meas(
        category=MeasureGetMeasGroupCategory.REAL,
        lastupdate=s,
        startdate=s,
        enddate=int(time.mktime(n.timetuple())),
    )
    t = list()
    p = 2.20462 # pounds in kg
    i = 39.3701 # inches in meter
    n = 0
    for g in meas.measuregrps:
        n += 1
        d = g.date.to(meas.timezone).format('YYYY-MM-DD hh:mm:ssa')
        r = f"{d} r 'import from withings - grp {n}'\n"
        for m in g.measures:
            v = round(m.value * 10 ** m.unit, 2)
            if m.type == MeasureType.WEIGHT:
                k = 'body.weight'
                v = round(v*p, 2)
            elif m.type == MeasureType.FAT_MASS_WEIGHT:
                k = 'body.fat-mass'
                v = round(v*p, 2)
            elif m.type == MeasureType.FAT_FREE_MASS:
                k = 'body.fat-free-mass'
                v = round(v*p, 2)
            elif m.type == MeasureType.FAT_RATIO:
                k = 'body.fat-ratio'
            elif m.type == MeasureType.BONE_MASS:
                k = 'body.bone-mass'
                v = round(v*p, 2)
            elif m.type == MeasureType.MUSCLE_MASS:
                k = 'body.muscle-mass'
                v = round(v*p, 2)
            elif m.type == MeasureType.HYDRATION:
                k = 'body.water'
                v = round(v*p, 2)
            elif m.type == MeasureType.HEART_RATE:
                k = 'body.heart.rate'
            elif m.type == MeasureType.DIASTOLIC_BLOOD_PRESSURE:
                k = 'body.blood.press.dia'
            elif m.type == MeasureType.SYSTOLIC_BLOOD_PRESSURE:
                k = 'body.blood.press.sys'
            elif m.type == MeasureType.HEIGHT:
                k = 'body.height'
                v = round(v*i, 2)
            elif m.type == MeasureType.PULSE_WAVE_VELOCITY:
                k = 'body.heart.pwv'
            else:
                print('*********', file=sys.stderr)
                print(m.type.name, file=sys.stderr)
                print(m, file=sys.stderr)
                continue
            r += f'  {k} {v}\n'
        print(r)


if __name__ == "__main__":
    main()
