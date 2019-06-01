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
