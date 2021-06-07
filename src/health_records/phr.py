__copyright__ = 'Copyright (C) 2021 Paco Gomez'
__license__ = 'GNU GPLv3'

import click
import sys
from lark import Lark, Transformer, v_args
from decimal import *
from datetime import datetime
from dateutil import parser as dateutil_parser
from tabulate import tabulate
import operator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
import matplotlib.cbook
import numpy as np
import collections

warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

@v_args(inline=True)
class T(Transformer):
    def __init__(self, metrics, records):
        self.metrics = metrics
        self.records = records

    def SIGNED_NUMBER(self, tok):
        return tok.update(value=Decimal(tok))

    def open_directive(self, dir_date, item, unit=None):
        if unit is not None:
            self.metrics[item.value] = Item(key=unit.value, name=unit.value, unit=unit)
        return item

    def record_directive(self, record_date, record_time, narrative, *kwargs):
        entries = list()
        for i in range(0, len(kwargs), 2):
            entries.append(Entry(kwargs[i].value, kwargs[i+1].value))
        self.records.append(Record(record_date, record_time, narrative, entries))
        return None

class FileParser:
    def __init__(self, filename):
        self.filename = filename
        self.metrics = dict()
        self.records = list()

    def parse(self):
        parser = Lark.open_from_package('health_records',
                                        'grammar.lark',
                                        parser='lalr',
                                        transformer=T(self.metrics, self.records),
                                        propagate_positions=True)
        with open(self.filename, 'r') as f:
            parser.parse(f.read())
        self.records = sorted(self.records, key=operator.attrgetter('dt'))

class Item:
    def __init__(self, key, name, unit):
        self.key = key
        self.name = name
        self.unit = unit

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f'{self.key} {self.value}'

    def __eq__(self, other):
        if (isinstance(other, Entry)):
            return self.key == other.key and self.value == other.value
        return false

class Record:
    def __init__(self, rd, rt, narrative, entries):
        self.rd = rd
        self.rt = rt
        self.dt = dateutil_parser.parse(f'{rd} {rt}')
        self.narrative = narrative
        self.entries = entries

    def to_commented(self):
        s = f';{self.dt} r {self.narrative}\n'
        for e in self.entries:
            s += f';  {e}\n'
        return s

    def __str__(self):
        s = f'{self.dt} r {self.narrative}\n'
        for e in self.entries:
            s += f'  {e}\n'
        return s

    def __eq__(self, other):
        if (isinstance(other, Record)):
            return self.dt == other.dt and self.entries == other.entries
        return false

@click.group()
@click.option('-f', '--filename', type=click.Path(exists=True))
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('-q', '--quiet', is_flag=True, default=False)
@click.pass_context
def cli(ctx, filename, config, quiet):
    ctx.ensure_object(dict)
    ctx.obj['filename'] = filename
    if config is not None:
        with open(config) as file:
            ctx.obj['config'] = yaml.load(file, Loader=yaml.FullLoader)
    ctx.obj['quiet'] = quiet
    parser = FileParser(filename)
    parser.parse()
    ctx.obj['parser'] = parser

@click.command('metrics')
@click.argument('filter', required=False)
@click.pass_context
def metrics_cmd(ctx, filter):
    parser = ctx.obj['parser']
    t = list()
    for i in sorted(parser.metrics.items()):
        if not filter or filter in i[0]:
            t.append([i[0], i[1].unit])
    h = ['metric', 'unit']
    click.secho(tabulate(t, headers=h))

@click.command('list')
@click.argument('filter', required=False)
@click.option('-s', '--since', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.pass_context
def list_cmd(ctx, filter, since):
    parser = ctx.obj['parser']
    t = list()
    for r in parser.records:
        if not since or since < r.dt:
            for e in r.entries:
                if not filter or filter in e.key:
                    t.append([r.dt, e.key, e.value, parser.metrics[e.key].unit])
    h = ['date', 'metric', 'value', 'unit']
    t = sorted(t, key=operator.itemgetter(0, 1))
    click.secho(tabulate(t, headers=h))

@click.command('latest')
@click.pass_context
def latest_cmd(ctx):
    click.secho('not implemented', fg='red')

@click.command('delta')
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('-d', '--duplicated', is_flag=True, default=False)
def delta_cmd(ctx, filename, duplicated):
    parser = ctx.obj['parser']
    imp_parser = FileParser(filename)
    imp_parser.parse()
    for r in imp_parser.records:
        if r not in parser.records:
            click.secho(r)
        elif duplicated:
            click.secho(r.to_commented(), fg='yellow')

@click.command('plot')
@click.pass_context
@click.argument('metric', required=True, nargs=-1)
@click.option('-s', '--since', type=click.DateTime(formats=["%Y-%m-%d"]))
def plot_cmd(ctx, metric, since):
    parser = ctx.obj['parser']
    dates = dict()
    data = dict()
    for m in metric:
        if m not in parser.metrics:
            click.secho(f'metric not found {m}')
            return
        dates[m] = list()
        data[m] = list()
    fd = datetime.now()
    ld = datetime.now()
    for r in parser.records:
        if not since or since < r.dt:
            if fd > r.dt: fd = r.dt
            if ld < r.dt: ld = r.dt
            for e in r.entries:
                for m in metric:
                    if m == e.key:
                        dates[m].append(r.dt)
                        data[m].append(e.value)
    if fd != ld:
        delta = ld - fd
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        if delta.days > 365:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        elif delta.days > 31:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        elif delta.days > 10:
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
        for m in metric:
            plt.plot(dates[m], data[m])
        plt.gcf().autofmt_xdate()
        plt.show()

cli.add_command(metrics_cmd)
cli.add_command(list_cmd)
cli.add_command(latest_cmd)
cli.add_command(delta_cmd)
cli.add_command(plot_cmd)

if __name__ == 'health_records.phr':
    cli(obj={}, auto_envvar_prefix='PHR')
