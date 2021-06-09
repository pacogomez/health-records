# health-records

This is work in progress and is unfinished.


## data file format


### directives

- open
- close
- record (r)
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

A record directive contains metrics recorded at a particular date and time. Each metric is listed in the directive and implicitly grouped together. The `record` directive uses the letter `r` as the directive id for convenience.

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
meta.date    record date
meta.desc    record description (narration)
meta.line    line of the record in the file

# can be set, user defined with the 'open' directive
meta.id      record identifier
meta.type    type of record
```

record type examples:
```
; blood test, lipid panel
2021-03-01 09:13:00 r 'Blood test, lipids (cholesterol and triglycerides) (LIPID PANEL)'
  meta.id   'epic-21332'
  meta.type 'blood test, lipids'
  body.blood.triglyceride 69
  body.blood.chol.chol 181
  body.blood.chol.hdl 49
  body.blood.chol.t-chol-hdl.ratio 3.8
  body.blood.chol.ldl-calc 117
  body.blood.chol.non-hdl 142


; bike ride
2021-06-08 14:10:47 r 'Morning Ride'
  meta.id 'strava-5435184860'
  meta.type 'ride'
  acti.distance.m 26457.4
  acti.moving.time 3838.0
  acti.suffer.score 98
  acti.energy.output 822.7
  acti.power.average 211.4
  acti.calories 934.4
  acti.heart.rate.average 150.0
  acti.heart.rate.max 167
  acti.country 'United States'
```

## data loading

- apple health
- withins
- strava
- epic
- others

```
./apple.py ...

./strava.py --access-token $ACCESS_TOKEN --refresh-token $REFRESH_TOKEN --after 2021-01-01 --before 2021-06-01 >> strava.phr

./withings.py --consumer-secret <secret> --client-id <client-id> --callback-uri https://test.com --live-data --days 365 >> withings.phr


export PHR_FILENAME=sample.phr
phr delta apple.phr    >> $PHR_FILENAME
phr delta strava.phr   >> $PHR_FILENAME
phr delta withings.phr >> $PHR_FILENAME

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

phr list body.blood.chol -r

# graph metrics
phr plot body.blood.press.dia body.blood.press.sys body.weight --since 2020-01-01

phr plot acti.heart.rate.max acti.heart.rate.average
```

## graphs

To show the plot diagram embedded in the terminal (iTerm):
```
export MPLBACKEND="module://itermplot"
export ITERMPLOT=rv
```
