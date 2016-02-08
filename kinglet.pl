#!/usr/bin/perl -w

use strict;

my $word = shift;

# convert caps to use the 'caps' chord, including the doubled 'allcaps' variant
$word =~ s/([A-Z][A-Z]+)/||\L$1|/g;
$word =~ s/([A-Z])/|\L$1/g;

my @letters = split '', $word;

my @alpha = ();

# left ring and little fingers
$alpha[0]{' '}  = "E";
$alpha[0]{'e'}  = "3";
$alpha[0]{'t'}  = "D";
$alpha[0]{'a'}  = "WE";
$alpha[0]{'o'}  = "23";
$alpha[0]{'i'}  = "SD";
$alpha[0]{'n'}  = "SE";
$alpha[0]{'s'}  = "W3";
$alpha[0]{'r'}  = "WSE";
$alpha[0]{'h'}  = "W3E";
$alpha[0]{'l'}  = "SED";
$alpha[0]{'d'}  = "2W3";
$alpha[0]{'c'}  = "3E";
$alpha[0]{'th'} = "ED";
$alpha[0]{'u'}  = "2W3E";
$alpha[0]{'m'}  = "WSED";
$alpha[0]{'he'} = "WS3E";
$alpha[0]{'f'}  = "W";
$alpha[0]{'p'}  = "2";
$alpha[0]{'in'} = "S";
$alpha[0]{'g'}  = "AW";
$alpha[0]{'w'}  = "Q2";
$alpha[0]{'y'}  = "QW";
$alpha[0]{'er'} = "AS";
$alpha[0]{'an'} = "12";
$alpha[0]{'b'}  = "2W";
$alpha[0]{'re'} = "WS";
$alpha[0]{'on'} = "QAW";
$alpha[0]{'at'} = "Q2W";
$alpha[0]{'en'} = "AWS";
$alpha[0]{'nd'} = "1Q2";
$alpha[0]{'ti'} = "QA2W";
$alpha[0]{','}  = "1Q2W";
$alpha[0]{'.'}  = "QAWS";
$alpha[0]{'|'}  = "AE";
$alpha[0]{'v'}  = "Q3";
$alpha[0]{'or'} = "QAE";
$alpha[0]{'te'} = "Q3E";
$alpha[0]{'k'}  = "AED";
$alpha[0]{"'"}  = "1Q3";
$alpha[0]{'"'}  = "QA3E";
$alpha[0]{'-'}  = "QE";
$alpha[0]{'x'}  = "AD";
$alpha[0]{'j'}  = "Q";
$alpha[0]{'q'}  = "1";
$alpha[0]{'z'}  = "A";
$alpha[0]{'!'}  = "1Q";
$alpha[0]{'?'}  = "QA";

# left fore and middle fingers
$alpha[1]{' '}  = "T";
$alpha[1]{'e'}  = "R";
$alpha[1]{'t'}  = "5";
$alpha[1]{'a'}  = "4";
$alpha[1]{'o'}  = "5T";
$alpha[1]{'i'}  = "4R";
$alpha[1]{'n'}  = "TG";
$alpha[1]{'s'}  = "RF";
$alpha[1]{'r'}  = "G";
$alpha[1]{'h'}  = "F";
$alpha[1]{'l'}  = "4T";
$alpha[1]{'d'}  = "RG";
$alpha[1]{'c'}  = "45";
$alpha[1]{'th'} = "RT";
$alpha[1]{'u'}  = "45T";
$alpha[1]{'m'}  = "4R5T";
$alpha[1]{'he'} = "4RT";
$alpha[1]{'f'}  = "RTG";
$alpha[1]{'p'}  = "4TG";
$alpha[1]{'in'} = "4RTG";
$alpha[1]{'g'}  = "4RG";
$alpha[1]{'w'}  = "FG";
$alpha[1]{'y'}  = "RFG";
$alpha[1]{'er'} = "RFTG";
$alpha[1]{'an'} = "45TG";
$alpha[1]{'b'}  = "4RFG";
$alpha[1]{'re'} = "4G";
$alpha[1]{'on'} = "45G";
$alpha[1]{'at'} = "4FG";
$alpha[1]{'en'} = "4RF";
$alpha[1]{'nd'} = "5TG";
$alpha[1]{'ti'} = "4F";
$alpha[1]{','}  = "5G";
$alpha[1]{'.'}  = "4F5G";
$alpha[1]{'|'}  = "4R5";
$alpha[1]{'v'}  = "R5";
$alpha[1]{'or'} = "R5T";
$alpha[1]{'te'} = "FT";
$alpha[1]{'k'}  = "RFT";
$alpha[1]{"'"}  = "FTG";
$alpha[1]{'"'}  = "RF5T";
$alpha[1]{'-'}  = "RF5";
$alpha[1]{'x'}  = "4RF5";
$alpha[1]{"j"}  = "F5T";
$alpha[1]{'q'}  = "F5TG";
$alpha[1]{'z'}  = "F5";
$alpha[1]{'!'}  = "4F5";
$alpha[1]{'?'}  = "F5G";

# thumbs
$alpha[2]{'a'} = "B";
$alpha[2]{'b'} = "CVBN";
$alpha[2]{'c'} = "VB";
$alpha[2]{'d'} = "CM";
$alpha[2]{'e'} = "V";
$alpha[2]{'f'} = "CVB";
$alpha[2]{'g'} = "VNM";
$alpha[2]{'h'} = "VM";
$alpha[2]{'i'} = "M";
$alpha[2]{'j'} = "NM,";
$alpha[2]{'k'} = "XBN";
$alpha[2]{'l'} = "BM";
$alpha[2]{'m'} = "NM";
$alpha[2]{'n'} = "VN";
$alpha[2]{'o'} = "C";
$alpha[2]{'p'} = "BNM";
$alpha[2]{'q'} = "XNM";
$alpha[2]{'r'} = "CB";
$alpha[2]{'s'} = "CN";
$alpha[2]{'t'} = "N";
$alpha[2]{'u'} = "CV";
$alpha[2]{'v'} = "N,";
$alpha[2]{'w'} = "CBN";
$alpha[2]{'x'} = "XCV";
$alpha[2]{'y'} = "VBM";
$alpha[2]{'z'} = "CV,";
$alpha[2]{'an'} = "CVM";
$alpha[2]{'at'} = "X";
$alpha[2]{'en'} = ",";
$alpha[2]{'er'} = "CNM";
$alpha[2]{'he'} = "VBN";
$alpha[2]{'in'} = "CVN";
$alpha[2]{"nd"} = "XN";
$alpha[2]{'on'} = "CVNM";
$alpha[2]{'or'} = "XM";
$alpha[2]{'re'} = "VBNM";
$alpha[2]{'te'} = "C,";
$alpha[2]{'th'} = "BN";
$alpha[2]{'ti'} = "V,";
$alpha[2]{'-'} = "BN,";
$alpha[2]{'!'} = "XC";
$alpha[2]{'"'} = "XVB";
$alpha[2]{','} = "XB";
$alpha[2]{'.'} = "B,";
$alpha[2]{'?'} = "M,";
$alpha[2]{"'"} = "VB,";
$alpha[2]{'|'} = "XV"; # cap chord
$alpha[2]{' '} = "[ ]";

# thumbs with space preceding
$alpha[2]{' a'} = "[ ]B";
$alpha[2]{' b'} = "[ ]CVBN";
$alpha[2]{' c'} = "[ ]VB";
$alpha[2]{' d'} = "[ ]CM";
$alpha[2]{' e'} = "[ ]V";
$alpha[2]{' f'} = "[ ]CVB";
$alpha[2]{' g'} = "[ ]VNM";
$alpha[2]{' h'} = "[ ]VM";
$alpha[2]{' i'} = "[ ]M";
$alpha[2]{' j'} = "[ ]NM,";
$alpha[2]{' k'} = "[ ]XBN";
$alpha[2]{' l'} = "[ ]BM";
$alpha[2]{' m'} = "[ ]NM";
$alpha[2]{' n'} = "[ ]VN";
$alpha[2]{' o'} = "[ ]C";
$alpha[2]{' p'} = "[ ]BNM";
$alpha[2]{' q'} = "[ ]XNM";
$alpha[2]{' r'} = "[ ]CB";
$alpha[2]{' s'} = "[ ]CN";
$alpha[2]{' t'} = "[ ]N";
$alpha[2]{' u'} = "[ ]CV";
$alpha[2]{' v'} = "[ ]N,";
$alpha[2]{' w'} = "[ ]CBN";
$alpha[2]{' x'} = "[ ]XCV";
$alpha[2]{' y'} = "[ ]VBM";
$alpha[2]{' z'} = "[ ]CV,";
$alpha[2]{' an'} = "[ ]CVM";
$alpha[2]{' at'} = "[ ]X";
$alpha[2]{' en'} = "[ ],";
$alpha[2]{' er'} = "[ ]CNM";
$alpha[2]{' he'} = "[ ]VBN";
$alpha[2]{' in'} = "[ ]CVN";
$alpha[2]{" nd"} = "[ ]XN";
$alpha[2]{' on'} = "[ ]CVNM";
$alpha[2]{' or'} = "[ ]XM";
$alpha[2]{' re'} = "[ ]VBNM";
$alpha[2]{' te'} = "[ ]C,";
$alpha[2]{' th'} = "[ ]BN";
$alpha[2]{' ti'} = "[ ]V,";
$alpha[2]{' -'} = "[ ]BN,";
$alpha[2]{' !'} = "[ ]XC";
$alpha[2]{' "'} = "[ ]XVB";
$alpha[2]{' ,'} = "[ ]XB";
$alpha[2]{' .'} = "[ ]B,";
$alpha[2]{' ?'} = "[ ]M,";
$alpha[2]{" '"} = "[ ]VB,";
$alpha[2]{' |'} = "[ ]XV"; # space plus cap chord

# right fore and middle fingers
$alpha[3]{' '}  = "Y";
$alpha[3]{'e'}  = "U";
$alpha[3]{'t'}  = "6";
$alpha[3]{'a'}  = "7";
$alpha[3]{'o'}  = "6Y";
$alpha[3]{'i'}  = "7U";
$alpha[3]{'n'}  = "YH";
$alpha[3]{'s'}  = "UJ";
$alpha[3]{'r'}  = "H";
$alpha[3]{'h'}  = "J";
$alpha[3]{'l'}  = "Y7";
$alpha[3]{'d'}  = "HU";
$alpha[3]{'c'}  = "67";
$alpha[3]{'th'} = "YU";
$alpha[3]{'u'}  = "6Y7";
$alpha[3]{'m'}  = "6Y7U";
$alpha[3]{'he'} = "Y7U";
$alpha[3]{'f'}  = "YHU";
$alpha[3]{'p'}  = "YH7";
$alpha[3]{'in'} = "YH7U";
$alpha[3]{'g'}  = "H7U";
$alpha[3]{'w'}  = "HJ";
$alpha[3]{'y'}  = "HUJ";
$alpha[3]{'er'} = "YHUJ";
$alpha[3]{'an'} = "6YH7";
$alpha[3]{'b'}  = "H7UJ";
$alpha[3]{'re'} = "H7";
$alpha[3]{'on'} = "6H7";
$alpha[3]{'at'} = "H7J";
$alpha[3]{'en'} = "7UJ";
$alpha[3]{'nd'} = "6YH";
$alpha[3]{'ti'} = "7J";
$alpha[3]{','}  = "6H";
$alpha[3]{'.'}  = "6H7J";
$alpha[3]{'|'}  = "67U";
$alpha[3]{'v' } = "6U";
$alpha[3]{'or'} = "6YU";
$alpha[3]{'te'} = "YJ";
$alpha[3]{'k'}  = "YUJ";
$alpha[3]{"'"}  = "YHJ";
$alpha[3]{'"'}  = "6YUJ";
$alpha[3]{'-'}  = "6UJ";
$alpha[3]{'x'}  = "67UJ";
$alpha[3]{"j"}  = "6YJ";
$alpha[3]{'q'}  = "6YHJ";
$alpha[3]{'z'}  = "6J";
$alpha[3]{'!'}  = "67J";
$alpha[3]{'?'}  = "6HJ";

# right third and little fingers
$alpha[4]{' '}  = "I";
$alpha[4]{'e'}  = "8";
$alpha[4]{'t'}  = "K";
$alpha[4]{'a'}  = "IO";
$alpha[4]{'o'}  = "89";
$alpha[4]{'i'}  = "KL";
$alpha[4]{'n'}  = "IL";
$alpha[4]{'s'}  = "8O";
$alpha[4]{'r'}  = "IOL";
$alpha[4]{'h'}  = "8IO";
$alpha[4]{'l'}  = "IKL";
$alpha[4]{'d'}  = "89O";
$alpha[4]{'c'}  = "8I";
$alpha[4]{'th'} = "IK";
$alpha[4]{'u'}  = "8I9O";
$alpha[4]{'m'}  = "IKOL";
$alpha[4]{'he'} = "8IOL";
$alpha[4]{'f'}  = "O";
$alpha[4]{'p'}  = "9";
$alpha[4]{'in'} = "L";
$alpha[4]{'g'}  = "O;";
$alpha[4]{'w'}  = "9P";
$alpha[4]{'y'}  = "OP";
$alpha[4]{'er'} = "L;";
$alpha[4]{'an'} = "90";
$alpha[4]{'b'}  = "9O";
$alpha[4]{'re'} = "OL";
$alpha[4]{'on'} = "OP;";
$alpha[4]{'at'} = "9OP";
$alpha[4]{'en'} = "OL;";
$alpha[4]{'nd'} = "90P";
$alpha[4]{'ti'} = "9OP;";
$alpha[4]{','}  = "9O0P";
$alpha[4]{'.'}  = "OLP;";
$alpha[4]{'|'}  = "I;";
$alpha[4]{'v'}  = "8P";
$alpha[4]{'or'} = "IP;";
$alpha[4]{'te'} = "8IP";
$alpha[4]{'k'}  = "IK;";
$alpha[4]{"'"}  = "80P";
$alpha[4]{'"'}  = "8IP;";
$alpha[4]{'-'}  = "IP";
$alpha[4]{'x'}  = "K;";
$alpha[4]{"j"}  = "P";
$alpha[4]{'q'}  = "0";
$alpha[4]{'z'}  = ";";
$alpha[4]{'!'}  = "0P";
$alpha[4]{'?'}  = "P;";

my $count = 0;
my $letterCount = 0;
my $fingerPairs = 0;
my $wordCount = 1 + $word =~ tr/ //;
my $strokeCount = 1;
while() {

    if(exists($letters[$letterCount+2]) && exists($alpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]$letters[$letterCount+2]"})) {
        # if a three-character combo exists in the lookup table for the current
        # slow, use the chord for that.
        print $alpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]$letters[$letterCount+2]"};
        $letterCount+=3;
        $fingerPairs++;

    }
    elsif(exists($letters[$letterCount+1]) && exists($alpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]"})) {
        # if a two-character combo exists in the lookup table for the current
        # slow, use the chord for that.
        print $alpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]"};
        $letterCount+=2;
        $fingerPairs++;
    }
    elsif(exists($letters[$letterCount]) && exists($alpha[$count]{$letters[$letterCount]})) {
        # otherwise if the current symbol exists in the lookup table, use the
        # chord for that.
        print $alpha[$count]{$letters[$letterCount]};
        $letterCount++;
        $fingerPairs++;
    }
    elsif($letterCount > $#letters) {
        # if there's no match, but it's because we've run out of letters, then
        # we're done
        last;
    }
    else {
        # if there's no match, but we still need to type a character, use QWERTY
        print "/[$letters[$letterCount]]/";
        $count = 0;
        $letterCount++;
        next;
    }

    if($count == 4) {
        print "/";
        $strokeCount++;
    }
    $count = ($count+1)%5;
}

print "\nchars per stroke: " . int(($letterCount/$fingerPairs*5)*100+.5)/100 . "\n";
print "strokes per word: " . int($strokeCount/$wordCount*100+.5)/100 . "\n";

