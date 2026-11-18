# VLSAT-3 独立検証証跡

著者: Takarashima, Kenshirou

収録は UNSAT 34 件、SAT 15 件です。UNSAT は VeriPB 3.0.2 と CakePB CP2026 が受理した証明、SAT は無修正の公式入力へ地面代入アサートだけを挿入し Z3 5.4.0・cvc5 1.4.2 で確認したものです。Bitwuzla 0.10.0 は対応ロジックのみ適用し、SKIP_LOGIC は未適用を示します。

独立検算は次の3段階です。

1. `python verify_zenodo_bundle.py --bundle . --checksums-only` で9ファイルのハッシュを照合します。
2. MANIFEST.json の公式URLから元の入力を別途入手し、入力ディレクトリに元のバイト列のまま保存します。検証器は THIRD_PARTY_NOTICES.md の公式配布元から指定バージョンを用意します。
3. `python verify_zenodo_bundle.py --bundle . --official-inputs INPUT_DIRECTORY --report ../verification_report.json` を実行します。実行ファイルの指定方法は英語版を参照してください。レポートは投稿対象外に保存します。

元となる非公開ソルバは黒箱として扱い、ソース、実装、アルゴリズム、実行バイナリを収録しません。速度比較・順位・OSサポートは主張しません。証明再検算が直接保証するのは収録CNFのUNSATです。translation_equivalence は元の公式式からCNFへの局所的な含意の実測記録であり、双方向同値の形式証明ではありません。公開スクリプトはこの変換を再生成せず、局所含意も再実行しません。SAT検査では公式入力の既存バイト列を変更せず、check-sat直前に代入のみ挿入します。

never-solved は指定年の公開された SMT-COMP SingleQuery 成績内の成功数0を意味し、既知の解の不存在や数学的新規性を意味しません。未評価年は評価済みとみなしません。代表ケースは別に表示しています。

アーカイブ2個と検算スクリプトだけの隔離検算にも対応し、スクリプト内のアーカイブハッシュを照合します。9ファイルすべての照合には投稿フォルダ全体が必要です。ライセンスと権利範囲は LICENSE を参照してください。
