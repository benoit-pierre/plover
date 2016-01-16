#!/usr/bin/perl -w

use strict;

my $word = shift;

# convert caps to use the 'caps' chord, including the doubled 'allcaps' variant
$word =~ s/([A-Z][A-Z]+)/||\L$1|/g;
$word =~ s/([A-Z])/|\L$1/g;

my @letters = split '', $word;

my @sixalpha = ();

# thumbs
$sixalpha[0]{'a'} = "B";
$sixalpha[0]{'b'} = "CVBN";
$sixalpha[0]{'c'} = "VB";
$sixalpha[0]{'d'} = "CM";
$sixalpha[0]{'e'} = "V";
$sixalpha[0]{'f'} = "CVB";
$sixalpha[0]{'g'} = "VNM";
$sixalpha[0]{'h'} = "VM";
$sixalpha[0]{'i'} = "M";
$sixalpha[0]{'j'} = "NM,";
$sixalpha[0]{'k'} = "XBN";
$sixalpha[0]{'l'} = "BM";
$sixalpha[0]{'m'} = "NM";
$sixalpha[0]{'n'} = "VN";
$sixalpha[0]{'o'} = "C";
$sixalpha[0]{'p'} = "BNM";
$sixalpha[0]{'q'} = "XNM";
$sixalpha[0]{'r'} = "CB";
$sixalpha[0]{'s'} = "CN";
$sixalpha[0]{'t'} = "N";
$sixalpha[0]{'u'} = "CV";
$sixalpha[0]{'v'} = "N,";
$sixalpha[0]{'w'} = "CBN";
$sixalpha[0]{'x'} = "XCV";
$sixalpha[0]{'y'} = "VBM";
$sixalpha[0]{'z'} = "CV,";
$sixalpha[0]{'an'} = "CVM";
$sixalpha[0]{'at'} = "X";
$sixalpha[0]{'en'} = ",";
$sixalpha[0]{'er'} = "CNM";
$sixalpha[0]{'he'} = "VBN";
$sixalpha[0]{'in'} = "CVN";
$sixalpha[0]{"nd"} = "XN";
$sixalpha[0]{'on'} = "CVNM";
$sixalpha[0]{'or'} = "XM";
$sixalpha[0]{'re'} = "VBNM";
$sixalpha[0]{'te'} = "C,";
$sixalpha[0]{'th'} = "BN";
$sixalpha[0]{'ti'} = "V,";
$sixalpha[0]{'-'} = "BN,";
$sixalpha[0]{'!'} = "XC";
$sixalpha[0]{'"'} = "XVB";
$sixalpha[0]{','} = "XB";
$sixalpha[0]{'.'} = "B,";
$sixalpha[0]{'?'} = "M,";
$sixalpha[0]{"'"} = "VB,";
$sixalpha[0]{'|'} = "XV"; # cap chord
$sixalpha[0]{' '} = "[ ]";

# thumbs with space preceding
$sixalpha[0]{' a'} = "[ ]B";
$sixalpha[0]{' b'} = "[ ]CVBN";
$sixalpha[0]{' c'} = "[ ]VB";
$sixalpha[0]{' d'} = "[ ]CM";
$sixalpha[0]{' e'} = "[ ]V";
$sixalpha[0]{' f'} = "[ ]CVB";
$sixalpha[0]{' g'} = "[ ]VNM";
$sixalpha[0]{' h'} = "[ ]VM";
$sixalpha[0]{' i'} = "[ ]M";
$sixalpha[0]{' j'} = "[ ]NM,";
$sixalpha[0]{' k'} = "[ ]XBN";
$sixalpha[0]{' l'} = "[ ]BM";
$sixalpha[0]{' m'} = "[ ]NM";
$sixalpha[0]{' n'} = "[ ]VN";
$sixalpha[0]{' o'} = "[ ]C";
$sixalpha[0]{' p'} = "[ ]BNM";
$sixalpha[0]{' q'} = "[ ]XNM";
$sixalpha[0]{' r'} = "[ ]CB";
$sixalpha[0]{' s'} = "[ ]CN";
$sixalpha[0]{' t'} = "[ ]N";
$sixalpha[0]{' u'} = "[ ]CV";
$sixalpha[0]{' v'} = "[ ]N,";
$sixalpha[0]{' w'} = "[ ]CBN";
$sixalpha[0]{' x'} = "[ ]XCV";
$sixalpha[0]{' y'} = "[ ]VBM";
$sixalpha[0]{' z'} = "[ ]CV,";
$sixalpha[0]{' an'} = "[ ]CVM";
$sixalpha[0]{' at'} = "[ ]X";
$sixalpha[0]{' en'} = "[ ],";
$sixalpha[0]{' er'} = "[ ]CNM";
$sixalpha[0]{' he'} = "[ ]VBN";
$sixalpha[0]{' in'} = "[ ]CVN";
$sixalpha[0]{" nd"} = "[ ]XN";
$sixalpha[0]{' on'} = "[ ]CVNM";
$sixalpha[0]{' or'} = "[ ]XM";
$sixalpha[0]{' re'} = "[ ]VBNM";
$sixalpha[0]{' te'} = "[ ]C,";
$sixalpha[0]{' th'} = "[ ]BN";
$sixalpha[0]{' ti'} = "[ ]V,";
$sixalpha[0]{' -'} = "[ ]BN,";
$sixalpha[0]{' !'} = "[ ]XC";
$sixalpha[0]{' "'} = "[ ]XVB";
$sixalpha[0]{' ,'} = "[ ]XB";
$sixalpha[0]{' .'} = "[ ]B,";
$sixalpha[0]{' ?'} = "[ ]M,";
$sixalpha[0]{" '"} = "[ ]VB,";
$sixalpha[0]{' |'} = "[ ]XV"; # space plus cap chord

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

# left ring and little fingers
$sixalpha[3]{' '} = "E";
$sixalpha[3]{'e'} = "W";
$sixalpha[3]{'t'} = "3";
$sixalpha[3]{'a'} = "D";
$sixalpha[3]{'o'} = "2";
$sixalpha[3]{'i'} = "S";
$sixalpha[3]{'n'} = "WE";
$sixalpha[3]{'s'} = "23";
$sixalpha[3]{'r'} = "SD";
$sixalpha[3]{'h'} = "SE";
$sixalpha[3]{'l'} = "2E";
$sixalpha[3]{'d'} = "W3";
$sixalpha[3]{'c'} = "WD";
$sixalpha[3]{'th'} = "3E";
$sixalpha[3]{'u'} = "ED";
$sixalpha[3]{'m'} = "2W";
$sixalpha[3]{'he'} = "WS";
$sixalpha[3]{'f'} = "2W3E";
$sixalpha[3]{'p'} = "WSED";
$sixalpha[3]{'in'} = "W3E";
$sixalpha[3]{'g'} = "23E";
$sixalpha[3]{'w'} = "SED";
$sixalpha[3]{'y'} = "WED";
$sixalpha[3]{'er'} = "2W3";
$sixalpha[3]{'an'} = "2WE";
$sixalpha[3]{'b'} = "WSE";
$sixalpha[3]{'re'} = "WSD";
$sixalpha[3]{'on'} = "WS3E";
$sixalpha[3]{'at'} = "2WED";
$sixalpha[3]{'en'} = "2WS";
$sixalpha[3]{'nd'} = "3ED";
$sixalpha[3]{'ti'} = "WS3";
$sixalpha[3]{','} = "2ED";
$sixalpha[3]{'.'} = "S3E";
$sixalpha[3]{'|'} = "2WD";
$sixalpha[3]{'v'} = "2WS3";
$sixalpha[3]{'or'} = "23ED";
$sixalpha[3]{'te'} = "S3ED";
$sixalpha[3]{'k'} = "2WSD";
$sixalpha[3]{"'"} = "2S";
$sixalpha[3]{'"'} = "3D";
$sixalpha[3]{'-'} = "S3";
$sixalpha[3]{'x'} = "2D";
$sixalpha[3]{'j'} = "2S3";
$sixalpha[3]{'q'} = "23D";
$sixalpha[3]{'z'} = "S3D";
$sixalpha[3]{'!'} = "2SD";
$sixalpha[3]{'?'} = "2S3D";

# right fore and middle fingers
$sixalpha[2]{' '} = "Y";
$sixalpha[2]{'e'} = "U";
$sixalpha[2]{'t'} = "6";
$sixalpha[2]{'a'} = "H";
$sixalpha[2]{'o'} = "7";
$sixalpha[2]{'i'} = "J";
$sixalpha[2]{'n'} = "YU";
$sixalpha[2]{'s'} = "67";
$sixalpha[2]{'r'} = "HJ";
$sixalpha[2]{'h'} = "YJ";
$sixalpha[2]{'l'} = "Y7";
$sixalpha[2]{'d'} = "6U";
$sixalpha[2]{'c'} = "HU";
$sixalpha[2]{'th'} = "6Y";
$sixalpha[2]{'u'} = "YH";
$sixalpha[2]{'m'} = "7U";
$sixalpha[2]{'he'} = "UJ";
$sixalpha[2]{'f'} = "6Y7U";
$sixalpha[2]{'p'} = "YHUJ";
$sixalpha[2]{'in'} = "6YU";
$sixalpha[2]{'g'} = "6Y7";
$sixalpha[2]{'w'} = "YHJ";
$sixalpha[2]{'y'} = "YHU";
$sixalpha[2]{'er'} = "67U";
$sixalpha[2]{'an'} = "Y7U";
$sixalpha[2]{'b'} = "YUJ";
$sixalpha[2]{'re'} = "HUJ";
$sixalpha[2]{'on'} = "6YUJ";
$sixalpha[2]{'at'} = "YH7U";
$sixalpha[2]{'en'} = "7UJ";
$sixalpha[2]{'nd'} = "6YH";
$sixalpha[2]{'ti'} = "6UJ";
$sixalpha[2]{','} = "YH7";
$sixalpha[2]{'.'} = "6YJ";
$sixalpha[2]{'|'} = "H7U";
$sixalpha[2]{'v'} = "67UJ";
$sixalpha[2]{'or'} = "6YH7";
$sixalpha[2]{'te'} = "6YHJ";
$sixalpha[2]{'k'} = "H7UJ";
$sixalpha[2]{"'"} = "7J";
$sixalpha[2]{'"'} = "6H";
$sixalpha[2]{'-'} = "6J";
$sixalpha[2]{'x'} = "H7";
$sixalpha[2]{"j"} = "67J";
$sixalpha[2]{'q'} = "6H7";
$sixalpha[2]{'z'} = "6HJ";
$sixalpha[2]{'!'} = "H7J";
$sixalpha[2]{'?'} = "6H7J";

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

