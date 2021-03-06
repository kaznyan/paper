﻿# REGULARIZING NEURAL NETWORKS BY PENALIZING CONFIDENT OUTPUT DISTRIBUTIONS

## 甲斐コメント

ラベル平滑化したり自信度ペナルティを与えるだけで過学習を防止できるよ、という論文。

結局はデータの空間に縛られたり上下や中央にシフトしたりするだけなんだよなあという感想。

ただし自信度ペナルティの実装は簡単なので知っておくとよい感じかな




## Abstruct

低エントロピー出力にペナルティを科すことが教師あり学習における強力な正則化子として作用することを示す。

さらに、

- エントロピーを用いたペナルティから、KL発散を用いたラベルスムージングに展開する。
- ラベル平滑化と信頼ペナルティの両方が、最先端のモデルを改善することを明らかにする。
- これらの正則化器の広い適用可能性を示唆する。



## 1. Introduction

過学習防止のアルゴリズムは隠れた活性化またはニューラルネットワークの重みに作用する。

- Early Stopping
- L1 / L2正則化
- Dropout
- バッチ正規化

→出力分布の正則化するはほとんど検討されていない



出力分布に関する考察

- 正しくないクラスラベルに割り当てられた確率もネットワークの知識の一部である
- その重要性は他の重みに依存せず自然スケールを有するべき



結論：ラベルスムージングと信頼ペナルティの両方が最先端のモデルを改善することを示す



## 2. 関連研究

エントロピーを低くしすぎないようにする研究

- 強化学習で使用（Williams＆Peng, 1991）

  →ポリシーの早期収束が妨げられ、パフォーマンスが向上（Mnih et al., 2016）

- 最大尤度と強化学習目的を結びつける（Norouzi et al., 2016）

- 音声認識モデルの訓練にも応用（Luo et al., 2016）



教師ありNNではラベル平滑化が研究される

- NWが各トレーニング例に完全な確率を割り当てないようにして過学習を減らす
- 単にラベルノイズを追加することもNNの正則化に効果的（Xie et al., 2016）
- 教師モデルを使用してラベルを平滑化（Hinton et al., 2015）
- モデル自身の分布を使用してラベルを平滑化（Reed et al., 2014）
- Virtual adversarial training（Miyato et al., 2015）も有力



## 3. 出力の正規化

####　3.1 自信度ペナルティ

自信度ペナルティ：1つのクラスにすべての確率を設定にしないよう正則化項を追加

![キャプチャ](画像とか\キャプチャ.PNG)

訓練の後半にのみ過学習を防ぎたい

- 自信度ペナルティをアニーリング
  - ？？？
- エントロピーが閾値を下回ったときのみペナルティ
  - 信頼損失にヒンジ損失を追加することで可能
  - 追加ハイパーパラメータを導入するが、収束は速くなる
  - 閾値を置かなくても同等のパフォーマンスを発揮できることが分かったので焦点を当てない



#### 3.2 ラベル平滑化

ラベル分布が一様である場合、ラベルの平滑化は一様分布Uとネットワークの予測分布pの間のKLダイバージェンスを負の対数尤度に追加することと同じ。
![キャプチャ2](画像とか\キャプチャ2.PNG)



## 4. 実験

#### 4.1 画像分類

![キャプチャ3](画像とか\キャプチャ3.PNG)



- 極端な予測を避けて汎化性能を獲得
- 精度はわずかに向上する程度



#### その他タスク 

- 機械翻訳や言語モデリングでも使用可能
- わずかに精度向上
- Dropoutと相性が悪い場合がある