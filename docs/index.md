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

```
YYYY-MM-DD HH:MM[:SS] [am|pm] <r> <narration> <item> <value> <item> <value> ...
```

example:

```
2021-05-31 10:00 r 'biometrics'
  body.height  70
  body.weight 167
```


#### record types

- body body metrics / measurement
- vacc vaccination event
- proc procedure event
- meds medication prescription / end
- act  activity
- diag diagnostics

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

phr metrics

phr list

phr plot body.blood.press.dia body.blood.press.sys body.weight --since 2020-01-01
```

## graphs

dependencies
- iTerm

```
export MPLBACKEND="module://itermplot"
export ITERMPLOT=rv
```
