```mermaid
graph TD
    %% ノード定義 (ID["表示名<br>説明文"])
    Kimura["木村<br>天から見守っている"];

    Okamoto["岡本<br>リーダー、少しコーディングする"];
    Kikuchi["菊地<br>主にフロントエンドのコーディング"];
    Toyota["豊田<br>主にバックエンドのコーディング"];
    Sasaki["佐々木<br>コードレビュー"];
    Oka["岡<br>リーダーの支援"];

    Okamoto --> Sasaki;
    Okamoto --> Oka;
    Okamoto --> Kikuchi;
    Okamoto --> Toyota;

    Sasaki --> Kikuchi;
    Sasaki --> Toyota;

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
