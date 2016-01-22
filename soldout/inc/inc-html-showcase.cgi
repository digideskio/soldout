# $Id: inc-html-showcase.cgi 96 2004-03-12 12:25:28Z mu $

my $showcasecount=$DT->{showcasecount};

$disp.="●陳列棚：現在$showcasecount個：維持費 \\$SHOWCASE_COST[$showcasecount-1]<HR>";

my $usertaxrate=GetUserTaxRate($DT);

$disp.=$TB;
$disp.=$TR;
$disp.=$TD."棚No";
$disp.=$TD."商品名";
$disp.=$TD."売値";
$disp.=$TD."標準価格";
$disp.=$TD."売却税";
$disp.=$TD."在庫数";
$disp.=$TD."今期売上数";
$disp.=$TD."前期売上数";
$disp.=$TD;
$disp.=$TRE;

for(my $cnt=0; $cnt<$DT->{showcasecount}; $cnt++)
{
	my $itemno=$DT->{showcase}[$cnt];
	my $ITEM=$ITEM[$itemno];
	my $scale=$ITEM->{scale};
	my $stock=$itemno ? $DT->{item}[$itemno-1]:0;

	$disp.=$TR.$TD."棚".($cnt+1);
	$disp.=$TD;
	$disp.="<A HREF='item.cgi?$USERPASSURL&no=$itemno&sc=".($cnt+1)."&pr=".$DT->{price}[$cnt]."&bk=$MYNAME'>" if $stock;
	$disp.=GetTagImgItemType($itemno).$ITEM->{name};
	$disp.="</A>" if $stock;
	
	if($itemno)
	{
		my($taxrate,$tax)=GetSaleTax($itemno,1,$DT->{price}[$cnt],$usertaxrate);
		$disp.=$TD."\\".$DT->{price}[$cnt];
		$disp.=$TD."\\".$ITEM->{price};
		$disp.=$TD."\\".$tax." (税率".$taxrate."%)";
		$disp.=$TD.$stock.$scale;
		$disp.=$TD.($DT->{itemtoday}{$itemno}+0).$scale;
		$disp.=$TD.($DT->{itemyesterday}{$itemno}+0).$scale;
		$disp.=$TD."<A HREF='showcase-edit.cgi?yen=1&$USERPASSURL&item=0&no=$cnt&bk=sc'>陳列中止</A>";
	}
	else
	{
		$disp.=$TD.$TD.$TD.$TD.$TD.$TD;
	}
	$disp.=$TRE;
}

$disp.=$TBE;

1;
