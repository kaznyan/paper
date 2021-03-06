# ThumbNet: One Thumbnail Image Contains All You Need for Recognition



## 甲斐コメント

- 構造は面白い
- NWの中で「ここはこうなっているべき」と思う箇所があるなら積極的にLossを設定して理想通りに仕向けるべきだということ、およびその発想とバリエーションも学べる
- まあ情報量減らす都合上、精度は……。でも普通に圧縮するよりは全然良いらしいよ



## Abstract

ThumbNet

- CNNモデルを1つのサムネイル画像で推論できるようにして高速化・圧縮
- ThumbNetをトレーニングするための3つの効果的な戦略
- 入力画像が16倍に縮小された場合でも、元の入力ネットワークの精度



## 1. Introduction

CNNを高速化・圧縮

- pruning
- 低ランク分解によってフィルタの数を減らす
- 知識蒸留
- 高速畳み込み技法（FFT、Winogradアルゴリズム）、量子化および２値化

提案手法：

- 任意のアーキテクチャ、深さ、幅のCNNを高速化および圧縮するためのテスト時ネットワーク入力としてサムネイル画像を使用する

  ![キャプチャ](画像\キャプチャ.PNG)

貢献：

- ThumbNet
  - オリジナル入力ネットワークの精度を維持しながら、計算量とメモリ消費量を大幅に削減できるようなサムネイル入力ネットワークをトレーニングするフレームワーク
- 優れた識別特性と自然な有彩色の外観を持つサムネイル画像を生成する教師付き画像ダウンスケーラ



## 2. Related Work

- 蒸留
- AE
- Small Input Network



## 3. ThumbNet Model and Learning

#### 3.1 Architecture

![キャプチャ2](画像\キャプチャ2.PNG)

- よく訓練されたネットワークＴを用意
  - 大きなサイズ（224 x 224など）の入力画像→Conv→FC→K個のロジットを生成
  - 参照として利用し、ThumbsNetのトレーニング時は変更されない

- サムネイル画像用のネットワークSを学習
  - より小さいサイズ（112 x 112など）
  - Tの対応するレイヤとまったく同じ形状とサイズだが空間サイズはより小さい
  - ThumbNetの主な学習目的
- ダウンスケーラE
  - 元の入力画像からサムネイル画像を生成

#### 3.2 詳細

###### ダウンスケーラー

- 伝統的な画像縮小方法では縮小された画像の識別能力を考慮していない

  →分類目標に合わせて元の画像から識別情報を適応的に抽出することが必要

- 5×5の畳み込み演算とそれに続くバッチ正規化およびReLUを持つ2つの畳み込み層を含むだけ

  - 第1層：入力チャンネルよりも多くの出力チャンネルがある
  - 第2層：画像を復元するためにちょうど３つの出力チャンネルがある
  - 各層の歩幅サイズは要求される縮小率に依存

- モーメントマッチング損失 LMM

  - 生成された小さい画像が視覚的に快適で認識可能であることを元画像との比較で保証
  - ThumbNetのアーキテクチャ全体に組み込まれ、他の損失と一緒にトレーニング

  →Eは教師付き画像ダウンスケーラである

###### Distillation-Boosted Supervision

- 分類損失 LCL：クロスエントロピー

  - 予測ラベルとグランドトゥルースラベルを一致させる

  - モデルTの情報をモデルSにうまく移行することが望ましい

    →別の損失を定義する

- 知識蒸留損失 LKD：2モデルの softened probabilities 間でのクロスエントロピー

  - この仕組みを distillation-boosted supervision と呼ぶ

###### Feature-Mapping Regularization

- 特徴マッピング損失 LFM：Sの特徴マップがTの特徴マップに良好にDecodeできるか

  ![キャプチャ3](画像\キャプチャ3.PNG)

  - AEのように平均二乗誤差をとる
  - Deconvはストライド2、レイヤ数は縮小率によって決まる



## 4. Experiment

- ThumbNetを介してトレーニングされたネットワークSのパフォーマンス

- 学習したダウンスケーラが他の分類関連のタスクにも一般的に適用できることを検証する



## 5. Conclusion

認識の正確さを犠牲にすることなくリソース消費を劇的に減らす推論ネットワークを学ぶ

副産物として教師付きダウンスケーラを使用

トレーニングに使用した以外のデータセットやネットワークアーキテクチャに一般化できる







