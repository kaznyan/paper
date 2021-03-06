# Pyramid Mask Detector



## 甲斐コメント

ソフトラベルを使い、「Anchorの中心は凄く物体っぽいけど外縁はほぼ背景っぽい」という感じを再現。

Segmentationで学習することでPixcelごとに「物体っぽさ」をちゃんと推論。

→やっぱSoft Labelは最高やな

推論結果に対して「pyramid」で近似して一番しっくりくる4点座標を決めることで歪んだ四角形も再現可能。

→ここのアルゴリズム天才的



## Abstruct

フォーカス対象：シーンテキスト検出

- Mask R-CNNによるセグメンテーションで高精度
- バイナリテキストマスク



提案手法：Pyramid Mask Detector（PMTD）

- 内容：Mask R ‐ CNNベースのフレームワーク

  - マスク：位置を意識した教師あり学習でピクセルレベルの回帰

    →より有益なソフトテキストマスク

  - テキストボックスの生成：PMTDは得られた2Dソフトマスクを3D空間に再解釈

    →3D形状に基づいた最適なテキストボックス導出のための、新規な平面クラスタリングアルゴリズム

- 結果：標準的なデータセットに関する実験

  →提案されたPMTDが首尾一貫した顕著な利益

  →ICDAR 2017 MLTデータセットでF値80.13％（SOTA）

  

## 1. Introduction

シーンテキスト検出：Mask R-CNNベースの方法が主流

Mask R-CNNベースの欠点

- 過度に簡素化された教師あり学習
  - Mask R-CNNベースの方法では、ほとんどのテキスト領域が四辺形であるという知識を活用できない
    - 特定の形状のテキストマスクを生成するのではなくテキスト領域を背景領域から区別する

- 不正確なセグメンテーションラベル

  - テキスト領域に属さない多くの背景ピクセルは誤って前景ピクセルと見なされる

    ⇒ノイズの多いデータ

- エラー伝播

  - テキスト境界ボックス→境界ボックス内で意味的セグメンテーション
    - 予測される境界ボックスがテキスト領域全体をカバーできない場合は脆弱
      - バウンディングボックスの内側のテキスト領域のみでテキストボックスを決定することは外側部分を除外する傾向がある
      - オブジェクト検出からのエラーは、テキストボックスを見つけるプロセスに伝播され、シーンテキスト検出の性能低下を招く



提案手法：PMTD

- ピクセルレベルのバイナリ分類の代わりに、テキスト領域と背景領域との間の「ソフト」セマンティックセグメンテーションを実行

  ⇒暗黙的に形状と位置の情報をトレーニングデータにエンコード

  　⇒テキストインスタンスの四辺形特性を考慮

  　⇒テキストボックスの境界近くの誤ってラベル付けされたピクセルの影響を減らす

- 推論時は、ピクセルレベルのセグメンテーション出力の値を特徴付ける拡張z軸を使用

  - 2D予測テキストマスクを3Dポイントのセットに再解釈

  - これらの三次元点から最適ピラミッドを回帰するために平面クラスタリングアルゴリズムを提案
    - ピラミッドの４つの初期化された支持平面を用いて起動された平面クラスタリングアルゴリズムは、支持平面ごとに最も近い点を反復的にグループ化し、次いでクラスタ化された点によって支持平面を更新する。反復後、正確なバウンディングピラミッドが得られ、その底面が出力テキストボックスと見なされる

- 貢献

  - 多くのベンチマークデータセットでSOTA
  - 「ソフト」セグメンテーションにより、形状と位置の情報をモデルトレーニングに組み込み、インスタンス境界の不正確なラベリングを軽減
  - 3D座標でより良いテキストボックスを見つけるための新しい平面クラスタリングアルゴリズム

![キャプチャ](画像\キャプチャ.PNG)



## 2. RelatedWork

シーンテキスト検出は過去数年間にわたって大きな注目を集めており、多数のディープラーニングベースの方法［５、４５、２２、３２、４６、１０、２０、２９、４１］が文献に報告されている。包括的なレビューと詳細な分析は調査報告書にあります[47、40、43]。

［１３、１６、１５］を含む初期のテキスト検出作業は、最初のディープニューラルネットワークベースの方法の１つである。それらは通常、候補の集約、単語分割、後処理フィルタリングによる誤検知除去など、複数の段階で構成されています。黄等。 [13]最初に入力画像にMSER演算子を適用していくつかのテキスト候補を生成し、次にCNN分類器を使用して信頼マップを生成し、これを後でテキスト行の構築に使用しました。 Jaderberg他。 [16]テキストの顕著性マップを生成するために強く監視された文字分類器を訓練し、次に複数のスケールで境界ボックスを結合し、フィルタリングと非最大抑制を受ける。後の研究[15]では、彼らはバウンディングボックス回帰のためにCNNを利用し、誤検出の数を減らすためにランダムフォレスト分類器を利用しています。

最近の研究[5、39、23、45]は、テキストの単語や行をオブジェクトと見なし、一般的なオブジェクト検出のパイプライン、例えばFaster R-CNN [36]、SSD [25]、YOLO [35]をテキスト検出に適用します。それらは、提案領域または特徴マップ内の単一のピクセルからの水平方向の長方形へのオフセットを後退させ、水平方向のテキスト検出に対する適切に設計された修正によって良好な性能を得る。グプタ等。 [5]はテキスト予測のためにYOLOネットワークとFully Convolutional Networks（FCN）[28]を改良し、さらに誤検出を除去するためのフィルタと回帰のステップを採用しています。 TextBoxes [23]は、シーンテキストの特性に応じて、不規則なたたみ込みカーネルと長いデフォルトアンカーを使用してSSDを修正します。 FTP R-CNNの上に構築されたCTPN [39]は、各固定幅プロポーザルの位置とテキスト/非テキストスコアを同時に予測し、次にリカレントニューラルネットワークによって順次プロポーザルを接続する垂直アンカーメカニズムを開発します。 FEN [45]は、機能強化RPNとテキスト検出改良のためのハイパー機能生成により、テキストの思い出しを改善します。

シーンテキストが任意の向きであることを考慮すると、［２２、３２、４６、１０、２６、９］の作品は、多方向テキスト検出のために上記の方法を可能にする。 RRPN [32]は、任意指向のテキスト予測のための角度情報と回転RoIプーリング層を持つ傾斜アンカーを導入し、任意指向の提案をテキスト領域分類器の特徴マップに射影します。 TextBoxes ++ [22]は、テキストを囲むより一般的な四辺形への水平アンカーを後退させることでTextBoxを改善します。それはまた、四辺形または回転された長方形のための効率的な縦続非最大抑制を提案する。密な予測と1ステップの後処理で、EAST [46]とDDR [10]は両方ともテキスト領域の各点に回転ボックスまたは四角形のテキストを直接生成します。 FOTS [26]やHe et al。のような最近のテキストスポッティング方法。 [9]は、テキストの検出と認識を同時に訓練することで、検出性能が大幅に向上することを示しています。

上記の回帰に基づく方法を除いて、[3、20、29、41]はセグメンテーション問題としてテキスト検出を行います。 PixelLink [3]は最初に同じインスタンス内のピクセルをリンクすることによってテキスト領域をセグメント化し、次に位置回帰なしでセグメンテーションから直接テキスト境界ボックスを抽出する。

TextSnake [29]は、FCN [28]モデルを使用してテキストインスタンスのジオメトリ属性を推定し、ストライディングアルゴリズムを使用して中心軸点リストを抽出し、最後にテキストインスタンスを再構築します。

セグメンテーションベースの方法は、隣接するテキスト領域を互いに誤ってリンクする傾向がある。この問題に対処するために、PSENet [20]はさまざまなスケールのテキストカーネルを見つけ、互いに正確に近いテキストインスタンスを分離するためのプログレッシブスケール拡張アルゴリズムを提案します。 SPCNET [41]は、Mask R-CNNに基づいて、テキスト検出をインスタンスセグメンテーション問題と見なし、誤検出を抑制するためのテキストコンテキストモジュールと再スコア化メカニズムを提案します。

曲面テキスト検出[1、44]は最近ますます研究関心を集めていますが、四辺形テキスト検出は依然として解決されるべき根本的で挑戦的な問題です。 PMTDは四辺形のテキスト検出用に特別に設計されており、ICDAR 2017 MLTの最先端の結果を74.3％から14.18％に大幅に向上させます。

## 3. 理論

お品書き

- 強力なベースライン

- ソフトピラミッドラベルを提案

- 予測されたソフトテキストマスクの最も適合するピラミッドを見つけるための平面クラスタリング



#### 3.1 ベースライン

- ResNet50バックボーンを持つMask R-CNN

- トレーニング段階
  - テキスト領域の軸合わせ境界矩形をグラウンドトゥルース境界ボックスとして扱う
  - テキスト境界内のピクセルをポジティブセグメンテーションラベルに割り当てる
- テスト段階
  - 最初に予測マスク内のすべての接続領域を見つける
  - 次に最大領域を持つ接続領域を選択する
  - 最後にこの接続領域の最小外接矩形を見つける
- 3つの変更を加えて強力にする
  - Data Augmentation
  - FPNに対するAnchor設定
  - Online Hard Sample Mining (OHEM)



## 3.2 PMTDのMotivation

Baseline時点での欠点：Introductionで述べた通り

⇒PMTD

- 各テキスト領域についてソフトテキストマスクを予測
- 予測されたソフトマスクをピラミッドマスクに変換するために平面クラスタリングを適用



## 3.3 Pyramid Label

ソフトラベルの話。簡単なので飛ばす



## 3.4 平面クラスタリング

推論時の話（テキスト領域からピラミッドラベルを生成することの逆に相当するプロセス）。

- テキストマスクからピラミッド
- ピラミッドの下端を出力テキストボックスとして取得

⇒ピラミッドをパラメータ化して再構築することが重要



平面クラスタリングアルゴリズムのタスク：

　Ax + By + Cz + D = 0, C = 1

を満たす最適なパラメータ｛Ａ、Ｂ、Ｄ｝を見つけること



![キャプチャ2](画像\キャプチャ2.PNG)

アルゴリズム：

- Maskの推論地との誤差が小さくなるように4面の位置を反復的に移動させる回帰
- 最終的なテキストボックスは、4面とz = 0の交点



## 4. 実験と結果

- 精度あがった
- 不正確なラベルに対してRobustだった