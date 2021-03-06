# Bayesian Generative Active Deep Learning



## 甲斐コメント

- 「良い情報をもたらすサンプル」をラベルなしデータから選び出す能動学習をさらに発展。

  そういうサンプルを生成することができるようになった

- ちょっと詳細はまたほしくなったらでいいやって感じだった



## Abstract

トレーニングとラベリングのために膨大な量の計算と人的資源を必要とする

小さなラベル付きトレーニングセットを必要とする効果的なトレーニング方法の設計は、リソースのより効果的な使用を可能にする重要な研究

この問題に対処するために設計された現在のアプローチ：

- 能動学習
  - オラクルによってラベル付けされるラベル付けされていないトレーニングサンプルの「最も有益な」サブセットの選択に依存している
  - 少量の有益なサンプルしか選択できない
- Augmentation
  - 新しいトレーニングポイントを人工的に生成する
  - 有益でないサンプルも生成するので計算資源を浪費する

提案手法：

- 能動学習とデータ増大を組み合わせたベイズ生成型能動深層学習アプローチ
- 効率的な訓練
- MNIST、CIFAR- {10、100}、SVHNで能動学習やDataAugmentationと比較



## 1. Introduction

データ足りない問題への対策：Active Learning（プールベース）

- 小さいラベル付きデータセットと大きいラベルなしデータセットの使用

  - ラベルなしセットから小さいサブセットを取り出す（サブセットがどれほど有益かを評価する取得関数を使用して自動的に選択）
  - 選択されたサブセットにオラクル（人間の注釈者）がラベル付け
  - サブセットをラベル付きデータセットに統合
  - 再学習

  →得られるデータのサイズが小さいのが難点

- Augmentation

  →新しいサンプルの生成がトレーニングプロセスにとってどれほど有益であるかを考慮しない

  →→生成されたサンプルの大部分はトレーニングプロセスにとって重要ではない



提案手法：ベイズ生成型アクティブディープラーニング手法

- トレーニングプロセスに有益なサンプルを生成する
  - Bayesian active learning by disagreement (BALD)
  - サンプルをオラクルによってラベル付け
  - VAE - ACGANによって処理
  - 追加 & 再学習
- GANと比較した利点
  - 単純な情報の喪失よりも効果的と言われている「取得関数」を使用できる
  - 生成モデルと分類モデルを一緒に訓練する
- 生成された人工サンプルの有益性を検証
  - ラベルなしのトレーニングセットから選択したアクティブ学習サンプルとの比較
  - できたモデルの精度を見て検証



## 2. Related work

###### Bayesian Active Learning

- （プールベースの）アクティブラーニングフレームワーク
  - 最初は小さなラベル付きトレーニングセットでモデル化
  - ラベルのない大きなラベルなしデータセットから「最も有益な」サンプルを繰り返し検索
    - 最も有益なサンプルを選択するために最大化される取得関数によって推定
      - 「予想される有益性」を最大にすること（MacKay, 1992）
      - 「予想されるエラー」を最小にすること（Cohn et al., 1996）
      - 高次元のパラメータベクトルに関して予想される誤差から計算されたヘッセ行列の逆行列の推定を必要とするためDLでは最適化するのが難しい
  - ラベル付きサンプルを使って再モデル化

- Houlsby et al（2011）：Bayesian active learning by disagreement（BALD）
  - モデルパラメータに関する学習サンプルの「相互情報」によって獲得関数を測定する
- Gal et al（2017）
  - 取得関数の評価はモデルの不確実性に基づいているため、モデルパラメータの事後分布の近似が必要であることを指摘
  - 取得関数を近似するためにモンテカルロ（MC）ドロップアウト法（Gal＆Ghahramani、2016）の使用を紹介
  - MC近似の収束性が低いにもかかわらず、実際にはうまく機能する
- 提案手法
  - Gal et alの方法を踏襲する



###### Augmentation

- ラベル保存変換（Krizhevsky et al., 2012, Simard et al., 2003, Yaeger et al., 1996）

- ベイジアンデータ拡張（BDA）：Tran et al,. 2017

  - トレーニングセットを使用して生成モデルをトレーニングし、それを使用して新しい人工トレーニングサンプルを作成します

  - 通常のDataAugmentationより良い理論的基礎を持ち、より有益らしい

  - 生成されたサンプルがトレーニングセットに属するという可能性によって新しいトレーニングポイントが生成される

    →トレーニングプロセスが進むにつれて、これらの点は分類子によって正しく分類される可能性が高くなる部分なので、有益ではなくなる

- 提案手法

  - 学習した生成分布に属する可能性が高いだけでなく、トレーニングプロセスにとっても有益なトレーニングサンプルを継続的に生成することを目標とする



###### Generative Active Learning

- 能動学習は有益なサンプルを積極的に生成することによって加速できる

- Zhu＆Bento（2017）：generative adversarial active learning (GAAL)

  - 現在のモデルにとって有益な新しい合成サンプルを生成する

  - GANモデルが事前に訓練されている仮定のもと、豊富な代表的な訓練データを生成できる

  - 取得関数がサンプル生成プロセス中に生成モデルによって使用される

    →計算および最適化（例えば、分類超平面までの距離）が簡単でなければならない

    →→このような単純な獲得関数は能動学習にはあまり有用ではない（Gal et al、2017）

  - GANモデルはトレーニングの進行につれて微調整されない

    →生成モデルと識別モデルは「共進化」しない

- 提案手法

  - 「information content」に基づいてラベルのないデータセットサンプルを問い合わせる
  - 選択されたサンプル上の新しい合成サンプルの生成を条件付ける
  - TrainerとGeneratorは、共同で訓練され「共進化する」

  →最も有益なサンプルから生成された合成サンプルは、その十分に小さい近傍に属する

  →生成されたサンプルにおける取得関数の値は、その数学的最適値（最も有益なサンプル）に近いことが数学的に示されており、したがって合成事例もまた有益である



###### VAE-GAN

- Larsen et al（2016）：VAE-GAN
  - GANの低多様性問題（モード崩壊）に取り組むため、GANとVAEを融合
  - ジェネレータ/デコーダによって接続されている
- 提案手法
  - 分類性能の向上を目的としてACGANとVAE-GANの両方を利用



## 3. “Information-Preserving” Data Augmentation for Active Learning

###### BALD





###### Generative Model





###### Bayesian Data Augmentation





###### Bayesian Generative Active Deep Learning









## 6（前半）Discussion

ベイズ生成的能動学習（AL w. VAEACGAN）がBDAによる能動学習（AL w ACGAN）よりも優れている

特に訓練の後期段階では生成されたサンプルが有益である

提案したアプローチが３つのデータセットに関して他の方法よりも優れている

トレーニングセットの一部で、トレーニングセット全体にわたって10倍のデータ拡張を使用してBDAと同等の分類性能を達成できる

VAEACGANはすべての実験でBDA（部分トレーニング）よりも優れた分類結果を生成し、有益なトレーニングサンプルを生成することの有効性を強化します

生成される画像の品質は驚くほど高い



## 6（後半）Conclusion

- データ拡大や能動的学習よりも効果的なベイズの生成的能動的深層学習アプローチを提案した

- 現在導入されている能動的学習法と組み合わせることもできる