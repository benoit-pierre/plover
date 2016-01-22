#!/usr/bin/perl -w

use strict;

my $word = shift;

# convert caps to use the 'caps' chord, including the doubled 'allcaps' variant
$word =~ s/([A-Z][A-Z]+)/||\L$1|/g;
$word =~ s/([A-Z])/|\L$1/g;

my @letters = split '', $word;

my @sixalpha = ();

# left ring and little fingers
$sixalpha[0]{' '} = "E";
$sixalpha[0]{'e'} = "W";
$sixalpha[0]{'t'} = "3";
$sixalpha[0]{'a'} = "D";
$sixalpha[0]{'o'} = "2";
$sixalpha[0]{'i'} = "S";
$sixalpha[0]{'n'} = "WE";
$sixalpha[0]{'s'} = "23";
$sixalpha[0]{'r'} = "SD";
$sixalpha[0]{'h'} = "SE";
$sixalpha[0]{'l'} = "2E";
$sixalpha[0]{'d'} = "W3";
$sixalpha[0]{'c'} = "WD";
$sixalpha[0]{'th'} = "3E";
$sixalpha[0]{'u'} = "ED";
$sixalpha[0]{'m'} = "2W";
$sixalpha[0]{'he'} = "WS";
$sixalpha[0]{'f'} = "2W3E";
$sixalpha[0]{'p'} = "WSED";
$sixalpha[0]{'in'} = "W3E";
$sixalpha[0]{'g'} = "23E";
$sixalpha[0]{'w'} = "SED";
$sixalpha[0]{'y'} = "WED";
$sixalpha[0]{'er'} = "2W3";
$sixalpha[0]{'an'} = "2WE";
$sixalpha[0]{'b'} = "WSE";
$sixalpha[0]{'re'} = "WSD";
$sixalpha[0]{'on'} = "WS3E";
$sixalpha[0]{'at'} = "2WED";
$sixalpha[0]{'en'} = "2WS";
$sixalpha[0]{'nd'} = "3ED";
$sixalpha[0]{'ti'} = "WS3";
$sixalpha[0]{','} = "2ED";
$sixalpha[0]{'.'} = "S3E";
$sixalpha[0]{'|'} = "2WD";
$sixalpha[0]{'v'} = "2WS3";
$sixalpha[0]{'or'} = "23ED";
$sixalpha[0]{'te'} = "S3ED";
$sixalpha[0]{'k'} = "2WSD";
$sixalpha[0]{"'"} = "2S";
$sixalpha[0]{'"'} = "3D";
$sixalpha[0]{'-'} = "S3";
$sixalpha[0]{'x'} = "2D";
$sixalpha[0]{'j'} = "2S3";
$sixalpha[0]{'q'} = "23D";
$sixalpha[0]{'z'} = "S3D";
$sixalpha[0]{'!'} = "2SD";
$sixalpha[0]{'?'} = "2S3D";

# left fore and middle fingers
$sixalpha[1]{' '} = "T";
$sixalpha[1]{'e'} = "R";
$sixalpha[1]{'t'} = "5";
$sixalpha[1]{'a'} = "G";
$sixalpha[1]{'o'} = "4";
$sixalpha[1]{'i'} = "F";
$sixalpha[1]{'n'} = "RT";
$sixalpha[1]{'s'} = "45";
$sixalpha[1]{'r'} = "FG";
$sixalpha[1]{'h'} = "FT";
$sixalpha[1]{'l'} = "4T";
$sixalpha[1]{'d'} = "R5";
$sixalpha[1]{'c'} = "RG";
$sixalpha[1]{'th'} = "5T";
$sixalpha[1]{'u'} = "TG";
$sixalpha[1]{'m'} = "4R";
$sixalpha[1]{'he'} = "RF";
$sixalpha[1]{'f'} = "4R5T";
$sixalpha[1]{'p'} = "RFTG";
$sixalpha[1]{'in'} = "R5T";
$sixalpha[1]{'g'} = "45T";
$sixalpha[1]{'w'} = "FTG";
$sixalpha[1]{'y'} = "RTG";
$sixalpha[1]{'er'} = "4R5";
$sixalpha[1]{'an'} = "4RT";
$sixalpha[1]{'b'} = "RFT";
$sixalpha[1]{'re'} = "RFG";
$sixalpha[1]{'on'} = "RF5T";
$sixalpha[1]{'at'} = "4RTG";
$sixalpha[1]{'en'} = "4RF";
$sixalpha[1]{'nd'} = "5TG";
$sixalpha[1]{'ti'} = "RF5";
$sixalpha[1]{','} = "4TG";
$sixalpha[1]{'.'} = "F5T";
$sixalpha[1]{'|'} = "4RG";
$sixalpha[1]{'v'} = "4RF5";
$sixalpha[1]{'or'} = "45TG";
$sixalpha[1]{'te'} = "F5TG";
$sixalpha[1]{'k'} = "4RFG";
$sixalpha[1]{"'"} = "4F";
$sixalpha[1]{'"'} = "5G";
$sixalpha[1]{'-'} = "F5";
$sixalpha[1]{'x'} = "4G";
$sixalpha[1]{"j"} = "4F5";
$sixalpha[1]{'q'} = "45G";
$sixalpha[1]{'z'} = "F5G";
$sixalpha[1]{'!'} = "4FG";
$sixalpha[1]{'?'} = "4F5G";

# thumbs
$sixalpha[2]{'a'} = "B";
$sixalpha[2]{'b'} = "CVBN";
$sixalpha[2]{'c'} = "VB";
$sixalpha[2]{'d'} = "CM";
$sixalpha[2]{'e'} = "V";
$sixalpha[2]{'f'} = "CVB";
$sixalpha[2]{'g'} = "VNM";
$sixalpha[2]{'h'} = "VM";
$sixalpha[2]{'i'} = "M";
$sixalpha[2]{'j'} = "NM,";
$sixalpha[2]{'k'} = "XBN";
$sixalpha[2]{'l'} = "BM";
$sixalpha[2]{'m'} = "NM";
$sixalpha[2]{'n'} = "VN";
$sixalpha[2]{'o'} = "C";
$sixalpha[2]{'p'} = "BNM";
$sixalpha[2]{'q'} = "XNM";
$sixalpha[2]{'r'} = "CB";
$sixalpha[2]{'s'} = "CN";
$sixalpha[2]{'t'} = "N";
$sixalpha[2]{'u'} = "CV";
$sixalpha[2]{'v'} = "N,";
$sixalpha[2]{'w'} = "CBN";
$sixalpha[2]{'x'} = "XCV";
$sixalpha[2]{'y'} = "VBM";
$sixalpha[2]{'z'} = "CV,";
$sixalpha[2]{'an'} = "CVM";
$sixalpha[2]{'at'} = "X";
$sixalpha[2]{'en'} = ",";
$sixalpha[2]{'er'} = "CNM";
$sixalpha[2]{'he'} = "VBN";
$sixalpha[2]{'in'} = "CVN";
$sixalpha[2]{"nd"} = "XN";
$sixalpha[2]{'on'} = "CVNM";
$sixalpha[2]{'or'} = "XM";
$sixalpha[2]{'re'} = "VBNM";
$sixalpha[2]{'te'} = "C,";
$sixalpha[2]{'th'} = "BN";
$sixalpha[2]{'ti'} = "V,";
$sixalpha[2]{'-'} = "BN,";
$sixalpha[2]{'!'} = "XC";
$sixalpha[2]{'"'} = "XVB";
$sixalpha[2]{','} = "XB";
$sixalpha[2]{'.'} = "B,";
$sixalpha[2]{'?'} = "M,";
$sixalpha[2]{"'"} = "VB,";
$sixalpha[2]{'|'} = "XV"; # cap chord
$sixalpha[2]{' '} = "[ ]";

# thumbs with space preceding
$sixalpha[2]{' a'} = "[ ]B";
$sixalpha[2]{' b'} = "[ ]CVBN";
$sixalpha[2]{' c'} = "[ ]VB";
$sixalpha[2]{' d'} = "[ ]CM";
$sixalpha[2]{' e'} = "[ ]V";
$sixalpha[2]{' f'} = "[ ]CVB";
$sixalpha[2]{' g'} = "[ ]VNM";
$sixalpha[2]{' h'} = "[ ]VM";
$sixalpha[2]{' i'} = "[ ]M";
$sixalpha[2]{' j'} = "[ ]NM,";
$sixalpha[2]{' k'} = "[ ]XBN";
$sixalpha[2]{' l'} = "[ ]BM";
$sixalpha[2]{' m'} = "[ ]NM";
$sixalpha[2]{' n'} = "[ ]VN";
$sixalpha[2]{' o'} = "[ ]C";
$sixalpha[2]{' p'} = "[ ]BNM";
$sixalpha[2]{' q'} = "[ ]XNM";
$sixalpha[2]{' r'} = "[ ]CB";
$sixalpha[2]{' s'} = "[ ]CN";
$sixalpha[2]{' t'} = "[ ]N";
$sixalpha[2]{' u'} = "[ ]CV";
$sixalpha[2]{' v'} = "[ ]N,";
$sixalpha[2]{' w'} = "[ ]CBN";
$sixalpha[2]{' x'} = "[ ]XCV";
$sixalpha[2]{' y'} = "[ ]VBM";
$sixalpha[2]{' z'} = "[ ]CV,";
$sixalpha[2]{' an'} = "[ ]CVM";
$sixalpha[2]{' at'} = "[ ]X";
$sixalpha[2]{' en'} = "[ ],";
$sixalpha[2]{' er'} = "[ ]CNM";
$sixalpha[2]{' he'} = "[ ]VBN";
$sixalpha[2]{' in'} = "[ ]CVN";
$sixalpha[2]{" nd"} = "[ ]XN";
$sixalpha[2]{' on'} = "[ ]CVNM";
$sixalpha[2]{' or'} = "[ ]XM";
$sixalpha[2]{' re'} = "[ ]VBNM";
$sixalpha[2]{' te'} = "[ ]C,";
$sixalpha[2]{' th'} = "[ ]BN";
$sixalpha[2]{' ti'} = "[ ]V,";
$sixalpha[2]{' -'} = "[ ]BN,";
$sixalpha[2]{' !'} = "[ ]XC";
$sixalpha[2]{' "'} = "[ ]XVB";
$sixalpha[2]{' ,'} = "[ ]XB";
$sixalpha[2]{' .'} = "[ ]B,";
$sixalpha[2]{' ?'} = "[ ]M,";
$sixalpha[2]{" '"} = "[ ]VB,";
$sixalpha[2]{' |'} = "[ ]XV"; # space plus cap chord

# right fore and middle fingers
$sixalpha[3]{' '} = "Y";
$sixalpha[3]{'e'} = "U";
$sixalpha[3]{'t'} = "6";
$sixalpha[3]{'a'} = "H";
$sixalpha[3]{'o'} = "7";
$sixalpha[3]{'i'} = "J";
$sixalpha[3]{'n'} = "YU";
$sixalpha[3]{'s'} = "67";
$sixalpha[3]{'r'} = "HJ";
$sixalpha[3]{'h'} = "YJ";
$sixalpha[3]{'l'} = "Y7";
$sixalpha[3]{'d'} = "6U";
$sixalpha[3]{'c'} = "HU";
$sixalpha[3]{'th'} = "6Y";
$sixalpha[3]{'u'} = "YH";
$sixalpha[3]{'m'} = "7U";
$sixalpha[3]{'he'} = "UJ";
$sixalpha[3]{'f'} = "6Y7U";
$sixalpha[3]{'p'} = "YHUJ";
$sixalpha[3]{'in'} = "6YU";
$sixalpha[3]{'g'} = "6Y7";
$sixalpha[3]{'w'} = "YHJ";
$sixalpha[3]{'y'} = "YHU";
$sixalpha[3]{'er'} = "67U";
$sixalpha[3]{'an'} = "Y7U";
$sixalpha[3]{'b'} = "YUJ";
$sixalpha[3]{'re'} = "HUJ";
$sixalpha[3]{'on'} = "6YUJ";
$sixalpha[3]{'at'} = "YH7U";
$sixalpha[3]{'en'} = "7UJ";
$sixalpha[3]{'nd'} = "6YH";
$sixalpha[3]{'ti'} = "6UJ";
$sixalpha[3]{','} = "YH7";
$sixalpha[3]{'.'} = "6YJ";
$sixalpha[3]{'|'} = "H7U";
$sixalpha[3]{'v'} = "67UJ";
$sixalpha[3]{'or'} = "6YH7";
$sixalpha[3]{'te'} = "6YHJ";
$sixalpha[3]{'k'} = "H7UJ";
$sixalpha[3]{"'"} = "7J";
$sixalpha[3]{'"'} = "6H";
$sixalpha[3]{'-'} = "6J";
$sixalpha[3]{'x'} = "H7";
$sixalpha[3]{"j"} = "67J";
$sixalpha[3]{'q'} = "6H7";
$sixalpha[3]{'z'} = "6HJ";
$sixalpha[3]{'!'} = "H7J";
$sixalpha[3]{'?'} = "6H7J";

# right third and little fingers
$sixalpha[4]{' '} = "I";
$sixalpha[4]{'e'} = "O";
$sixalpha[4]{'t'} = "8";
$sixalpha[4]{'a'} = "K";
$sixalpha[4]{'o'} = "9";
$sixalpha[4]{'i'} = "L";
$sixalpha[4]{'n'} = "IO";
$sixalpha[4]{'s'} = "89";
$sixalpha[4]{'r'} = "KL";
$sixalpha[4]{'h'} = "IL";
$sixalpha[4]{'l'} = "I9";
$sixalpha[4]{'d'} = "8O";
$sixalpha[4]{'c'} = "KO";
$sixalpha[4]{'th'} = "8I";
$sixalpha[4]{'u'} = "IK";
$sixalpha[4]{'m'} = "9O";
$sixalpha[4]{'he'} = "OL";
$sixalpha[4]{'f'} = "8I9O";
$sixalpha[4]{'p'} = "IKOL";
$sixalpha[4]{'in'} = "8IO";
$sixalpha[4]{'g'} = "8I9";
$sixalpha[4]{'w'} = "IKL";
$sixalpha[4]{'y'} = "IKO";
$sixalpha[4]{'er'} = "89O";
$sixalpha[4]{'an'} = "I9O";
$sixalpha[4]{'b'} = "IOL";
$sixalpha[4]{'re'} = "KOL";
$sixalpha[4]{'on'} = "8IOL";
$sixalpha[4]{'at'} = "IK9O";
$sixalpha[4]{'en'} = "9OL";
$sixalpha[4]{'nd'} = "8IK";
$sixalpha[4]{'ti'} = "8OL";
$sixalpha[4]{','} = "IK9";
$sixalpha[4]{'.'} = "8IL";
$sixalpha[4]{'|'} = "K9O";
$sixalpha[4]{'v'} = "89OL";
$sixalpha[4]{'or'} = "8IK9";
$sixalpha[4]{'te'} = "8IKL";
$sixalpha[4]{'k'} = "K9OL";
$sixalpha[4]{"'"} = "9L";
$sixalpha[4]{'"'} = "8K";
$sixalpha[4]{'-'} = "8L";
$sixalpha[4]{'x'} = "K9";
$sixalpha[4]{"j"} = "89L";
$sixalpha[4]{'q'} = "8K9";
$sixalpha[4]{'z'} = "8KL";
$sixalpha[4]{'!'} = "K9L";
$sixalpha[4]{'?'} = "8K9L";

my $count = 0;
my $letterCount = 0;
my $fingerPairs = 0;
my $wordCount = 1 + $word =~ tr/ //;
my $strokeCount = 1;
while() {

    if(exists($letters[$letterCount+2]) && exists($sixalpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]$letters[$letterCount+2]"})) {
        # if a three-character combo exists in the lookup table for the current
        # slow, use the chord for that.
        print $sixalpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]$letters[$letterCount+2]"};
        $letterCount+=3;
        $fingerPairs++;

    }
    elsif(exists($letters[$letterCount+1]) && exists($sixalpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]"})) {
        # if a two-character combo exists in the lookup table for the current
        # slow, use the chord for that.
        print $sixalpha[$count]{"$letters[$letterCount]$letters[$letterCount+1]"};
        $letterCount+=2;
        $fingerPairs++;
    }
    elsif(exists($letters[$letterCount]) && exists($sixalpha[$count]{$letters[$letterCount]})) {
        # otherwise if the current symbol exists in the lookup table, use the
        # chord for that.
        print $sixalpha[$count]{$letters[$letterCount]};
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

