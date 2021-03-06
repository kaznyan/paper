# Implementing the Deep Q-Network

## Abstruct

- 各論文の正しいハイパーパラメータ設定まとめ
- 各論文の実装のポイントまとめ
- 計算パフォーマンスを向上させる方法について
- 元のアーケード学習環境だけでなく、さまざまなドメインで機能する独自の実装の紹介

## Introduction

- DQNのベンチマーク：Mnih et al.

  - 主な貢献：学習中のNNの安定性を改善する方法
  - 課題：方法論以外に不透明な点が多い

  →この論文ではそこを解決してまとめた

- MnihらAtariより約4倍速く、かつ様々なアーキテクチャや問題ドメインに対応できる実装をした

  - 無料公開中
- 実装に関するいくつかの重要な洞察を発見
  - 良好なパフォーマンスに不可欠なもの
  - Mnihの結果を再現するために不可欠なテクニック
    - 終了条件
    - 勾配降下最適化アルゴリズム
  - アルゴリズムの期待される結果

## Related Work

- マルコフ決定プロセス（MDP）[Bellman、1957]

  - 強化学習問題に使用される典型的な定式化

  - 5タプル（S、A、T、R、E）で定義

    - S：エージェントの状態空間

    - A：エージェントのアクションスペース

    - T（s、a、s0）：遷移ダイナミクス

      状態sでアクションaを実行すると状態s0になる確率

    - R（s、a、s0）：報酬関数

      状態sでアクションaを実行した後、状態s0に遷移したときに受け取った報酬

    - E⊂S：最終状態

  - 目標：状態πからアクションへのマッピングπ：S→Aを見つけること

  - Q関数

    - 状態sでアクションaを実行し、その後ポリシーπを実行するために予想される将来の割引報酬
    - Bellman方程式を用いて重要な性質が表現される

- Qラーニング [Watkins、1989]

  - 環境内で任意のアクションを実行し、報酬と次の状態を観察し、Q関数推定を繰り返し更新
  - QがQ*に収束する条件
    - Q関数推定が表形式
    - t→∞
  - 問題の状態空間が 大きい場合、関数近似で実装することが多い
    - 関数近似の推定誤差により、Q学習（その他のoff-policyメソッドも）発散する可能性あり [Baird et al。、1995]

## DQN

- 3つの主要な貢献
  - Q関数近似用のDeep CNN
  - ランダムなトレーニングデータのミニバッチによる学習（Experiecne Replay）
    - 経験の履歴（s、a、s0、r、T）を保持
      - 状態sでアクションaをとり、状態s0に到着し、報酬rを受け取る
      - Tは、s0が最終状態かどうか
      - 環境の各ステップの後、エージェントはエクスペリエンスをメモリに追加
    - 報酬のバックアップを加速
    - 環境のサンプルを無相関化
  - 古いネットワークパラメータを使用して、次の状態のQ値を推定
    - 安定したトレーニングターゲットを提供
- Mnihらの報告と同じレベルのパフォーマンスを達成するために**必要な詳細**がほかにもある



## 元論文に明示されていない学習のテクニック

元の論文ではさらっと流されていた重要ポイントの解説。

#### 実行方法

- 全てのエピソードは0〜30のランダムな「操作なし」アクションで開始
  - エージェントが見るフレームをオフセットするため
- 任意の勾配降下ステップの前にランダムなポリシーで50,000ステップ実行する
  - 初期の経験への過剰適合を回避するために経験を足す

#### 終了条件

- 終了時でなくライフ喪失時に学習打ち切り
  - 常識的にマイナスなものは避けるようにするということ
  - ロボットとかの実用タスクだと「終了」を強制的に指令できる方法を用意しなければならない

#### 学習方法

- 4つステップごとに勾配降下
  - トレーニング速度が大幅に向上
  - 経験のメモリが現在のポリシーの状態分布により近くなる（4つずつ追加するので）
  - ネットワークの過剰適合を防ぐことができる

- 最良のパフォーマンスをもたらしたネットワークパラメータを保存しておく
  - DQNの「破滅的な忘却」は突然起こる
    - ベルマン更新を使用して大規模な状態空間でQ関数を近似することが本質的な不安定なため
      - 対策：Experience Replay、古いネットワークの使用、勾配のクリップなど
      - 完全には対策できていない
  - ポリシーを直接計算せず、Q値を学習しているため
    - Q関数近似の精度が向上しても、生成されるポリシーのパフォーマンスが低下する可能性がある
  - 同じ状態、異なるアクションのQ値が非常に近いことがある
    - 小さな差は長期的な報酬の結果であるため重要
    - Q値に小さなエラーがあるだけでも異なるポリシーを選択し、長期的なポリシーの学習が困難

#### 勾配降下法のカスタマイズ

- Mnihらの実装では、多くのディープラーニングライブラリが提供するものと同じRMSProp定義を使用していない
- RMSPropの定義はそのままに、学習率を下げることで対応可能（0.00025ではなく0.00005）



## 結果

- エージェントを50,000,000ステップでトレーニング

  - この研究による実装：約3日
    - GPUとかライブラリの使い方によるもの。
  - 論文の実装：約10日半

- 250,000ステップごとにパフォーマンスをテスト

  - 論文と異なるパフォーマンス

    →勾配降下最適化アルゴリズムと学習率の違いに起因（後述）



## 結論

- MnihらのDQNを実装する際の重要なポイントを示した
- 大きな状態空間でQ関数をCNNで近似することの難しさを強調
- オンラインで自由に利用できる実装