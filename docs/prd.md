# Album Manager Brownfield Enhancement PRD

## Intro Project Analysis and Context

### Existing Project Overview

#### Analysis Source
- IDE-based fresh analysis

#### Current Project State

Album Manager 是一個基於 FastAPI 的專輯收藏管理系統，主要功能包括：

- **用戶管理**：支援多用戶系統，每個用戶可以管理自己的專輯收藏
- **專輯 CRUD 操作**：建立、讀取、更新、刪除專輯記錄
- **基本搜尋功能**：依專輯標題進行不區分大小寫的搜尋
- **條碼檢查**：檢查專輯是否已存在於用戶收藏中
- **MusicBrainz 整合**：透過條碼查詢 MusicBrainz API 獲取專輯資訊

**技術架構：**
- 後端：FastAPI (Python)
- 資料庫：SQLite（可切換 PostgreSQL）
- ORM：SQLAlchemy
- 外部服務：MusicBrainz API

**資料模型：**
- `User`：用戶基本資訊（username）
- `Album`：專輯資訊（title, normalized_title, barcode, artist, owner_id）

### Available Documentation Analysis

#### Available Documentation

- [ ] Tech Stack Documentation
- [ ] Source Tree/Architecture
- [ ] Coding Standards
- [x] API Documentation (部分 - 透過程式碼可見)
- [x] External API Documentation (MusicBrainz 整合)
- [ ] UX/UI Guidelines
- [ ] Technical Debt Documentation

**建議**：建議執行 `document-project` 任務以建立完整的技術文件，特別是架構和編碼標準文件。

### Enhancement Scope Definition

#### Enhancement Type

- [x] New Feature Addition
  - 條碼掃描功能
  - 圖形辨識功能
  - 進階搜尋功能（依藝術家、年份、類型篩選）
  - 專輯封面顯示
  - 詳細資訊展示
- [x] Integration with New Systems
  - 可能需要整合其他音樂資料庫 API（除了現有的 MusicBrainz）
  - 圖形辨識服務整合
- [x] UI/UX Improvements
  - 前端在另一個專案，但需要提供完整的 API 支援

#### Enhancement Description

本次增強將擴展現有的專輯管理系統，新增以下核心功能：

1. **自動辨識功能**：支援條碼掃描和圖形辨識兩種方式，讓使用者可以快速將專輯加入收藏
2. **進階搜尋功能**：提供多維度篩選（藝術家、年份、類型），提升使用者查找專輯的效率
3. **豐富的專輯資訊**：顯示專輯封面和詳細資訊，提升使用者體驗
4. **跨平台支援**：API 設計需同時支援電腦版和手機版前端應用

#### Impact Assessment

- [x] Moderate Impact (some existing code changes)
  - 需要擴展現有的搜尋 API
  - 需要新增資料模型欄位（年份、類型、封面 URL 等）
  - 需要整合新的外部服務（圖形辨識）
  - 需要擴展現有的 MusicBrainz 整合以獲取更多資訊

### Goals and Background Context

#### Goals

- 讓使用者能夠快速且方便地將專輯加入收藏（透過掃描或拍照）
- 提供強大的搜尋和篩選功能，幫助使用者管理大量收藏
- 提供豐富的視覺化資訊（封面、詳細資料），提升使用體驗
- 建立可擴展的 API 架構，支援未來的前端應用開發

#### Background Context

目前系統已經具備基本的專輯管理功能，但對於收藏大量專輯的使用者來說，手動輸入專輯資訊過於繁瑣。此外，現有的搜尋功能僅支援標題搜尋，無法滿足進階需求。

本次增強將大幅提升系統的實用性和使用者體驗，特別針對：
- 需要快速批量新增專輯的使用者（透過掃描/拍照）
- 需要管理大量收藏並需要進階搜尋功能的使用者
- 希望看到視覺化專輯資訊的使用者

### Change Log

| Change | Date | Version | Description | Author |
|--------|------|---------|-------------|--------|
| Initial PRD Creation | 2025-11-23 | v1.0 | Created Brownfield Enhancement PRD | PM Agent |

## Requirements

### Functional Requirements

**注意**：以下需求基於我對現有系統的理解。請仔細審查並確認是否符合您的專案實際情況。

FR1: 系統應支援透過條碼掃描自動辨識專輯並加入收藏
- 使用者可以透過 API 提交條碼
- 系統自動查詢 MusicBrainz 或其他音樂資料庫獲取專輯資訊
- 自動建立專輯記錄並關聯到使用者

FR2: 系統應支援透過圖形辨識（專輯封面照片）自動辨識專輯
- 使用者可以上傳專輯封面圖片
- 系統透過圖形辨識服務識別專輯
- 自動建立專輯記錄

FR3: 系統應提供進階搜尋功能，支援多維度篩選
- 依藝術家名稱搜尋
- 依發行年份篩選
- 依音樂類型/風格篩選
- 支援組合條件搜尋（例如：特定藝術家在特定年份的專輯）

FR4: 系統應顯示專輯封面圖片
- 從 MusicBrainz 或 Cover Art Archive 獲取封面 URL
- 儲存封面 URL 到資料庫
- API 回應中包含封面 URL

FR5: 系統應提供專輯詳細資訊
- 包含藝術家、標題、年份、類型、條碼等完整資訊
- 可選：曲目列表、發行資訊等

FR6: 系統應支援電腦版和手機版前端應用
- API 設計需考慮不同平台的資料需求
- 支援圖片上傳（手機版可能需要）
- 回應格式需適合不同螢幕尺寸的資料展示

### Non-Functional Requirements

NFR1: 系統必須維持現有的效能特性，API 回應時間不應超過現有標準的 150%
- 現有 API 回應時間基準需建立
- 新增功能不應導致整體系統效能明顯下降

NFR2: 圖形辨識 API 回應時間應在合理範圍內（建議 < 5 秒）
- 考慮使用非同步處理或背景任務處理長時間運行的辨識請求

NFR3: 系統應能處理大量專輯資料（數千筆）而不影響搜尋效能
- 需要適當的資料庫索引
- 考慮分頁和快取機制

NFR4: 外部 API 整合應具備錯誤處理和降級機制
- 當 MusicBrainz 或圖形辨識服務不可用時，系統應優雅降級
- 提供適當的錯誤訊息給使用者

NFR5: 資料庫架構變更應向後相容
- 新增欄位應設為可選（nullable）
- 不應破壞現有的 API 合約

### Compatibility Requirements

CR1: 現有 API 端點必須保持向後相容
- 現有的 `/users/{user_id}/albums` GET 端點應繼續運作
- 現有的專輯建立、更新、刪除功能不應受影響
- 現有的搜尋功能（依標題）應繼續運作

CR2: 資料庫架構變更應支援現有資料
- 現有的專輯記錄應能正常運作
- 新增的欄位（年份、類型、封面 URL）應為可選，不影響現有記錄

CR3: 與 MusicBrainz 的現有整合應保持運作
- 現有的 `/api/search/barcode/{barcode}` 端點應繼續運作
- 新的功能應擴展而非取代現有整合

CR4: 前端整合相容性
- API 回應格式應考慮現有和未來的前端需求
- 不應破壞任何現有的前端整合（如果存在）

## User Interface Enhancement Goals

### Integration with Existing UI

**注意**：前端目前在另一個專案中。本節主要描述 API 設計如何支援前端 UI 需求。

API 設計應提供：
- 結構化的 JSON 回應，適合前端渲染
- 圖片 URL 而非直接傳輸圖片資料（減少頻寬）
- 分頁和排序參數，支援前端表格/列表展示
- 搜尋和篩選參數，支援前端篩選 UI 元件

### Modified/New Screens and Views

**後端 API 端點（新增/修改）：**

新增端點：
- `POST /users/{user_id}/albums/scan` - 條碼掃描辨識
- `POST /users/{user_id}/albums/recognize` - 圖形辨識
- `GET /users/{user_id}/albums/search` - 進階搜尋（取代或擴展現有的搜尋）

修改端點：
- `GET /users/{user_id}/albums` - 擴展回應以包含封面 URL 和詳細資訊
- `GET /users/{user_id}/albums/{album_id}` - 新增詳細資訊端點

### UI Consistency Requirements

- API 回應格式應保持一致（統一的 JSON 結構）
- 錯誤回應格式應遵循 FastAPI 標準
- 圖片 URL 應使用 HTTPS 並提供備用方案

## Technical Constraints and Integration Requirements

### Existing Technology Stack

**Languages**: Python 3.x

**Frameworks**: 
- FastAPI 0.115.12
- SQLAlchemy 2.0.40
- Pydantic 2.11.4

**Database**: 
- SQLite (開發環境)
- PostgreSQL (生產環境，透過 psycopg2 2.9.10)

**Infrastructure**: 
- Uvicorn 0.34.2 (ASGI 伺服器)
- 目前為單體應用，無容器化配置

**External Dependencies**:
- MusicBrainz API (現有整合)
- httpx 0.28.1 (HTTP 客戶端)

### Integration Approach

**Database Integration Strategy**: 
- 使用 Alembic 進行資料庫遷移（已在 requirements.txt 中）
- 新增欄位：`year` (Integer, nullable), `genre` (String, nullable), `cover_url` (String, nullable)
- 建立適當的索引以支援進階搜尋

**API Integration Strategy**: 
- 擴展現有的 FastAPI 路由結構
- 使用 Pydantic schemas 定義新的請求/回應模型
- 保持 RESTful API 設計原則

**Frontend Integration Strategy**: 
- 提供完整的 OpenAPI/Swagger 文件（FastAPI 自動生成）
- 確保 CORS 設定支援前端應用
- 設計 API 回應格式以支援前端需求

**Testing Integration Strategy**: 
- 擴展現有的測試結構（如果存在）
- 為新功能建立單元測試和整合測試
- 模擬外部 API（MusicBrainz、圖形辨識服務）進行測試

### Code Organization and Standards

**File Structure Approach**: 
- 保持現有的模組化結構（models.py, schemas.py, main.py）
- 考慮將新的服務（圖形辨識）分離到獨立的服務檔案
- 遵循現有的檔案命名慣例

**Naming Conventions**: 
- 遵循 Python PEP 8 命名慣例
- API 端點使用小寫和連字號（kebab-case）
- 變數和函數使用 snake_case

**Coding Standards**: 
- 使用型別提示（type hints）
- 使用 Pydantic 進行資料驗證
- 適當的錯誤處理和日誌記錄

**Documentation Standards**: 
- API 端點應包含 docstrings
- 使用 FastAPI 的自動文件生成功能
- 複雜邏輯應包含註解

### Deployment and Operations

**Build Process Integration**: 
- 使用現有的 requirements.txt 管理依賴
- 確保新依賴不會與現有依賴衝突

**Deployment Strategy**: 
- 資料庫遷移應在部署前執行
- 確保向後相容性，避免服務中斷

**Monitoring and Logging**: 
- 記錄外部 API 呼叫（MusicBrainz、圖形辨識）
- 監控 API 回應時間和錯誤率
- 記錄圖片上傳和處理活動

**Configuration Management**: 
- 使用環境變數管理外部 API 金鑰和端點
- 使用 python-dotenv 載入配置（已存在）

### Risk Assessment and Mitigation

**Technical Risks**: 
- **圖形辨識服務選擇和整合**：需要評估不同的圖形辨識服務（Google Vision API, AWS Rekognition, 或其他）
  - *緩解*：先進行概念驗證，評估準確性和成本
- **大量圖片上傳的儲存和處理**：如果直接儲存圖片，需要考慮儲存空間
  - *緩解*：僅儲存圖片 URL，不儲存實際圖片檔案
- **外部 API 依賴**：MusicBrainz 和圖形辨識服務的可用性
  - *緩解*：實作錯誤處理、重試機制和降級策略

**Integration Risks**: 
- **資料庫遷移風險**：新增欄位可能影響現有資料
  - *緩解*：所有新欄位設為 nullable，使用 Alembic 進行安全的遷移
- **API 向後相容性**：新功能可能意外破壞現有整合
  - *緩解*：完整的測試覆蓋，特別是現有 API 端點的迴歸測試

**Deployment Risks**: 
- **資料庫遷移執行順序**：需要確保遷移在應用程式啟動前完成
  - *緩解*：建立明確的部署流程和檢查清單

**Mitigation Strategies**: 
- 分階段實作：先實作條碼掃描和進階搜尋，再實作圖形辨識
- 完整的測試：單元測試、整合測試、端對端測試
- 監控和日誌：及早發現問題
- 文件化：確保團隊理解新功能和整合點

## Epic and Story Structure

### Epic Approach

**Epic Structure Decision**: 單一綜合 Epic

**Rationale**: 
本次增強雖然包含多個功能，但這些功能都是圍繞「提升專輯辨識和管理體驗」這個核心目標。所有功能相互關聯：
- 條碼掃描和圖形辨識都是為了快速新增專輯
- 進階搜尋是為了管理新增的大量專輯
- 封面和詳細資訊是為了提升使用體驗

將這些功能組織在單一 Epic 中可以：
1. 確保功能之間的協調和一致性
2. 按邏輯順序實作，每個 Story 都建立在之前的基礎上
3. 更容易管理整體進度和風險

## Epic 1: 專輯自動辨識與進階管理功能增強

**Epic Goal**: 
擴展現有的專輯管理系統，新增自動辨識功能（條碼掃描和圖形辨識）、進階搜尋功能，以及豐富的專輯資訊展示，大幅提升使用者體驗和系統實用性。

**Integration Requirements**: 
- 必須保持現有 API 的向後相容性
- 必須支援現有的資料結構和資料
- 必須與現有的 MusicBrainz 整合協同工作
- 必須提供完整的 API 文件以支援前端開發

### Story 1.1: 擴展資料模型以支援新功能

**As a** 系統開發者,  
**I want** 擴展 Album 資料模型以包含年份、類型和封面 URL 欄位,  
**so that** 系統可以儲存和展示更豐富的專輯資訊。

#### Acceptance Criteria

1. 使用 Alembic 建立資料庫遷移腳本
2. 在 Album 模型中新增以下欄位（全部為 nullable）：
   - `year` (Integer, nullable)
   - `genre` (String(100), nullable)
   - `cover_url` (String(500), nullable)
3. 更新 Pydantic schemas (AlbumCreate, AlbumUpdate, AlbumOut) 以包含新欄位
4. 現有的專輯記錄不受影響（新欄位為 NULL）
5. 現有的 API 端點繼續正常運作
6. 資料庫遷移可以安全地回滾

#### Integration Verification

IV1: 驗證現有的專輯建立、讀取、更新、刪除功能仍然正常運作
IV2: 驗證現有的搜尋功能（依標題）不受影響
IV3: 驗證現有資料在遷移後完整保留
IV4: 驗證新欄位可以正確儲存和讀取

---

### Story 1.2: 擴展現有 MusicBrainz 整合以獲取完整專輯資訊

**As a** 使用者,  
**I want** 系統從 MusicBrainz 獲取專輯的完整資訊（年份、類型、封面）,  
**so that** 我新增專輯時可以自動填入這些資訊。

#### Acceptance Criteria

1. 擴展現有的 `musicbrainz_service.py` 以從 MusicBrainz API 獲取年份、類型和封面 URL
2. 更新 `search_by_barcode` 方法以返回完整的專輯資訊
3. 處理 MusicBrainz API 回應中可能缺失的欄位（優雅降級）
4. 驗證封面 URL 的有效性（可選：檢查 URL 是否可訪問）
5. 更新現有的 `/api/search/barcode/{barcode}` 端點以返回新資訊
6. 現有的條碼搜尋功能繼續運作

#### Integration Verification

IV1: 驗證現有的條碼搜尋端點返回新資訊但不破壞現有整合
IV2: 驗證當 MusicBrainz API 不可用時，系統優雅降級
IV3: 驗證新資訊正確儲存到資料庫

---

### Story 1.3: 實作條碼掃描自動辨識功能

**As a** 使用者,  
**I want** 透過提交條碼自動辨識並新增專輯到我的收藏,  
**so that** 我可以快速批量新增專輯而不需要手動輸入。

#### Acceptance Criteria

1. 建立新的 API 端點 `POST /users/{user_id}/albums/scan`
2. 接受條碼作為輸入參數
3. 自動查詢 MusicBrainz 獲取專輯資訊
4. 自動建立專輯記錄並關聯到使用者
5. 處理重複專輯的情況（返回現有專輯或錯誤訊息）
6. 處理 MusicBrainz 找不到專輯的情況（返回適當錯誤）
7. 返回建立的專輯資訊（包含所有新欄位）
8. 提供適當的錯誤處理和日誌記錄

#### Integration Verification

IV1: 驗證新端點不影響現有的專輯建立端點
IV2: 驗證重複檢查邏輯與現有邏輯一致
IV3: 驗證新建立的專輯包含完整的資訊（年份、類型、封面等）

---

### Story 1.4: 實作進階搜尋功能

**As a** 使用者,  
**I want** 使用多個條件（藝術家、年份、類型）搜尋我的專輯收藏,  
**so that** 我可以快速找到特定的專輯。

#### Acceptance Criteria

1. 擴展現有的 `GET /users/{user_id}/albums` 端點以支援進階篩選
2. 新增查詢參數：
   - `artist` (可選): 依藝術家名稱篩選（不區分大小寫）
   - `year` (可選): 依年份篩選（支援範圍，例如 `year_min` 和 `year_max`）
   - `genre` (可選): 依類型篩選（不區分大小寫）
   - `title` (可選): 保留現有的標題搜尋功能
3. 支援組合條件搜尋（多個條件同時使用）
4. 保持現有的排序功能（依標題）
5. 新增適當的資料庫索引以優化搜尋效能
6. 現有的簡單搜尋（僅標題）繼續運作
7. 提供適當的錯誤處理（例如：無效的年份範圍）

#### Integration Verification

IV1: 驗證現有的標題搜尋功能不受影響
IV2: 驗證新索引不影響寫入效能
IV3: 驗證組合條件搜尋返回正確結果
IV4: 驗證搜尋效能在大量資料下仍然可接受

---

### Story 1.5: 實作圖形辨識功能

**As a** 使用者,  
**I want** 透過上傳專輯封面圖片自動辨識並新增專輯,  
**so that** 我可以使用手機拍照快速新增專輯。

#### Acceptance Criteria

1. 選擇並整合圖形辨識服務（例如：Google Vision API 或 AWS Rekognition）
2. 建立新的 API 端點 `POST /users/{user_id}/albums/recognize`
3. 接受圖片上傳（支援常見格式：JPEG, PNG）
4. 呼叫圖形辨識服務識別專輯
5. 使用識別結果查詢 MusicBrainz 或直接建立專輯記錄
6. 處理圖片上傳失敗、辨識失敗等錯誤情況
7. 實作適當的圖片大小和格式驗證
8. 考慮非同步處理（如果辨識時間較長）
9. 提供適當的錯誤處理和使用者回饋

#### Integration Verification

IV1: 驗證圖片上傳不影響其他 API 端點的效能
IV2: 驗證辨識失敗時系統優雅降級
IV3: 驗證辨識結果正確轉換為專輯記錄
IV4: 驗證與條碼掃描功能的一致性（相同的專輯建立邏輯）

---

### Story 1.6: 擴展現有 API 回應以包含完整專輯資訊

**As a** 前端開發者,  
**I want** API 回應包含專輯的完整資訊（封面 URL、年份、類型等）,  
**so that** 我可以在前端展示豐富的專輯資訊。

#### Acceptance Criteria

1. 更新 `AlbumOut` schema 以包含所有新欄位
2. 更新所有返回專輯資訊的 API 端點：
   - `GET /users/{user_id}/albums` - 列表回應
   - `GET /users/{user_id}/albums/{album_id}` - 單一專輯回應（如果不存在則建立）
   - `POST /users/{user_id}/albums` - 建立回應
   - `PUT /users/{user_id}/albums/{album_id}` - 更新回應
3. 確保所有端點返回一致的資料格式
4. 處理 NULL 值（當專輯沒有某些資訊時）
5. 更新 API 文件（FastAPI 自動生成）

#### Integration Verification

IV1: 驗證所有現有 API 端點返回新格式但不破壞現有前端整合
IV2: 驗證資料格式一致性
IV3: 驗證 NULL 值正確處理

---

### Story 1.7: 建立專輯詳細資訊端點

**As a** 前端開發者,  
**I want** 有一個專門的端點獲取專輯的詳細資訊,  
**so that** 我可以在專輯詳情頁面展示完整資訊。

#### Acceptance Criteria

1. 建立新的 API 端點 `GET /users/{user_id}/albums/{album_id}/details`
2. 返回專輯的完整資訊，包括：
   - 基本資訊（標題、藝術家、年份、類型、條碼）
   - 封面 URL
   - 可選：從 MusicBrainz 獲取額外資訊（曲目列表等）
3. 處理專輯不存在的情況
4. 驗證使用者權限（只能查看自己的專輯）
5. 提供適當的錯誤處理

#### Integration Verification

IV1: 驗證權限檢查正確運作
IV2: 驗證回應格式與其他端點一致
IV3: 驗證錯誤處理適當

---

## Story Sequencing Rationale

這個 Story 順序設計旨在：

1. **最小化風險**：從資料模型擴展開始，確保基礎穩固
2. **逐步建立**：每個 Story 建立在之前的基礎上
3. **向後相容**：每個 Story 都確保不破壞現有功能
4. **價值遞增**：每個 Story 都提供可用的功能，即使後續 Story 未完成

**順序說明**：
- Story 1.1-1.2: 建立基礎（資料模型和資料來源）
- Story 1.3: 實作第一個自動辨識功能（條碼掃描，較簡單）
- Story 1.4: 實作搜尋功能（使用新資料）
- Story 1.5: 實作較複雜的圖形辨識功能
- Story 1.6-1.7: 完善 API 回應和詳細資訊

這個順序是否符合您專案的架構和約束條件？

