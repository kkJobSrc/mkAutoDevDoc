
# エラー発生したら (when occurer error): 
# >> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# >> misc/scoop.ps1

##################################################
# install Scoop
##################################################
try {
  # Scoopのインストール確認
  get-command scoop -ErrorAction Stop
} 
catch [Exception] {
  # Scoopのインストール
  Set-ExecutionPolicy RemoteSigned -scope CurrentUser
  Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
  scoop alias add up "scoop update; scoop update *" "Update all apps."
}

# install basic module
scoop install aria2
#scoop install git # 既存の環境のgitと共存することになるので不要
scoop install sudo

# add bucket
scoop bucket add extras

# Scoopのインストールディレクトリの取得
$SCOOP_ROOT = if ($env:SCOOP) {$env:SCOOP} else {"$home\scoop"}

scoop install winmerge # winmerge
