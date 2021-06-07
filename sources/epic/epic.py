#!/usr/bin/env python3
from xml.dom import minidom
from dateutil import parser as dateutil_parser
import sys

if len(sys.argv) < 2:
    xmlfile = 'data0001.xml'
else:
    xmlfile = sys.argv[1]

urine_metrics = {
    'color':              'body.urine.color',
    'clarity':            'body.urine.clarity',
    'specific gravity':   'body.urine.specific-gravity',
    'ph':                 'body.urine.ph',
    'glucose, urine':     'body.urine.glucose',
    'bilirubin':          'body.urine.bilirubin',
    'ketones':            'body.urine.ketones',
    'blood':              'body.urine.blood',
    'protein, urine':     'body.urine.protein',
    'nitrite':            'body.urine.nitrite',
    'bacteria':           'body.urine.bacteria',
    'leukocyte esterase': 'body.urine.leukocyte-esterase',
    'wbc':                'body.urine.wbc',
    'rbc':                'body.urine.rbc',
    'squamous epithelial cells': 'body.urine.nitrite',
    'hyaline casts':      'body.urine.hyaline-casts',
    # 'urine, culture':           'body.urine.urine',
}

lipid_metrics = {
    'triglyceride':        'body.blood.triglyceride',
    'cholesterol':         'body.blood.chol.chol',
    'hdl chol':            'body.blood.chol.hdl',
    't chol/hdl ratio':    'body.blood.chol.t-chol-hdl-ratio',
    'ldl calc':            'body.blood.chol.ldl-calc',
    'non hdl cholesterol': 'body.blood.chol.non-hdl',
}

blood_metrics = {
    'glucose':          'body.blood.glucose',
    'bun':              'body.blood.bun',
    'creatinine':       'body.blood.creatinine',
    'bun/creat ratio':  'body.blood.bun-creat-ratio',
    'sodium':           'body.blood.sodium',
    'potassium':        'body.blood.potassium',
    'chloride':         'body.blood.chloride',
    'co2':              'body.blood.co2',
    'calcium':          'body.blood.calcium',
    'total protein':    'body.blood.total-protein',
    'albumin':          'body.blood.albumin',
    'globulins':        'body.blood.globulins',
    'a/g ratio':        'body.blood.a-g-ratio',
    'bilirubin, total': 'body.blood.bilirubin-total',
    'alk phos':         'body.blood.alk-phos',
    'alt (sgpt)':       'body.blood.alt-sgpt',
    'ast (sgot)':       'body.blood.ast-sgot',
    'egfr':             'body.blood.egfr',
    'egfr black':       'body.blood.egfr-black',
}

breath_metrics = {
    'helicobacter pylori (breath)': 'body.breath.helicobacter-pylori',
}

def to_metric(n, s):
    if 'breath test' in n.lower():
        m = breath_metrics
    elif 'COMPREHENSIVE METABOLIC PANEL/EGFR' in n.upper():
        m = blood_metrics
    elif 'lipid panel' in n.lower():
        m = lipid_metrics
    elif 'UA, MICRO, REFLEX TO CULT' in n.upper():
        m = urine_metrics
    else:
        m = dict()
    return m[s.lower()] if s.lower() in m else f';{s}'

doc = minidom.parse(xmlfile)

nodes = doc.getElementsByTagName('item')
for n in nodes:
    if n.getAttribute('ID').startswith('Result'):
        id = n.getAttribute('ID')
        narrative = n.getElementsByTagName('caption')[0].firstChild.nodeValue
        k = list()
        for t in n.getElementsByTagName('td'):
            a = t.getAttribute('ID')
            if a.startswith(id+'Comp') and a.endswith('Name'):
                k.append(t.firstChild.nodeValue)
        v = list()
        for t in n.getElementsByTagName('tr'):
            a = t.getAttribute('ID')
            if a.startswith(id+'Comp'):
                c = t.getElementsByTagName('content')
                if len(c)>0:
                    v.append(c[0].firstChild.nodeValue)
        if len(k)>0:
            a = narrative.split(' - Final result')
            d = dateutil_parser.parse(a[1].strip()[1:-1])
            n = a[0].strip()
            print(f'{d.strftime("%Y-%m-%d %I:%M:%S%p")} r \'{n}\'')
            for i in range(len(k)):
                print(f'  {to_metric(n, k[i])} {v[i]} ;{k[i]}')
