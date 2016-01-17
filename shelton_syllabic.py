#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

import re

# Required theory constants. {{{

# #ASCTWHNRao*euRNLGCHTSEY
LETTERS = (
    '#',
    'A-', 'S-', 'C-', 'T-', 'W-', 'H-', 'N-', 'R-',
    'a-', 'o-',
    '*',
    '-e', '-u',
    '-R', '-N', '-L', '-G', '-C', '-H', '-T', '-S', '-E', '-Y',
)

IMPLICIT_HYPHEN_LETTERS = ('a-', 'o-', '-e', '-u', '*')

SUFFIX_LETTERS = ()

NUMBER_LETTER = ''

NUMBERS = {}

UNDO_STROKE_STENO = '*'

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

KEYBOARD_KEYMAP = (
    ('A-'        , 'q'),
    ('S-'        , 'a'),
    ('C-'        , 'w'),
    ('T-'        , 's'),
    ('W-'        , 'e'),
    ('H-'        , 'd'),
    ('N-'        , 'r'),
    ('R-'        , 'f'),
    ('a-'        , 'c'),
    ('o-'        , 'v'),
    ('*'         , ('t', 'g', 'y', 'h')),
    ('-e'        , 'n'),
    ('-u'        , 'm'),
    ('-R'        , 'u'),
    ('-N'        , 'j'),
    ('-L'        , 'i'),
    ('-G'        , 'k'),
    ('-C'        , 'o'),
    ('-H'        , 'l'),
    ('-T'        , 'p'),
    ('-S'        , ';'),
    ('-E'        , '['),
    ('-Y'        , '\''),
    ('#'         , ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=')),
    ('no-op'     , ('z', 'x', 'b', ',', '.', '/', '\\')),
    ('arpeggiate', 'space'),
)

# }}}

# Theory implementation. {{{

IMPLICIT_HYPHENS = dict([(l.replace('-', ''), l) for l in IMPLICIT_HYPHEN_LETTERS])

LEFT_COMBOS = '''
		A	S	N	R	AS	AN	AR	SN	SR	NR 	ASN 	ASR 	ANR	SNR 	ASNR 
		a	s	n	r	as	an	ar	sn	ser	l	ann 	arr	al	sl	asl
C	c	ac 	sc	z	cr	asc	anc	acr	ss 	scr	cl	ass	ascr			
T	t	at	st	v	tr	ast	ant	atr	sv	str	qu		astr	aqu 	squ	asqu
W	w	aw	sw	m	wr	ass	am		sm		mr 	asm 		all 		
H	h	ah	sh	y	wh	ash 	ay		sy	shr	ly	asy 			sly	
CT	d 	ad	g	dev 	dr	ag	adv 	adr	gn	gr	del	agn	agr 	acqu	gl	agl 
CW	p	ap	sp	pn	pr	ap	amm	apr		spr	pl	app	appr	apl	spl	appl
CH	ch	ach	sch	cy 	chr		acc	accr			cry			accl	scry	
TW	tw 	att 	x	j		ax	aj	attr		xer 	jer				serv 	
TH	th 	ath		ty	thr	asth 					try			athl 	stry 	
WH	wh	awh		my												
CTW	dw	add		dem 	der	agg	adm	addr			del	adj	aggr 	addl		aggl 
CTH	f	af	gh	dy	fr	agh	aff	afr	gy		fl 	aft	affr	afl		affl
CWH	ph	aph	sph	py	phr	asph 	app	appr			phl	asphy 				
TWH	k	ak	sk 	kn	kr	ask	ackn		xy		kl					
CTWH	b	ab		by	br	abb 	aby 	abr			bl		abbr			
'''

THUMBS_COMBOS = {
    # Vowels.
    'a'  : u'a',
    'ao' : u'io',
    'aoe': u'ee',
    'aou': u'oo',
    'ae' : u'ea',
    'aeu': u'ai',
    'au' : u'au',
    'o'  : u'o',
    'oe' : u'ie',
    'oeu': u'oi',
    'ou' : u'ou',
    'e'  : u'e',
    'eu' : u'i',
    'u'  : u'u',
}

RIGHT_COMBOS = '''
		R	N	T	S	RN	RT	RS	NT	NS	TS	RNT	RNS	RTS	NTS	RNTS
		r	n	t	s	rn	rt	rs	nt	ns	ts	rnt	rns	rts	nts 	mts
L	l	rl	s	lt	ls	ll		rls	st	ss	lts	rst 	lls		sts	rsts 
G	g	rg	ng	k	gs	gn	rk	rgs	nk 	ngs 	ks		gns	rks 	nks 	
C	c	rc	nc	ct	cs			rcs	tion 	nces	d				tions 	
H	h	w	v	th	hs	wn	rth	ws 	nth	ves	ths	wth 	wns	rths	nths 	wths 
LG 	lg		d	kl		dl			sk	ds	kles	lk	dles 		sks 	lks
LC 	p	rp	sp	pt	ps	pl		rps	nst 	sps	pts	lp	ples 		nsts 	lps
LH 	z	wl	sh	lth	zes	lv		wls		shes			lves			
GC 	b	rb	gg	ck	bs	lb	wk	rbs	bt	ggs	cks		lbs	wks 	bts	
GH	gh	rgh	m	ght	ghs	rm		rghs	ngth 	ms	ghts		rms 		ngths 	
CH	ch	rch	nch	tch	d	rv		rches		nches 	tches		rves 			
LGC 	bl	rbl		ckl	bles	bl		rbles			ckles		bles			
LGH 	x	rx	sm	xt	xes	lm			dth	sms	xts		lms 			
LCH	ph	rph		pth	phs	lch		rphs			pths 		lches 			
GCH	f	rf	mb	ft	fs	fl		rfs		mbs	fts 					
LGCH	lf		mp	lk 						mps 	lks 					
'''

COMBOS = {
    # Don't forget last 2 vowels!
    ('-E',): u'e',
    ('-Y',): u'y',
}
MAX_COMBO_LEN = 0

WORD_PARTS = {}
MAX_WORD_PART_LEN = 0


def strokes_to_steno(stroke):
    if isinstance(stroke[0], (tuple, list)):
        return '/'.join(strokes_to_steno(s) for s in stroke)
    left = ''
    middle = ''
    right = ''
    for k in stroke:
        l = k.replace('-', '')
        if k in IMPLICIT_HYPHEN_LETTERS:
            middle += l
        elif '-' == k[0]:
            right += l
        else:
            left += l
    s = left
    if not middle and right:
        s += '-'
    else:
        s += middle
    s += right
    return s

def steno_to_strokes(steno):
    stroke_list = []
    for stroke_steno in steno.split('/'):
        right_index = stroke_steno.find('-')
        if -1 == right_index:
            for implicit_hyphen_letter in IMPLICIT_HYPHENS:
                right_index = stroke_steno.find(implicit_hyphen_letter)
                if -1 != right_index:
                    break
        if -1 == right_index:
            left = steno
            right = ''
        else:
            left = stroke_steno[:right_index]
            right = stroke_steno[right_index:]
        stroke = []
        for letter in left:
            if letter in IMPLICIT_HYPHENS:
                stroke.append(IMPLICIT_HYPHENS[letter])
            else:
                stroke.append(letter + '-')
        for letter in right:
            if '-' == letter:
                pass
            elif letter in IMPLICIT_HYPHENS:
                stroke.append(IMPLICIT_HYPHENS[letter])
            else:
                stroke.append('-' + letter)
        stroke_list.append(tuple(stroke))
    return tuple(stroke_list)

def strokes_weight(stroke):
    if isinstance(stroke[0], (tuple, list)):
        return '/'.join(strokes_weight(s) for s in stroke)
    s = ''
    for l in stroke:
        s += chr(ord('a') + LETTERS.index(l))
    return s

def strokes_to_text(stroke):
    if () == stroke:
        return u''
    if isinstance(stroke[0], (tuple, list)):
        text = u''
        for s in stroke:
            part = strokes_to_text(s)
            text += part
        return text
    text = u''
    while len(stroke) > 0:
        combo = stroke[0:MAX_COMBO_LEN]
        while len(combo) > 0:
            if combo in COMBOS:
                part = COMBOS[combo]
                text += part
                break
            combo = combo[:-1]
        if 0 == len(combo):
            raise ValueError
        assert len(combo) > 0
        stroke = stroke[len(combo):]
    return text

def text_to_strokes(text):
    leftover_text = text
    stroke_list = []
    part_list = []
    stroke = []
    while len(leftover_text) > 0:
        # Find candidate parts.
        combo_list = []
        part = leftover_text[0:MAX_WORD_PART_LEN]
        while len(part) > 0:
            if part in WORD_PARTS:
                combo_list.extend(WORD_PARTS[part])
            part = part[:-1]
        if 0 == len(combo_list):
            return ()
        assert len(combo_list) > 0
        # Prefer combo starting with lowest steno key order.
        combo_list = sorted(combo_list, key=lambda s: LETTERS.index(s[0]))
        # First try to extend current stroke.
        part = None
        if len(stroke) > 0:
            stroke_last_letter_weight = LETTERS.index(stroke[-1])
            for combo in combo_list:
                if stroke_last_letter_weight < LETTERS.index(combo[0]):
                    # Check if we're not changing the translation.
                    wanted = strokes_to_text(tuple(stroke) + combo)
                    result = strokes_to_text(tuple(stroke)) + COMBOS[combo]
                    if wanted != result:
                        continue
                    stroke.extend(combo)
                    part = COMBOS[combo]
                    part_list[-1] += part
                    break
        # Start a new stroke
        if part is None:
            combo = combo_list[0]
            stroke = list(combo)
            stroke_list.append(stroke)
            part = COMBOS[combo]
            part_list.append(part)
        assert len(part) > 0
        leftover_text = leftover_text[len(part):]
    assert len(stroke_list) == len(part_list)
    return tuple(tuple(s) for s in stroke_list)


def build_combos(table, left_not_right):
    cells = [l.split('\t') for l in table.strip('\n').split('\n')]
    assert not cells[0][0]
    header = cells[0][1:]
    for row in cells[1:]:
        middle = row[0]
        for outer, translation in zip(header, row[1:]):
            translation = translation.strip()
            if not translation:
                continue
            steno = middle.strip() + outer.strip()
            if left_not_right:
                steno = steno + '-'
            else:
                steno = '-' + steno
            stroke = steno_to_strokes(steno)
            assert 1 == len(stroke)
            stroke = list(stroke[0])
            stroke.sort(key=lambda k: LETTERS.index(k))
            stroke = tuple(stroke)
            assert stroke not in COMBOS
            COMBOS[stroke] = unicode(translation)

build_combos(LEFT_COMBOS, True)
build_combos(RIGHT_COMBOS, False)
for steno, translation in THUMBS_COMBOS.items():
    strokes = steno_to_strokes(steno)
    assert 1 == len(strokes)
    COMBOS[strokes[0]] = translation
MAX_COMBO_LEN = max(len(combo) for combo in COMBOS)

for combo, part in COMBOS.items():
    if part in WORD_PARTS:
        WORD_PARTS[part] += (combo,)
    else:
        WORD_PARTS[part] = (combo,)
for part, combo_list in WORD_PARTS.items():
    # We want left combos to be given priority over right ones,
    # e.g. 'R-' over '-R' for 'r'.
    combo_list = sorted(combo_list, key=lambda s: strokes_weight(s))
    WORD_PARTS[part] = combo_list
MAX_WORD_PART_LEN = max(len(part) for part in WORD_PARTS.keys())

# }}}

# Required interface for Plover "Python" dictionary. {{{

MAXIMUM_KEY_LENGTH = 1

def lookup_translation(key):
    strokes = []
    for steno in key:
        strokes.extend(steno_to_strokes(steno))
    if len(strokes) > MAXIMUM_KEY_LENGTH:
        raise KeyError()
    strokes = tuple(strokes)
    try:
        text = strokes_to_text(strokes)
    except ValueError:
        raise KeyError
    return '{^%s}' % text

def reverse_lookup(text):
    strokes = text_to_strokes(text)
    if () == strokes:
        return None
    steno = [strokes_to_steno(s) for s in strokes]
    return (steno,)

# }}}

# Main entry-point for testing. {{{

if __name__ == '__main__':
    import sys
    import re
    if '/' == sys.argv[1]:
        text = u''
        # steno -> text.
        for steno in sys.argv[2:]:
            steno = steno.replace('[ ]', '_')
            for part in steno.split('/'):
                if not part:
                    continue
                if '[' == part[0]:
                    assert ']' == part[-1]
                    text += part[1:-2]
                else:
                    strokes = steno_to_strokes(part)
                    text += strokes_to_text(strokes)
        print text
    else:
        # text -> steno.
        supported_chars = set()
        for part in WORD_PARTS:
            supported_chars.update(part)
        assert not set('/[]') & supported_chars
        supported_chars = ''.join(sorted(supported_chars))
        rx = re.compile('([^' + supported_chars.replace('-', '\\-') + ']+)')
        steno = ''
        for text in sys.argv[1:]:
            # No case support for now.
            text = text.lower()
            for part in re.split(rx, text):
                if not part:
                    continue
                if steno:
                    steno += '/'
                if part[0] in supported_chars:
                    strokes = text_to_strokes(part)
                    steno += strokes_to_steno(strokes)
                else:
                    steno += '[' + ']/['.join(part) + ']'
        steno = steno.replace('_', '[ ]')
        print steno

# }}}

# vim: foldmethod=marker ts=8
