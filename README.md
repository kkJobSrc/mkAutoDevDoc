# Understand 

## getGlbVarInfo (関数)
Understand から取得した変更のマクロをマクロ名から検索し、該当するマクロの情報を返す関数。
検索は名前依存であるため、変更していないファイルのマクロも拾ってくる。
取得した情報は`change_macro_list.csv`に出力される。

| 0 | 1 | 2 | 3 | 4 | 5 | Note |
|---|---|---|---|---|---|------|
|Macro name| "def." or "use"| Ent.| File name| Row No.| Col No.| def=定義、use=参照、Ent.=understad内での参照形式|


# code differcne

# PRG-Relife

# gitApi
pythonから git コマンドを実行するためのモジュールで、各クラスから APIとして呼び出しやすさを考慮して設計している。  

## getAllChgLst (関数)
`git diff` により取得した Cpp、 Cの関数やメソッドと、マクロの変更点を抽出し、データテーブルとして返す。

| 0 | 1 | 2 | Note |
|---|---|---|------|
|File|Class|Method| C++|
|File|"func"|Func Name | C|
|File|"macro"|Macro name| Macro|

## allChgList (変数)
GitApi の関数 `srchUniDiff`で抽出した差分を全て記録している変数。
| 0 | 1 | 2 | Note |
|---|---|---|------|
|Row No. |Extractet content |Type| Typeは任意文字列|

## fixFileList (変数)
変更したファイルの一覧を保持している。ファイル名は`./FD/`よりも下のパスとなっている。
また重複に関しての処理をしていないため、同じパスが複数存在している。
| 0 | 1 | 2 | Note |
|---|---|---|------|
|Row No. |File path |Type| Type="file"|


# TODO
- ファイルを全部削除する問題の解決(作成する物のみ削除など)
- PRG-relef の結果を直接 Excelに移す
- 変更したファイルのマクロの内容も Markdown に挿入する
- 特定のコミット同士を比較できるようにする
