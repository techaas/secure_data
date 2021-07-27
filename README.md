# secure-data

共通鍵/公開鍵暗号でデータを安全に交換する実装のテストです.

詳しくは、[TECHaas - セキュアなデータ交換](http://localhost:1313/post/secure-communication/) をどうぞ

### 開発環境

コードは、MacOS 上の python 3.8.7 で動作テストしています. \
インストールされているパッケージは、こんな感じ.

```
$ pip list
Package      Version
------------ -------
pip          21.1.2
pycryptodome 3.10.1
setuptools   49.2.1
```

### openssl での鍵生成

実行前に `openssl` コマンドで鍵データを生成しておいてください。

```
openssl genrsa 2048 > private.pem
openssl rsa -pubout < private.pem > public.pem
```

