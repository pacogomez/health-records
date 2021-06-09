# health-records

This is work in progress and is unfinished.


## data file format


### directives

- open
- close
- record
- range


#### open directive

```
YYYY-MM-DD <open> <item> [units]
```

example:

```
1999-01-21 open body.height in
1999-01-21 open body.weight lb
```

#### record directive

A record directive contains metrics recorded at a particular date and time. Each metric is listed in the directive and implicitly grouped together.

```
YYYY-MM-DD HH:MM[:SS] [am|pm] <r> <narration> <item> <value> <item> <value> ...
```

example:

```
2021-05-31 10:00 r 'biometrics'
  body.height  70
  body.weight 167
```


#### metric types

- body body metrics / measurement
- vacc vaccination event
- proc procedure event
- meds medication prescription / end
- acti activity
- diag diagnostics
- meta metadata about the record itself

##### metadata

`meta` is a special metric that contains information about the record itself, and applies to all the metrics in the record

```
# from first line, auto generated and reserved
meta.date             record date
meta.desc             record description (narration)
meta.line             line of the record in the file

# can be set, user defined with the 'open' directive
meta.id          record identifier
meta.type        type of record
```

record type examples:
```
meta.id   'epic-21332'
meta.type 'blood test, lipids'

meta.id   'strava-39203'
meta.type 'run'
```

## data loading

- apple health
- withins
- strava
- epic
- others

```
./withings.py --consumer-secret <secret> --client-id <client-id> --callback-uri https://test.com --live-data --days 365 > records.phr
```

```
export PHR_FILENAME=sample.phr
phr delta ~/prj/health-records/sources/withings/records.phr >> $PHR_FILENAME
```

## calculated measurements

BMI

## commands

```
export PHR_FILENAME=sample.phr

# list metric declaration
phr metrics

# list metric measurements
phr list

# list records
phr list -r

# graph metrics
phr plot body.blood.press.dia body.blood.press.sys body.weight --since 2020-01-01
```

## graphs

dependencies
- iTerm

```
export MPLBACKEND="module://itermplot"
export ITERMPLOT=rv
```
