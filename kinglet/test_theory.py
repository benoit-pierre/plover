#!/usr/bin/env python2

import unittest

from kinglet.theory import Stroke, strokes_to_text, strokes_from_text


SAMPLES = (
    ("I'm Zack.", 'AE4RVB,6Y7UI/AEF5B67IK;/QAWS'),

    ("camelCaseVar", '3E4NMUIKL/AE45BUJ8/AER5BH'),

    ("Kinglet's reDONKulous", 'AERFTCVNH7UIKL/35VB,UJI/WS4R5XVHUOP;/AED4R5CVY789/2W3ERF'),

    ("hello", 'WS3E4TBM6Y'),

    ("where have all the flowers gone?", 'Q24RTVBNMY8IO/WER5VYIO/SED4T_BNUI/W4TCHJL;/W3TVNM6H78/QA'),

    ("I prefer 'ck' for Zack, and 'ch' for Zachary. Is that weird?", 'AE4R_BNMH7O/ASTVB,67IK;/1Q3TCVB6YUI/AEF5B67IK;/1Q2WTCVMHUI/1Q345VMYHJI/WR5T_XV6JIO/3EFBHOP/QAWSTXV7U8O/ERTXY9P/34RCBHUP;'),

    ("it's friggin' NUTSO dude!", 'SD5VB,UJI/WGMH7UO;/SFTG_XV67UIL/2W3E5CN6YI;/ERGCVHU8/1Q'),

    ("Oblique anastomosis effected between spatulated upper ureter and renal pelvis.",
     'AE5TCVBNY7KL/145TVY90/WERFN6YIKOL/23RFMUJI/3RTGCVBU8I/Q3ERG_CVBNUK/Q2R,Y8O/24FGCVY79OP/3RG_CVYH79/ASTCVH78IP/WSETCVMHUI/WSTGBY7I/2RBM6UKL/W34F5G'),

    (
        "When most I wink then do mine eyes best see, For all the day they view things unrespected, "
        "But when I sleep, in dreams they look on thee, And darkly bright, are bright in dark directed. "
        "Then thou whose shadow shadows doth make bright How would thy shadow's form, form happy show, "
        "To the clear day with thy much clearer light, When to unseeing eyes thy shade shines so! How would "
        # (
        "I say"
        # )
        " mine eyes be blessed made, By looking on thee in the living day, When in dead night thy fair imperfect shade, "
        "Through heavy sleep on sightless eyes doth stay! All days are nights to see till I see thee, "
        "And nights bright days when dreams do show thee me."
        ,
        'AEFGVBNYHI/WSED5TCN6I/AE4R_CBNYH7UIK;/ERT,Y89O/23TNMYH7U8/ERVBMU8O/E4RFGVUJK/ERFVU9O0P/E4R5CVB6YUI/WE4TBMYIK/'
        '3TCM7OP/ERTVHUJI/Q34RVHJI/ED4RTGVNMUJI/2W3ETGVBNMUJ9/345C,HU9O0P/E4R5CVBN6Y7K/EFGVBNYHI/AE4R_CNY78/34TGXBYL/'
        'ERGVBNM7IKOL/W3TBNUOP/E4TC6YIK;/E45G_BNU8/1Q2WTXV6YH789O/ERGBHIK;/SEDRFG_CVBNHKL/AWFN6HI/WE4G_CVBNHKL/'
        'AWFNYL/ERGBHIK;/ERGMH78I/Q3ERGB,YI;/ED4RF_BN6Y8I9O/EFGVM6Y8O/3TCNJIO/2W35TCBNY8O/W3E4CM6Y9P/W3TCM6YIK/'
        'E4R5TBYUJ8/E4RFGCB7UO;/W3E5_XVJ89/Q2TCBN6Y8I9O/SEDRG_BNHUJI/W3FBHU89/Q2FTGCNYO/QAE4R5TXBYO/QAE4R5T_VM79/'
        '2RFG_CNJ89/Q25G_XV689/ERTVY8I/SEDRBHI/2W34VBMY9P/SDRT_BNHUJI/WSED45TVBJI/3E4TV7OL/WSETBM7UO;/W3E5XBYI;/'
        'Q24RTVNYK/23TCVYH8O/3RCVNH7UI/3RFGVUJI/EDRFG_CNJIO/2W3R_CNJL/3RF_CN6Y0P/E4R5VM6Y9P/EFGC6Y7IKL/2W3T/'
        'AE4R_CN7OP/'
        'E4R5TCVNUI/3RFGVUJI/2WR_CVBNY78/W3RFVHUI/WSED4CMU9O0P/E4R5CVBNHUJI/SED5TCYUJL/AWTCVNMYIK/'
        '3R_CVNYIK/3TBM7U8P/S4RG_CM7OP/1Q2WTXVHJ8IOL/SETCVNY89O/34CMYIL/SD4RGVM6I/EDRFG_CVB7KL/WSETM6Y7U9/ASRTGV67K/'
        'ERFVM789O/35G_XVYUIOL/2345TVNMJI/WS3E4N,HUJI/W34TVU9/E45G_CN7UO;/W3E5BMU8O/W3TVHUJ8/W3TCM6YIK/ERFN7OP/'
        '1QTXV7IKL/SEDTCM7OP/W3TBH7I/SE4RVNMJK/W3TN6YI/W3RVY9OP;/SED4T_XV7UI/W3RVYIK/3RXBYI;/'
        '12RG_VN7UO;/W3E5CNY9O/WSE4RVNMJK/ERGBHUJ8O/EFGVBNYHI/2W34GB6Y7U8O/ERGCY8O/W3E5TCBNYIK/3R_NMUOLP;'
    ),
)


def _strokes(steno):
    return [Stroke(s) for s in steno.split('/')]


class KingletTest(unittest.TestCase):

    def test_single_key_strokes(self):
        stroke_list = _strokes("Q/W/E/R/T/Y/_")
        self.assertNotEqual(strokes_to_text(stroke_list), 'qwerty ')
        self.assertEqual(strokes_to_text(stroke_list, use_keymap=True), 'qwerty ')

    def test_translation(self):
        for text, steno in SAMPLES:
            stroke_list = _strokes(steno)
            cap_state = {
                'shift': False,
                'capslock': False,
            }
            self.assertEqual(strokes_to_text(stroke_list, cap_state=cap_state), text)

    def test_lookup(self):
        for text, steno in SAMPLES:
            stroke_list = strokes_from_text(text)
            cap_state = {
                'shift': False,
                'capslock': False,
            }
            self.assertEqual(strokes_to_text(stroke_list, cap_state=cap_state), text)

