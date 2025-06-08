```mermaid
graph TD
    %% ノード定義 (ID["表示名<br>説明文"])
    Kimura["木村<br>天から見守っている"];

    Okamoto["岡本<br>リーダー、少しコーディングする"];
    Kikuchi["菊池<br>主にフロントエンドのコーディング"];
    Toyota["豊田<br>主にバックエンドのコーディング"];
    Sasaki["佐々木<br>コードレビュー"];
    Oka["岡<br>リーダーの支援"];

    %% 上下関係とつながり
    %% 木村は最上位で誰ともつながっていないため、単独で定義します。
    %% Mermaidのレイアウトで一番上または独立した位置に表示されることを期待します。

    %% 岡本がリーダーとして中心的な役割
    Okamoto --> Sasaki;  %% 岡本の下に佐々木
    Okamoto --> Oka;     %% 岡本の下に岡 (これで佐々木と岡が同列に見えやすくなります)

    %% 岡本と開発者のつながり
    Okamoto --> Kikuchi; %% 岡本と菊池がつながる
    Okamoto --> Toyota;  %% 岡本と豊田がつながる

    %% 佐々木と開発者のつながり
    Sasaki --> Kikuchi;  %% 佐々木と菊池がつながる (コードレビュー)
    Sasaki --> Toyota;   %% 佐々木と豊田がつながる (コードレビュー)

    %% 岡と岡本のつながりは Okamoto --> Oka で表現済み（岡本が上で岡が下）

    %% これで、指定された上下関係「木村、岡本、佐々木=岡、菊池=豊田」を意図した構造になります。
    %% ・木村は独立して最上位に配置されることを想定
    %% ・岡本が木村の下 (直接線はないが、他のメンバーの起点となる)
    %% ・佐々木と岡が岡本の下で同列
    %% ・菊池と豊田が佐々木の下 (かつ岡本とも接続) で同列

    %% ノードのスタイル (任意で見栄えを調整)
    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef leader fill:#ccf,stroke:#333,stroke-width:2px;
    classDef coder fill:#cfc,stroke:#333,stroke-width:2px;
    classDef support fill:#ffc,stroke:#333,stroke-width:2px;
    classDef special fill:#eee,stroke:#333,stroke-width:1px;

    class Kimura special;
    class Okamoto leader;
    class Kikuchi coder;
    class Toyota coder;
    class Sasaki support;
    class Oka support;
