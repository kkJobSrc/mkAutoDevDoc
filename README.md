# Purpose
開発ドキュメントの自動生成をするスクリプト
* winmrg を利用したコード差分の生成
* 静的解析(PRG-Relife)の結果の抽出
* 影響解析ツール(understand)の自動操作

# How to Use
実行コマンドは以下の通りです。
```shell=
python main.py
```
1. GUIが起動
2. *条件の手動入力*か*設定ファイル利用可*を選択し[Next]
3. 解析条件の入力
    * ローカルリポジトリのパス
    * ブランチ名
    * ブランチ先頭からどれだけ遡るか(比較対象)
    * ドキュメントの出力先
    * 各解析の実行選択
4. [Excute]を押して実行

# Understand 

## getGlbVarInfo (関数)
Understand から取得した変更のマクロをマクロ名から検索し、該当するマクロの情報を返す関数。
検索は名前依存であるため、変更していないファイルのマクロも拾ってくる。
取得した情報は`change_macro_list.csv`に出力される。

| 0 | 1 | 2 | 3 | 4 | 5 | Note |
|---|---|---|---|---|---|------|
|Macro name| "def." or "use"| Ent.| File name| Row No.| Col No.| def=定義、use=参照、Ent.=understad内での参照形式|


# code differcne

# prg

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
変更したファイルの一覧を保持している。
また重複に関しての処理をしていないため、同じパスが複数存在している。
| 0 | 1 | 2 | Note |
|---|---|---|------|
|Row No. |File path |Type| Type="file"|
