# パーティクルフィルタを用いた物体追跡
パーティクルフィルタを使ってノイズの乗った入力データから，物体を追跡するプログラム．

## 実行方法
### 物体追跡プログラム
```
$ python src/object_tracking.py
```
出力は[result/result_10000.gif](./result/result_10000.gif)

### 入力データの視覚化をするプログラム
```
$ python src/data_visualize.py
```
出力は[result/data.gif](result/data.gif)

## 出力
出力のGIFは[result](./result)に保存される．  
- [パーティクル数1000の結果](./result/result_1000.gif)
- [パーティクル数10000の結果](./result/result_10000.gif)
- [パーティクル数100000の結果](./result/result_100000.gif)
- [入力データのGIF](result/data.gif)

出力例
![パーティクル数100000の結果](https://github.com/yotaroy/particle_filter/tree/master/result/result_100000.gif, "出力例")

## 入力データ
入力データは[DataForPF/txt](./DataForPF/txt)にあるテキストデータ400個．データ1つは30*40のバイナリーで，1が物体を表すが，ノイズによって0,1が反転している．ノイズの乗り方は時間変化する．また，時々データのほとんどが1になる．  
これを視覚化したものが[result/data.gif](result/data.gif)．
