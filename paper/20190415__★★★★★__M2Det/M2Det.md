# M2Det: A Single-Shot Object Detector based on Multi-Level Feature Pyramid Network

## 甲斐コメント

- 速い、精度高い、分かりやすいを兼ね備えた検出NW。

  ちょっと計算コスト高そうな印象？

  gitにコードが落ちているので試してみるのも簡単。

- 「マルチスケール特徴って本当にそのBackboneでとらえられるのか論」みたいなのが最近ホットな気がしている。

  これもその一端かなと

- こんな甲斐の自己満を読むよりQiita読もうぜ

  <https://qiita.com/kzykmyzw/items/1831f70dcade04db2210>

- ごちゃごちゃいうよりGithub見ようぜ

  https://github.com/qijiezhao/M2Det




## Abstruct

特徴ピラミッド

- オブジェクトインスタンス間のスケール変動から生じる問題を軽減する
  - One-stage Detector：DSSD、RetinaNet、RefineDet
  - Two-stage Detector：Mask RCNN、DetNet
- 特徴ピラミッドを単に構築するだけであるという理由でいくつかの制限がある



提案手法

- Multi-Level Feature Pyramid Network（MLFPN）：より効果的な特徴ピラミッドを構築
- M2Det：MLFPNをSSDのアーキテクチャに統合したをOne-stage Detector
- https://github.com/qijiezhao/M2Detにて公開予定

![キャプチャ2](画像とか\キャプチャ2.PNG)



## 1. Instruction

オブジェクトインスタンス間のスケール変動への対策

- 入力画像をコピーによりサイズ変更
  - テスト時のみ
  - メモリ、計算の複雑さ
- 特徴ピラミッド内のオブジェクトを検出
  - トレーニング、テストの両方
  - メモリ、計算コストが少ない
  - 最先端のDetectorに統合しやすい



特徴ピラミッドの問題点

- ピラミッド内の特徴マップはBackbone依存のため、物体検出タスクに十分に代表的とは限らない
- ピラミッド内の各特徴マップは単一レベルの情報のみを含む
  - 上位レベルの特徴：classificationタスク、複雑な外観を持つオブジェクトに向く
  - 下位レベルの特徴：位置回帰タスク、単純な外観を持つオブジェクトに向く

→最善のパフォーマンスが得られているとは言えない



提案手法：Multi-Level Feature Pyramid Network (MLFPN)

- Backboneによって抽出されたマルチレベル特徴（すなわち、複数の層）を基本特徴として融合

- 基本特徴をThinned U-shape Module と Feature Fusion Module にフィード

  →各U-shape Module の decoder レイヤを物体検出用の特徴として活用

- 物体検出のための特徴ピラミッドを構築するためにデコーダ層集約

  特徴マップは複数レベルの特徴から成るが大きさは同等



## 2. Related Work

とばす



## 3. 提案手法

![キャプチャ](画像とか\キャプチャ.PNG)

- M2Det

  - BackBone + Multi-Level Feature Pyramid Network (MLFPN)

- MLFPN

  - Feature Fusion Module (FFM)
  - Thinned U-shape Module (TUM)
  - Scale-wise Feature Aggregation Module (SFAM)

- MLFPN詳細

  - FFM1：Backboneの特徴マップを融合し、意味情報を特徴マップに足す

  - 各TUM：マルチスケール特徴のグループを生成する

     ⇒交互に結合したTUMとFFMv2：マルチレベルマルチスケール特徴を抽出する

  - SFAM：マルチレベル機能ピラミッドに集約

    - Scale-wise feature concatenation operation
    - Adaptive attention mechanism



#### 3.1 FFM

FFM：さまざまなレベルの機能を融合する

- 入力特徴のチャネルを圧縮するために１×１畳み込み層を使用
- 特徴マップを集約するために連結演算を使用

FFMv1

- バックボーン内のスケールが異なる2つのフィーチャーマップを入力として使用
- 深い特徴をリスケールするためにアップサンプルリングを使用

FFMv2

- 次のTUMのための融合した特徴 = 基本特徴 + 直前のTUMにおける最大の出力特徴マップ



#### 3.2 TUM

- Encoder：Stride 2の3×3畳み込み
- Decoder：アップサンプリング→1x1畳み込み



#### 3.3 SFAM

TUMによって生成されたmulti-level multiscale featuresをmulti-level feature pyramidに集約

- チャネル次元に沿って等価スケールのフィーチャを連結
- channel-wise attention module：SEブロック
  - Squeeze：GAP
  - Excitation：FC層によりattention mechanismの学習



##4. Experiment

画像サイズはBackboneによるが、320x320～800x800くらい

FFM、TUM、SFAMの全てが有効に働いており、TUMは多いほど良いっぽい

精度も速度もSOTAを達成している

