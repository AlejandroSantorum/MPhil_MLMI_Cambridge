#### File: IndusCorporaDefs.pl
#### Desc: This file defines the preferred scoring regime for a system 
####
#### History:
#### V1 20130305 - Initial version
#### V2 20130327 - Added 107
#### V3 20130402 - Added EvalPart1 for 101, 104, 105, and 106
####             - Added the set definititons
####             - Added Version ID
#### V4 20130424 - Added evalpart1 as a data set for 107
#### V5 20130429 - Added the character case conversion for Vietnamese STT scoring
#### V6 20130828 - Added 102 and 103 data
#### V7 20131106 - Added 206 data
#### V8 20131126 - Added 201 data
#### V9 20131216 - Modified the Babel corpora names to 'IARPA-babel'.  Added the code to linke babel??? db names to IARPA-babel??? names so that both work.
#### V10 20131219 - Added 203 data
#### V11 20140402 - Added 204 data
#### V12 20141016 - Added 205, 207, 301, 302, 303, and 304 data
#### V13 20140417 - Corrected the EvalPart1 subset for the Op2 dev languages
#### V14 20140424 - Added 202

$indusCorporaDefs = {
    version => "IndusCorporaDefs V14 20150424",       
    versionID => 14,       
    sets => {
	"Full" => { 
	    Desc => "Full Submission",
	    ECF => "$db/${lcorpus}_${lpart}.scoring.ecf.xml", 
	    KWS => {
	      BaDev => [      "\\.alignment.csv", "\\.log", "\\.sh", "\\.sum.*", "\\.bsum.*", "\\.dets/.*srl.gz", "\\.dets/.*.png"],
	      BaEval=> [                          "\\.log", "\\.sh", "\\.sum.*",                                  "\\.dets/.*.png"],
	    }
	},
	"DevSubset" => { 
	    Desc => "Dev Subset", 
	    ECF => "$db/${lcorpus}_${lpart}.scoring.dev.ecf.xml",
	    KWS => {
	      BaDev => [      "\\.alignment.csv", "\\.log", "\\.sh", "\\.sum.*", "\\.bsum.*", "\\.dets/.*srl.gz", "\\.dets/.*.png"],
	      BaEval=> [                          "\\.log", "\\.sh", "\\.sum.*", "\\.bsum.*",                     "\\.dets/.*.png"],
	    },
	},
	"DevProgSubset" => { 
	    Desc => "Dev-Progress Subset", 
	    ECF => "$db/${lcorpus}_${lpart}.scoring.dev-progress.ecf.xml",
	    KWS => {
	      BaDev => [ ],
	      BaEval=> [                          "\\.log", "\\.sh",                                              "\\.dets/.*.png"],
	    },
	},
	"EvalPart1" => { 
	    Desc => "Eval Subset Part1",
	    ECF => "$db/${lcorpus}_${lpart}.scoring.cond-evalpart.value-evalpart1.files.ecf.xml",
	    KWS => {
	      BaDev => [      "\\.alignment.csv", "\\.log", "\\.sh", "\\.sum.*", "\\.bsum.*", "\\.dets/.*srl.gz", "\\.dets/.*.png"],
	      BaEval=> [                          "\\.log", "\\.sh", "\\.sum.*",                                  "\\.dets/.*.png"],
	    }
	},
    },

    languages => {     
        ### Cantonese
        "IARPA-babel101" =>  { "Set" => "Full|DevSubset|DevProgSubset|EvalPart1",
                         "TokTimes" => "MITLLFA[23]", 
                         "TokSeg" => "SplitCharText", 
                         "KWSProtocol" => "Occur", 
                         "STTOptions" => { encoding => "-e utf-8" } },

        ### Assamese
        "IARPA-babel102" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur", 
                         "STTOptions" => { encoding => "-e utf-8" } },

        ### Bengali
        "IARPA-babel103" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur", 
                         "STTOptions" => { encoding => "-e utf-8" } },

        ### Pashto
        "IARPA-babel104" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur", 
                         "STTOptions" => { encoding => "-e utf-8" }  } ,
        ### Turkish
        "IARPA-babel105" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_turkish" }  } ,
        ### Tagalog
        "IARPA-babel106" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" }  } ,
        ###Vietnamese
        "IARPA-babel107" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_vietnamese" } } ,
        ### HatianCreole
        "IARPA-babel201" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### Swahili
        "IARPA-babel202" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### Lao
        "IARPA-babel203" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### tamil
        "IARPA-babel204" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### kurmanji
        "IARPA-babel205" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_kurmanji" } } ,
        ### Zulu
        "IARPA-babel206" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### tokpisin
        "IARPA-babel207" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### cebuano
        "IARPA-babel301" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_cebuano" } } ,
        ### kazakh
        "IARPA-babel302" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_kazakh" } } ,
        ### telugu
        "IARPA-babel303" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" } } ,
        ### lithuanian
        "IARPA-babel304" =>  { "Set" => "Full|EvalPart1",
                         "TokTimes" => "MITLLFA3", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8 babel_lithuanian" } } ,
        ### English
        "babel001" =>  { "Set" => "Full",
                         "TokTimes" => "STD06FA", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { }  } ,
        ### Arabic
        "babel002" =>  { "Set" => "Full",
                         "TokTimes" => "STD06FA", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e utf-8" }  } ,
        ### Mandarin
        "babel003" =>  { "Set" => "Full",
                         "TokTimes" => "STD06FA", 
                         "TokSeg" => "AppenWordSeg", 
                         "KWSProtocol" => "Occur" , 
                         "STTOptions" => { encoding => "-e GB" } } 
        
        }
     };

### Copy languages with name change
foreach my $lang(keys %{ $indusCorporaDefs->{"languages"} }){
    next if ($lang !~ /^IARPA-(babel10[1234567]|babel20[16])/);
    $indusCorporaDefs->{"languages"}{$1} = $indusCorporaDefs->{"languages"}{$lang};
}

#use Data::Dumper;  print Dumper($indusCorporaDefs);

1;
