```mermaid
graph TD
    subgraph "部署與儲存"
        A[GitHub Repository<br/><i>程式碼儲存</i>]:::github
    end

    subgraph "後端服務 (Render)"
        B[Flask App<br/><i>app.py</i>]:::render
        C[Stock Price<br/><i>stockprice.py</i>]:::module
        D[Technical Analysis<br/><i>Technical_Analysis_test.py</i>]:::module
        E[News Fetcher<br/><i>news.py</i>]:::module
        F[Message Formatter<br/><i>Msg_News.py</i>]:::module
        B -->|調用| C
        B -->|調用| D
        B -->|調用| E
        E -->|格式化| F
    end

    subgraph "外部服務"
        G[Imgur<br/><i>圖表儲存</i>]:::external
        H[Yahoo Finance<br/><i>數據來源</i>]:::external
    end

    subgraph "LINE 平台"
        I[LINE Developers<br/><i>Webhook & API</i>]:::line
    end

    subgraph "用戶端"
        J[Mobile User<br/><i>LINE App</i>]:::user
    end

    %% 資料流
    A -->|部署| B
    J -->|查詢 (e.g., N0050)| I
    I -->|Webhook| B
    C -->|獲取數據| H
    D -->|獲取數據| H
    E -->|獲取新聞| H
    C -->|上傳圖表| G
    D -->|上傳圖表| G
    G -->|返回 URL| B
    B -->|推送回應| I
    I -->|顯示| J

    %% 樣式定義
    classDef github fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#24292e;
    classDef render fill:#e6f3ff,stroke:#0066cc,stroke-width:2px,color:#0066cc;
    classDef module fill:#cce5ff,stroke:#0066cc,stroke-width:1px,color:#004080;
    classDef external fill:#fff3e6,stroke:#ff6600,stroke-width:2px,color:#ff6600;
    classDef line fill:#e6ffe6,stroke:#00cc00,stroke-width:2px,color:#008000;
    classDef user fill:#f2e6ff,stroke:#6600cc,stroke-width:2px,color:#6600cc;
