# Learning Spatio-Temporal Representation with Local and Global Diffusion



## 甲斐コメント





## Abstract

CNNのフィルタはローカルな操作であり広範囲の依存性を無視する

- ビデオは複雑な時間的変動を伴う情報集約型メディアであるため、この特性は良くない

提案手法：Local and Global Diffusion（LGD）

- ローカル表現とグローバル表現を並行して学習する新しいアーキテクチャで時空間表現学習を促進する
- LGDブロック：2表現の間の拡散をモデル化して相互作用させる
- kernelized classifier：ビデオ認識のために２つの側面からの表現を組み合わせる
- Kinetics-400およびKinetics-600ビデオ分類データセットで検証し高精度（ほぼSOTA）
- グローバルおよびローカル表現の両方の汎化を詳細に検証した



## 1. Introduction

ビデオコンテンツは大きなバリエーションと複雑さを持つため難しい

- 強力で一般的な時空間表現が欲しい

CNNを用いた手法の課題：

- 畳み込み演算が隣接画素の局所的な窓だけを処理すること

  →視野の全体像を十分にとらえることはできない

  →2つの離れたピクセル間の接続は、多数のローカル操作の後にのみ確立され、勾配消失しやすい

提案手法１：Local and Global Diffusion（LGD）

- 広範囲の依存関係を捉えた時空間表現を学習するための新しいアーキテクチャ
- 特徴マップは、局所的変動を表す Local Path と空間的位置における全体的外観を記述する Global Path に分けられる

提案手法２：kernelized classifier

- 両方の経路からの最終的表現をカーネルベース分類器によって結合

→いくつかのビデオ分類ベンチマークでSOTA



## 2. Related Work

とばした



## 3. Local and Global Diffusion

つぎここから





