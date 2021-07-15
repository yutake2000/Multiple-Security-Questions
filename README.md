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
python3 decrypt.py input_file output_file
```

### 復号したファイル(主にテキストファイル)を標準出力する場合
```
python3 decrypt.py input_file -
```

## 例

sample.msq が同梱されているので、以下のコマンドを打つことで復号できます。
秘密の質問は有名なクイズになっていて、ボーダーは2問です。
```
python3 decrypt.py sample.msq sample.txt
```

次に自分の好きな秘密の質問を設定して暗号化してみましょう。
```
python3 encrypt.py sample.txt hoge.msq
```
