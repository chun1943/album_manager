# Epic 1: 專輯自動辨識與進階管理功能增強

**Epic Goal**: 
擴展現有的專輯管理系統，新增自動辨識功能（條碼掃描和圖形辨識）、進階搜尋功能，以及豐富的專輯資訊展示，大幅提升使用者體驗和系統實用性。

**Integration Requirements**: 
- 必須保持現有 API 的向後相容性
- 必須支援現有的資料結構和資料
- 必須與現有的 MusicBrainz 整合協同工作
- 必須提供完整的 API 文件以支援前端開發

## Story 1.1: 擴展資料模型以支援新功能

**As a** 系統開發者,  
**I want** 擴展 Album 資料模型以包含年份、類型和封面 URL 欄位,  
**so that** 系統可以儲存和展示更豐富的專輯資訊。

### Acceptance Criteria

1. 使用 Alembic 建立資料庫遷移腳本
2. 在 Album 模型中新增以下欄位（全部為 nullable）：
   - `year` (Integer, nullable)
   - `genre` (String(100), nullable)
   - `cover_url` (String(500), nullable)
3. 更新 Pydantic schemas (AlbumCreate, AlbumUpdate, AlbumOut) 以包含新欄位
4. 現有的專輯記錄不受影響（新欄位為 NULL）
5. 現有的 API 端點繼續正常運作
6. 資料庫遷移可以安全地回滾

### Integration Verification

IV1: 驗證現有的專輯建立、讀取、更新、刪除功能仍然正常運作
IV2: 驗證現有的搜尋功能（依標題）不受影響
IV3: 驗證現有資料在遷移後完整保留
IV4: 驗證新欄位可以正確儲存和讀取

---

## Story 1.2: 擴展現有 MusicBrainz 整合以獲取完整專輯資訊

**As a** 使用者,  
**I want** 系統從 MusicBrainz 獲取專輯的完整資訊（年份、類型、封面）,  
**so that** 我新增專輯時可以自動填入這些資訊。

### Acceptance Criteria

1. 擴展現有的 `musicbrainz_service.py` 以從 MusicBrainz API 獲取年份、類型和封面 URL
2. 更新 `search_by_barcode` 方法以返回完整的專輯資訊
3. 處理 MusicBrainz API 回應中可能缺失的欄位（優雅降級）
4. 驗證封面 URL 的有效性（可選：檢查 URL 是否可訪問）
5. 更新現有的 `/api/search/barcode/{barcode}` 端點以返回新資訊
6. 現有的條碼搜尋功能繼續運作

### Integration Verification

IV1: 驗證現有的條碼搜尋端點返回新資訊但不破壞現有整合
IV2: 驗證當 MusicBrainz API 不可用時，系統優雅降級
IV3: 驗證新資訊正確儲存到資料庫

---

## Story 1.3: 實作條碼掃描自動辨識功能

**As a** 使用者,  
**I want** 透過提交條碼自動辨識並新增專輯到我的收藏,  
**so that** 我可以快速批量新增專輯而不需要手動輸入。

### Acceptance Criteria

1. 建立新的 API 端點 `POST /users/{user_id}/albums/scan`
2. 接受條碼作為輸入參數
3. 自動查詢 MusicBrainz 獲取專輯資訊
4. 自動建立專輯記錄並關聯到使用者
5. 處理重複專輯的情況（返回現有專輯或錯誤訊息）
6. 處理 MusicBrainz 找不到專輯的情況（返回適當錯誤）
7. 返回建立的專輯資訊（包含所有新欄位）
8. 提供適當的錯誤處理和日誌記錄

### Integration Verification

IV1: 驗證新端點不影響現有的專輯建立端點
IV2: 驗證重複檢查邏輯與現有邏輯一致
IV3: 驗證新建立的專輯包含完整的資訊（年份、類型、封面等）

---

## Story 1.4: 實作進階搜尋功能

**As a** 使用者,  
**I want** 使用多個條件（藝術家、年份、類型）搜尋我的專輯收藏,  
**so that** 我可以快速找到特定的專輯。

### Acceptance Criteria

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

### Integration Verification

IV1: 驗證現有的標題搜尋功能不受影響
IV2: 驗證新索引不影響寫入效能
IV3: 驗證組合條件搜尋返回正確結果
IV4: 驗證搜尋效能在大量資料下仍然可接受

---

## Story 1.5: 實作圖形辨識功能

**As a** 使用者,  
**I want** 透過上傳專輯封面圖片自動辨識並新增專輯,  
**so that** 我可以使用手機拍照快速新增專輯。

### Acceptance Criteria

1. 選擇並整合圖形辨識服務（例如：Google Vision API 或 AWS Rekognition）
2. 建立新的 API 端點 `POST /users/{user_id}/albums/recognize`
3. 接受圖片上傳（支援常見格式：JPEG, PNG）
4. 呼叫圖形辨識服務識別專輯
5. 使用識別結果查詢 MusicBrainz 或直接建立專輯記錄
6. 處理圖片上傳失敗、辨識失敗等錯誤情況
7. 實作適當的圖片大小和格式驗證
8. 考慮非同步處理（如果辨識時間較長）
9. 提供適當的錯誤處理和使用者回饋

### Integration Verification

IV1: 驗證圖片上傳不影響其他 API 端點的效能
IV2: 驗證辨識失敗時系統優雅降級
IV3: 驗證辨識結果正確轉換為專輯記錄
IV4: 驗證與條碼掃描功能的一致性（相同的專輯建立邏輯）

---

## Story 1.6: 擴展現有 API 回應以包含完整專輯資訊

**As a** 前端開發者,  
**I want** API 回應包含專輯的完整資訊（封面 URL、年份、類型等）,  
**so that** 我可以在前端展示豐富的專輯資訊。

### Acceptance Criteria

1. 更新 `AlbumOut` schema 以包含所有新欄位
2. 更新所有返回專輯資訊的 API 端點：
   - `GET /users/{user_id}/albums` - 列表回應
   - `GET /users/{user_id}/albums/{album_id}` - 單一專輯回應（如果不存在則建立）
   - `POST /users/{user_id}/albums` - 建立回應
   - `PUT /users/{user_id}/albums/{album_id}` - 更新回應
3. 確保所有端點返回一致的資料格式
4. 處理 NULL 值（當專輯沒有某些資訊時）
5. 更新 API 文件（FastAPI 自動生成）

### Integration Verification

IV1: 驗證所有現有 API 端點返回新格式但不破壞現有前端整合
IV2: 驗證資料格式一致性
IV3: 驗證 NULL 值正確處理

---

## Story 1.7: 建立專輯詳細資訊端點

**As a** 前端開發者,  
**I want** 有一個專門的端點獲取專輯的詳細資訊,  
**so that** 我可以在專輯詳情頁面展示完整資訊。

### Acceptance Criteria

1. 建立新的 API 端點 `GET /users/{user_id}/albums/{album_id}/details`
2. 返回專輯的完整資訊，包括：
   - 基本資訊（標題、藝術家、年份、類型、條碼）
   - 封面 URL
   - 可選：從 MusicBrainz 獲取額外資訊（曲目列表等）
3. 處理專輯不存在的情況
4. 驗證使用者權限（只能查看自己的專輯）
5. 提供適當的錯誤處理

### Integration Verification

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

