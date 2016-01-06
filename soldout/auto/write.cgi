# $Id: write.cgi 96 2004-03-12 12:25:28Z mu $

sub DataCommitOrAbort
{
	my($abort)=@_;
	
	opendir(DIR,$TEMP_DIR);
	my @tempfile=grep(/.$FILE_EXT$/,readdir(DIR));
	closedir(DIR);
	
	my $markfile=GetPath($COMMIT_FILE);
	
	if(scalar(@tempfile))
	{
		OpenAndCheck($markfile),close(OUT) if !$abort;
		if(!$abort || -e $markfile)
		{
			# commit
			foreach(@tempfile)
			{
				RenameAndCheck($TEMP_DIR."/".$_,$DATA_DIR."/".$_);
			}
		}
		else
		{
			# abort
			foreach(@tempfile)
			{
				unlink($TEMP_DIR."/".$_);
			}
		}
	}
	unlink($markfile) if -e $markfile;
}

sub CheckLockStatus
{
	return if $LOCKED eq '' || -e $LOCKED;
	
	WriteErrorLog("write lock check error ",$LOG_ERROR_FILE);
	OutError("異常処理です。最初からやり直してみてください。");
}

sub DataWrite
{
	my($cnt,$DT);
	
	CheckLockStatus();
	
	DataFilesBackup() if (stat(GetPath($BACKUP_DIR,$DATA_FILE)))[9]<$NOW_TIME-$BACKUP_TIME; #$BACKUP_TIME秒経ったらバックアップ
	
	utime($DTlasttime,$DTlasttime,GetPath($LASTTIME_FILE));
	
	OpenAndCheck(GetPath($TEMP_DIR,$DATA_FILE));
	
	print OUT "$DTlasttime\n$DTpeople,$DTnextid,$DTblockip,$DTTradeIn,$DTTradeOut\n";
	print OUT join(",",@DTwholestore)."\n";
	print OUT join(",",%DTevent)."\n";
	print OUT AutoVar::Get(\$DTtown)."\n";

	print OUT "//\n";
	
	SortDT();

	for($cnt=0; $cnt<=$#DT; $cnt++)
	{
		$DT=$DT[$cnt];
		next if !$DT->{status};
		
		$DT->{money}=$MAX_MONEY if $DT->{money}>$MAX_MONEY;
		$DT->{foundation}=$NOW_TIME if !$DT->{foundation};
		
		print OUT join(",",map{$DT->{$_}}@DTindexnamelist),"\n";
		
		#SetUserData($DT) if ref($DT->{user}) eq "HASH";
		
		print OUT join(",",@{$DT->{showcase}}).":";
		print OUT join(",",@{$DT->{price}}).":";
		print OUT AutoVar::Get(\$DT->{item}).":";          #join(",",@{$DT->{item}}).":"
		print OUT AutoVar::Get(\$DT->{itemyesterday}).":"; #join(",",%{$DT->{itemyesterday}}).":";
		print OUT AutoVar::Get(\$DT->{itemtoday}).":";     #join(",",%{$DT->{itemtoday}}).":";
		print OUT AutoVar::Get(\$DT->{exp}).":";           #join(",",%{$DT->{exp}}).":";
		print OUT AutoVar::Get(\$DT->{user});
		print OUT "\n";
	}
	close(OUT);
}

sub DataFilesBackup
{
	foreach my $filetype (@BACKUP_FILES)
	{
		open(IN, GetPath($filetype));
		open(OUT,">".GetPath($BACKUP_DIR,$filetype));
		while(<IN>){print OUT $_;}
		close(OUT);
		close(IN);
	}
}

sub CloseShop
{
	my($id,$mode)=@_;
	
	return if !defined($id2idx{$id});
	
	my $idx=$id2idx{$id};
	my $DT=$DT[$idx];
	
	ReadBox(GetBoxFile('get_temp'));
	@NEWBOX=();
	foreach my $idx (0..$#BOX)
	{
		$_=$BOX[$idx];
		if(/^\d+,$id,(\d+),(\d+),/)
		{
			if(!($2&$FLAG_TO_READ) && defined($id2idx{$1}))
			{
				$DT[$id2idx{$1}]->{boxcount}--;
			}
		}
		elsif(/^\d+,(\d+),$id,(\d+),/)
		{
			if($2&$FLAG_TO_READ && defined($id2idx{$1}))
			{
				$DT[$id2idx{$1}]->{boxcount}--;
			}
		}
		else
		{
			push(@NEWBOX,$BOX[$idx]);
		}
	}
	@BOX=@NEWBOX;
	WriteBox();
	
	SetUserData($DT);
	my $dtdata="";
	$dtdata.=join("\n",
		$mode,
		join(",",map{$DT->{$_}}@DTindexnamelist),
		join(":",
			join(",",@{$DT->{showcase}}),
			join(",",@{$DT->{price}}),
			join(",",@{$DT->{item}}),
			join(",",%{$DT->{itemyesterday}}),
			join(",",%{$DT->{itemtoday}}),
			join(",",%{$DT->{exp}}),
			join(",",%{$DT->{user}}),
		),
	);
	WriteErrorLog($dtdata,$LOG_DELETESHOP_FILE);
	$DT->{status}=0;
	$DT->{money}=0;
	$DT->{rank}=0;
	unlink(GetPath($SUBDATA_DIR,$DT->{name}."-s"));
}

1;
