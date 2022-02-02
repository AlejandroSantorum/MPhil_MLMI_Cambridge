#!/usr/bin/env perl

# script provided by Lidia Mangu, IBM

$lgeid=$ARGV[0];
# language ID

$file=$ARGV[1];
#alignment.csv

$IV_file=$ARGV[2];
#term.map  file

$thresh=$ARGV[3];
#posterior threshold

$IV_OOV_TAG=$ARGV[4];
#"iv" if you score IV and "oov" if you score OOVs, "all" otherwise

$T_seconds=$ARGV[5];
# total duration of data set

$kk = "KW" . $lgeid . "-";

$beta=999.9;

open(fq,$IV_file)||die "I can't open $IV_file";
while(<fq>){
  @a=split(/\s+/);
  if ($IV_OOV_TAG eq "all"){
    $is_IV{$kk.$a[1]}=1;
  }
  elsif (/^$IV_OOV_TAG/){
    $is_IV{$kk.$a[1]}=1;
  }
}
close(fq);

$no_kwd=0;

open(f,$file) || die "I can't open $file";
while(<f>){
  chop;
  @a=split(/\,/);
  $kwd=$a[3];

  $t=$a[$#a-2];
  
  if ($t < $thresh){
    if ($a[$#a] eq "CORR"){
      $a[$#a] = "MISS";
    }
  }

  if (($t >=$thresh)|| ($a[$#a] eq "MISS")){
    $count{$kwd}{$a[$#a]}++;
    
    if ($is{$kwd} eq "" && $is_IV{$kwd}){
      $no_kwd++;
    }
    if ($is_IV{$kwd}){$is{$kwd}=1;};
  }
}
close(f);

while(($k,$v)=each %is){
   
  $count_kwd{$k}=$count{$k}{"MISS"}+$count{$k}{"CORR"};
  
  $total_Miss+=$count{$k}{"MISS"};
  $total_TP+=$count{$k}{"CORR"};
  
  if ($count{$k}{"MISS"} + $count{$k}{"CORR"} > 0){
    $total_FA+=$count{$k}{"FA"};
  }
  if ($count_kwd{$k} == 0){
    $no_kwd--;
  }
  else{
    $P_miss{$k}=$count{$k}{"MISS"}/$count_kwd{$k};
    $total_Pmiss+=$P_miss{$k};
    $P_FA{$k}=$count{$k}{"FA"}/($T_seconds - $count_kwd{$k});
    $total_PFA+=$P_FA{$k};    
    
    $value{$k}=1 - $P_miss{$k} - $beta*$P_FA{$k};
    $total+=$value{$k};
}
}

if ( $no_kwd == 0) {
    print "$IV_OOV_TAG TWV=N/A theshold=$thresh\n";
} else {
    print "$IV_OOV_TAG TWV=",$total/$no_kwd," theshold=$thresh number=$no_kwd\n";
}

  


  
  
