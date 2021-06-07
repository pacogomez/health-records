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
    'urine, culture':     'body.urine.culture',
    'mucus':     'body.urine.mucus',
    'urobilinogen':     'body.urine.urobilinogen',

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
    'agap':             'body.blood.agap',
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
    'hemoglobin a1c %': 'body.blood.hemoglobin-a1c',
    'tsh, 3rd generation': 'body.blood.tsh-3g',
    'wbc': 'body.blood.wbc',
    'rbc': 'body.blood.rbc',
    'nrbc, percent': 'body.blood.nrbc-pct',
    'hgb': 'body.blood.hgb',
    'hct': 'body.blood.hct',
    'mcv': 'body.blood.mcv',
    'mch': 'body.blood.mch',
    'mchc': 'body.blood.mchc',
    'rdw': 'body.blood.rdw',
    'rdw - sd': 'body.blood.rdw-sd',
    'mpv': 'body.blood.mpv',
    'platelet count': 'body.blood.platelet-count',
    'neut %': 'body.blood.neut-pct',
    'lymph %': 'body.blood.lymph-pct',
    'mono %': 'body.blood.mono-pct',
    'eos %': 'body.blood.eos-pct',
    'basophils': 'body.blood.basophils',
    'neut abs': 'body.blood.neut-abs',
    'lymph abs': 'body.blood.lymph-abs',
    'mono abs': 'body.blood.mono-abs',
    'eos abs': 'body.blood.eos-abs',
    'baso abs': 'body.blood.baso-abs',
    'vitamin d, 25-oh total': 'body.blood.vitamin-d-25-oh',
    'prostate specific antigen (psa)': 'body.blood.psa',
    'psa, free': 'body.blood.psa-free',
    'free psa': 'body.blood.free-psa',
    'iga': 'body.blood.iga',
    'igg': 'body.blood.igg',
    'igm': 'body.blood.igm',
}

breath_metrics = {
    'helicobacter pylori (breath)': 'body.breath.helicobacter-pylori',
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_metric(n, s):
    if 'breath test' in n.lower():
        m = breath_metrics
    elif 'COMPREHENSIVE METABOLIC PANEL/EGFR' in n.upper() or \
        'HEMOGLOBIN A1C' in n.upper() or \
        'VITAMIN D, 25 OH' in n.upper() or \
        'TSH' in n.upper() or \
        'CBC WITH DIFFERENTIAL' in n.upper() or \
        'PSA TOTAL' in n.upper() or \
        'PROSTATE SPECIFIC ANTIGEN' in n.upper() or \
        'IMMUNOFIXATION' in n.upper():
        m = blood_metrics
    elif 'lipid panel' in n.lower():
        m = lipid_metrics
    elif 'UA, MICRO, REFLEX TO CULT' in n.upper() or \
        'URINALYSIS,COMPLETE WITH REFLEX TO CULTURE' in n.upper():
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
            has_metric = False
            for i in range(len(k)):
                if not to_metric(n, k[i]).startswith(';'):
                    has_metric = True
            if has_metric:
                print(f'{d.strftime("%Y-%m-%d %I:%M:%S%p")} r \'{n}\'')
                for i in range(len(k)):
                    m = v[i] if is_number(v[i]) else f"'{v[i]}'"
                    print(f'  {to_metric(n, k[i])} {m} ;{k[i]}')
