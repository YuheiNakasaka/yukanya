# yukanya
Juice=Juiceのメンバーを判定する分類器

# Install
```
pip install -r requirements.txt
```

```
mkdir haarcascades && cp <haarcascadesのhaarcascade_frontalface_default.xmlのパス> ./haarcascades
```

# Step
## 1) 画像を取得

```
python scraping.py
```

## 2) 顔認識をして顔画像データを作成

```
python facecliping.py
```

## 3) 学習データを水増し
下記を生成する

- 通常画像/コントラストを上げた画像/コントラストを下げた画像/左右反転した画像の
  - 回転画像
  - ガウシアン
  - 閾値

```
python increase_data.py
```

## 4) 学習する

```
python train.py
```

## 5) 予測する

```
python predict.py <適当に拾ってきたメンバーの画像のパス>
```

# Tensorflow.jsで動かす
## 既存のモデルをweb用に変換する
[tfjs-converter](https://github.com/tensorflow/tfjs-converter)のREADMEに則ってインストールする

```
tensorflowjs_converter --input_format keras YukanyaModel_google_ameba.h5 ./
```