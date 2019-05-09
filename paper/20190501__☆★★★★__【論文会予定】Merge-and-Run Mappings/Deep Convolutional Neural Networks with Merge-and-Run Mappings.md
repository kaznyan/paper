# Deep Convolutional Neural Networks with Merge-and-Run Mappings



## 甲斐コメント

- 2回畳み込むより2つ並列して融通したほうが良いよっていうやつ
- 超簡単。
- 簡単な割に役立ちそうなので役立ちそう。



## Abstract

Residual 構造：Identity Mapping が Residual Branchをスキップ

- 情報の流れを改善するため、トレーニングが容易

提案手法：Deep Merge-and-Run

- Merge-and-Run ブロック ＆ Merge-and-Run マッピング

  - Residual Branchの入力を平均（Merge）
  - Residual Branchの出力に平均を追加し、次の入力とする（Run）

- 変換行列がべき乗

  →線形べき等関数

  →→情報の流れを改善し、学習を容易にする

- 他のネットワークと比較して

  - パスが短い
  - チャネル数が多い
  - 時間は変わらない

- 標準の認識タスクでパフォーマンスを評価

  →一貫した改善



## 1. Introduction

ResNetを発展させる手法：Deep Merge-and-Run

- Residual Branchをより効果的に組み立てる

  - Residual Branchの入力を平均し（Merge）、その平均を出力に追加
  - 追加したものを次のResidual Branchの入力とする（Run）
  - ネットワークの深さを直接減少させるため、トレーニングが容易です。

  ![キャプチャ](画像\キャプチャ.PNG)

- 線形べき等関数であり、順伝播も逆伝播も容易
- 幅が広いことで経験的にうまくいく
- CIFAR-10、CIFAR-100、SVHN、ImageNet上でResNetの性能を向上



## 2. Related Work

トレーニングを容易にするための重要な要素

- Identity MappingとBipass Path

標準：ResNet

- 比較的浅いネットワークの指数アンサンブルのように振る舞う
- 短いパスを導入することが勾配消失問題を回避する
- deeply-fused networks や FractalNetも同様の効果を含む

発展形：Decoupled Convolution, Inception, Xception, Inception-ResNet blocks, multi-residual networks, ResNeXt

- 各ブロックに複数のブランチを持つ
- 例えばResNeXtsはブランチを多くの小さなブランチに置き換える

提案手法：

- 深さを直接減らすために並列アセンブリを採用し、ブランチを変更しない

  →簡単に設計できて柔軟



## 3. Deep Merge-and-Run Neural Networks

###### Architecture

![キャプチャ4](画像\キャプチャ4.PNG)



###### 分析

- 定式化

![キャプチャ5](画像\キャプチャ5.PNG)

- 変形

![キャプチャ6](画像\キャプチャ6.PNG)

- 第二項の係数行列はべき等である（M^n = M）ため下記が成立

![キャプチャ7](画像\キャプチャ7.PNG)

- フォワードフロー中に入力と中間出力を後のブロックに直接送信するクイックパスがあることを示す

- 勾配逆伝搬についても同様

- その結果、前方と後方の両方の情報の流れを改善する

- 同じ層数で比較すると「長さ」は短くなるため、学習の難易度が改善する可能性がある

  ![キャプチャ8](画像\キャプチャ8.PNG)



## 4. Experiments

- 精度向上の効果あり（ResNet, Wide ResNet、Xception、ResNextで検証）

- SOTA（PyramidNet、IGC-L32M26など）と比較して同等程度

→パラメータ数のわりに効率の良い構造



## 5. Discussions

- ブランチの数は2が良い![キャプチャ2](画像\キャプチャ2.PNG)

- ブランチの相互作用が効果的であることを証明

  ![キャプチャ3](画像\キャプチャ3.PNG)



## 6. Conclusion

イントロと同じ