# Shake-Shake regularization

## 甲斐コメント

過学習防止シリーズ。

マルチブランチNWの各ブランチを無相関化する。

理論としては面白いが、ネットワークの形を変えてまで実装するかというと微妙？



## Abstruct

目的：過学習の防止

アイデア：マルチブランチNWで、並列ブランチの標準的な総和を確率的アフィン結合に置き換える

結果：3分岐残差NWに適用し、CIFAR-10およびCIFAR-100のSOTA

https://github.com/xgastaldi/shake-shake



## 1. Introduction

Deep残差ネットの精度改善

- 深さ、幅、濃度





Deep残差ネットの汎化性能改善

- Weight Decay、Early Stopping
- Dropout
- 確率的勾配降下（SGD）


- Batch Normalization
  - Ioffe＆Szegedy（2015）
  - Zagoruyko＆Komodakis（2016）
  - Huang et al.（2016b）


- マルチブランチNWのいくつかの情報経路をランダムにdropして学習
  - Huang et al.（2016b）
  - Larsson et al.（2016）





提案手法：

並列ブランチの標準的な総和を確率的アフィンの組み合わせで置き換えることによってマルチブランチネットワークの汎化能力を改善



#### 1.1 モチベーション

データ拡張技術を内部表現に適用することができるのでは？

→2つのテンソルを確率的に「ブレンド」する実現してみた

　→勾配にノイズを加える手法の拡張



#### 1.2 ResNet（3ブランチ）での解説 

![キャプチャ4](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ4.PNG)



従来手法：足す

![キャプチャ2](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ2.PNG)



提案手法：寄与をランダムにして足す

![キャプチャ3](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ3.PNG)



#### 1.3 学習手順

- 各順方向パスの前に、すべてのスケーリング係数が新しい乱数で上書きされる
- 各逆方向パスの前に、再びすべてのスケーリング係数が新しい乱数で上書きされる
- これにより、トレーニング中に順方向フローと逆方向フローが確率的に混在

![キャプチャ5](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ5.PNG)



## 2. CIFAR-10における実験

- コード：

​	https://github.com/xgastaldi/shake-shake

- 結果：

![キャプチャ6](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ6.PNG)

​		Even：スケーリング係数 = 0.5

​		Shake：スケーリング係数 = ランダム

​		Keep：Backwardでスケーリング係数をリセットしない

​		Image：ミニバッチ内の各画像に対し異なるスケーリング係数

​		Batch：ミニバッチ内の各画像に対し同一のスケーリング係数

- 考察：
  - Shake-EvenまたはShake-Shakeにより高精度を実現
  - フィルタ枚数を増やすとShake-Shakeが最も良い
  - Imageレベルで係数を適用する方が良い



## 3. Residual Branch間の相関

正則化（Shake-Shake Regularizationのこと）によって2つのResidual Branch間の相関が増減するか実験した

1. 画像を順方向に計算し、2つのBranchの出力を記録する
2. Flatにする
3. 2ベクトル間の共分散、各ベクトルの分散を計算する
4. 相関係数を計算する



結果：

- 2つのBranch間で、出力テンソルの相関は正則化によって減少する

  →2つのブランチが何か別のことを学ぶように強制される

  ![キャプチャ7](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ7.PNG)

- 同じ層のBranch間では、他の層のBranch間より相関が大きい

  →「整列」を強制する（甲斐注：どういうメリットであるかは不明）



## 4. 正則化の強さ

残差ブロックi内の画像jに対し、

- 順方向パス中に使用される係数：αij
- 逆方向パス中に使用される係数：βij

![キャプチャ8](C:\Users\d184813\Desktop\論文\おわ\20190402__Shake-Shake regularization\画像とか\キャプチャ8.PNG)



→往路で小さな重みを受けたブランチに復路で大きな重みを与えた場合に正則化が強くなる

　（学習しづらくなるが過学習もしづらくなる？）



## 5. NW条件を変えての検討

- Skip connectionがないNWでもShake-Shakeが有効であることがある
- 畳み込みを1回しか持たないパスではShake-Shakeが有効でない
- Batch Nornalizationを無くすと収束しづらくなるが使用は可能