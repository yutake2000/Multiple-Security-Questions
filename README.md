# 使い方

## 暗号化

```
python3 encrypt.py input_file output_file
```

初めに質問を1行ずつ入力して、終わったら空行を入力してください。<br>
次にそれぞれの質問の解答を1行ずつ入力して、確認のためにもう一度それぞれの解答を入力してください。<br>
最後に、復号するのに必要な正解数を入力してください。<br>

## 復号

### 復号したファイルを保存する場合
```
python3 decrypt.py input_file -o output_file
```

### 復号したファイル(主にテキストファイル)を標準出力する場合
```
python3 decrypt.py input_file -o -
```

### 復号して元のファイルと同じになるか確かめる場合
```
python3 decrypt.py input_file -c src_file
```
src_file は暗号化する前のファイル<br>
暗号化した後、元のファイルを削除する前に復号ができるかどうか試すと良いでしょう。<br>

## 例

sample.msq は以下のコマンドを打つことで復号できます。<br>
秘密の質問は有名なクイズになっていて、必要正解数は2問です。<br>
```
python3 decrypt.py sample.msq sample.txt
```

次に自分の好きな秘密の質問を設定して暗号化してみましょう。
```
python3 encrypt.py sample.txt hoge.msq
```
