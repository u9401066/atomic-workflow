# 🏥 麻醉科全流程 — 微顆粒級 SOP

> **目的**：以最細顆粒度記錄麻醉科臨床全流程的每一個動作、決策與分支  
> **顆粒度**：單一實體動作 / 單一判斷點 / 含決策分支路徑  
> **日期**：2026-02-28  
> **狀態**：🔄 建檔中，完成後將逐一 audit AI 介入機會  
> **角色**：🟢 **常規刀（Elective）基線版本** — 其他刀別以此為基礎標注差異  
> **關聯**：高階 AI 機會分析 → `anesthesia-ai-workflow-analysis.md`

### 📁 模組化架構

> 本文件為 **常規刀基線**。各刀別差異流程已模組化拆分至獨立檔案，  
> 共用統一步驟代碼系統（`A-01` ~ `L-08`），可交叉查詢。

| 檔案 | 說明 |
|------|------|
| [模組化總覽 & 步驟代碼索引](anesthesia-workflow/README.md) | 代碼註冊表 + 交叉比對矩陣 |
| [🔴 E刀流程](anesthesia-workflow/emergency.md) | Emergency — 急診手術差異流程 |
| [🟡 U刀流程](anesthesia-workflow/urgent.md) | Urgent — 加急手術差異流程 |
| [🔵 日間手術流程](anesthesia-workflow/day-surgery.md) | Day Surgery — 日間手術差異流程 |

---

## 📋 目錄

| Phase | 名稱 | 顆粒數 |
|:-----:|------|:------:|
| A | [術前門診 / 照會](#phase-a術前門診--照會) | — |
| B | [手術日 — 病房端準備](#phase-b手術日--病房端準備) | — |
| C | [前往開刀房 & 報到](#phase-c前往開刀房--報到) | — |
| D | [等候區 / 進入手術室](#phase-d等候區--進入手術室) | — |
| E | [手術室內 — 病人安頓 & 監測建立](#phase-e手術室內--病人安頓--監測建立) | — |
| F | [麻醉準備 — 機器 / 藥物 / 氣道設備](#phase-f麻醉準備--機器--藥物--氣道設備) | — |
| G | [麻醉誘導](#phase-g麻醉誘導) | — |
| H | [手術擺位 & 手術開始](#phase-h手術擺位--手術開始) | — |
| I | [術中維持](#phase-i術中維持) | — |
| J | [手術結束 & 甦醒](#phase-j手術結束--甦醒) | — |
| K | [PACU 轉送 & 恢復](#phase-kpacu-轉送--恢復) | — |
| L | [術後照護 & 紀錄結案](#phase-l術後照護--紀錄結案) | — |

---

## Phase A：術前門診 / 照會

### A1. 接案 & 病歷調閱

1. **接到麻醉照會單 / 術前門診排定**
   - 住院病人：主治醫師開立麻醉照會
   - 門診手術：手術排程系統自動排入術前門診
   - 急診手術：急診醫師電話 + 系統照會

2. **調閱電子病歷**
   - 登入 HIS / EMR 系統
   - 查看門診紀錄（主訴、診斷、手術計畫）
   - 查看住院紀錄（如有）
   - 查看各科會診紀錄
   - 查看過去麻醉紀錄（如有歷史）

3. **查閱檢驗 / 檢查報告**
   - CBC（Hb / WBC / PLT）
   - BMP / 電解質（Na / K / Cr / BUN / Glucose）
   - 凝血功能（PT / aPTT / INR）
   - 肝功能（AST / ALT / Bil）—— 如有肝臟疾病
   - 甲狀腺功能（TSH / T4）—— 如有甲狀腺病史
   - HbA1c —— 糖尿病病人
   - ECG 12-lead 判讀
   - CXR 判讀
   - 心臟超音波 —— 如有心臟病史 / 高風險手術
   - 肺功能 (PFT) —— 如有肺部疾病 / 胸腔手術
   - 頸椎 X-ray —— 如有頸椎病變疑慮

### A2. 術前評估看診

4. **病人到診 / 床邊評估**
   - 確認病人身份（手環 + 口頭）
   - 自我介紹（麻醉科醫師身份）

5. **病史詢問**
   - 主訴與手術原因
   - 過去病史（系統性回顧）
     - 心血管：HTN / CAD / CHF / Arrhythmia / Valve disease
     - 呼吸：Asthma / COPD / OSA / 最近上呼吸道感染
     - 神經：CVA / Seizure / Myasthenia gravis
     - 內分泌：DM / 甲狀腺 / 腎上腺
     - 肝腎：肝硬化 / CKD / 洗腎
     - 血液：貧血 / 凝血異常 / 抗凝血藥物
   - 過敏史
     - 藥物過敏（哪些藥？什麼反應？）
     - Latex 過敏
     - 食物過敏（與藥物交叉：如蛋白 → Propofol）
     - 碘過敏
   - 前次麻醉經驗
     - 有無 PONV
     - 有無困難插管
     - 有無 Succinylcholine 不良反應
     - 有無 awareness 經驗
     - 有無 MH 家族史
   - 家族麻醉史
     - MH（惡性高熱）
     - 假性膽鹼酯酶缺乏
   - 目前用藥（逐一列出）
     - 抗高血壓藥（ACEi / ARB / BB / CCB）
     - 抗凝血劑（Warfarin / DOAC / 抗血小板）
     - 降血糖藥（Metformin / SU / Insulin / SGLT2i）
     - 精神科用藥（MAOi / SSRI / Benzodiazepine）
     - 心臟用藥（Digoxin / Amiodarone）
     - 中草藥 / 保健食品
   - 物質使用
     - 吸菸（量 / 年 / 是否已戒）
     - 飲酒（量 / 頻率 / 耐受問題）
     - 檳榔
     - 娛樂性藥物

6. **理學檢查 — 氣道評估**
   - Mallampati 分數（I–IV）
     - 張嘴評估（坐姿、不發聲、伸舌）
   - 甲頦距離（Thyromental distance > 6.5 cm）
   - 張口度（Inter-incisor distance > 3 cm）
   - 頸椎活動度（extension / flexion）
   - 下顎前突能力（Upper lip bite test）
   - 頸圍（> 43 cm 男 / > 41 cm 女 → 困難氣道風險）
   - 牙齒狀況
     - 鬆動牙齒（記錄位置）
     - 義齒（全口 / 局部）→ 術前是否需移除
     - Crown / Bridge / Implant（記錄位置，插管避免施力）
     - 缺牙位置
   - 鬍鬚（影響面罩密合）
   - OSA 篩檢
     - STOP-Bang 問卷（≥ 3 分高風險）
     - 是否使用 CPAP

7. **理學檢查 — 心肺 & 其他**
   - 心音聽診（murmur / irregularity）
   - 肺音聽診（wheeze / crackles / 呼吸音對稱性）
   - 周邊水腫
   - JVP
   - 脊椎檢查（如計畫 RA）
     - 背部畸形 / 脊柱側彎
     - 皮膚感染（RA 禁忌）
     - 前次脊椎手術史
   - 靜脈通路評估
     - 上肢靜脈狀況
     - 有無 AV fistula（避免該側）
     - 有無淋巴結清除史（避免該側）
     - 預估 IV 建立難度

8. **風險評估 & 分級**
   - ASA 分級（I–VI）
   - 心臟風險（RCRI / Lee's Index 計算）
   - 功能能力（METs 評估）
     - ≥ 4 METs：可爬兩層樓
     - < 4 METs：高心臟風險
   - 肺部風險（ARISCAT score）
   - VTE 風險（Caprini score）
   - PONV 風險（Apfel score：女性 / 不吸菸 / PONV 史 / 術後 opioid）
   - 衰弱評估（高齡病人）
     - Edmonton Frail Scale 或 Clinical Frailty Scale
   - 營養評估（NRS 2002 或 MNA）

### A3. 麻醉計畫 & 說明

9. **制定麻醉計畫**
   - 麻醉方式選擇
     - GA（氣管插管 / LMA / Mask）
     - RA（Spinal / Epidural / Combined spinal-epidural）
     - Peripheral nerve block（哪條神經 / cathexter?）
     - MAC（monitored anesthesia care）
     - 合併使用（GA + epidural / GA + nerve block）
   - 術中監測等級
     - 標準監測（ECG / NIBP / SpO2 / Temp / ETCO2）
     - 進階監測（A-line / CVC / PA catheter / BIS / IONM / TEE）
   - 預期困難
     - 困難氣道計畫（Plan A / B / C）
     - 大量出血準備（備血量、cell salvage、TXA）
     - 特殊設備需求（雙腔管 / bronchial blocker / FOB）
   - 術後止痛計畫
     - IV PCA（Morphine / Fentanyl）
     - Epidural PCA
     - Nerve block catheter
     - Multimodal analgesia（Acetaminophen / NSAIDs / Ketamine / Lidocaine infusion）

10. **向病人說明**
    - 使用病人能理解的語言
    - 說明麻醉方式與流程
    - 說明風險
      - 常見：PONV、喉嚨痛、暫時性聲音沙啞
      - 罕見但嚴重：牙齒損傷、神經損傷、awareness、MH、嚴重過敏
      - 特定風險（如 RA：頭痛、背痛、極罕見脊髓損傷）
    - 回答病人 / 家屬問題
    - 說明禁食規定
      - 固體食物（含牛奶）：≥ 6 小時
      - 母乳：≥ 4 小時
      - 清澈液體（水、無渣果汁、黑咖啡）：≥ 2 小時
      - 口香糖 / 糖果：視同清澈液體 or 固體（依院規）
    - 說明術前用藥調整
      - 要繼續吃的藥（降壓藥BB等可以吃，少量水送服）
      - 要停的藥（抗凝血劑停藥時程、Metformin 手術當天停）
      - 糖尿病胰島素調整（手術當天減半？不打？依品項）

### A4. 文件簽署

11. **簽署麻醉同意書**
    - 確認病人 / 法定代理人簽名
    - 確認醫師簽名
    - 記錄說明內容及時間

12. **簽署自費同意書（如有自費品項）**
    - 列出自費項目（如 BIS sensor、保溫毯、特殊 ETT 等）
    - 說明費用
    - 確認病人 / 家屬簽名

13. **填寫麻醉術前評估表**
    - 電子或紙本填寫完整
    - 包含以上所有評估結果
    - ASA 分級記錄
    - 麻醉計畫記錄
    - 特殊注意事項記錄

14. **安排額外檢查或會診（如需要）**
    - → 心臟科會診（新發現 murmur / 異常 ECG）
    - → 胸腔科會診（嚴重 COPD / 新發 CXR 異常）
    - → 血液科會診（凝血異常）
    - → 追加檢查（Echo / PFT / Stress test / 頸椎 imaging）
    - → 追加抽血（TSH / HbA1c / BNP 等）
    - 確認報告回覆時間是否來得及手術日

---

## Phase B：手術日 — 病房端準備

### B1. 術前再確認（護理站）

15. **護理師確認手術排程**
    - 查看當日手術排程表
    - 確認手術時間（第幾台）
    - 確認該台手術預估開始時間

16. **確認禁食狀態**
    - 詢問病人最後進食時間
    - 詢問最後喝水時間
    - 記錄於護理紀錄
    - ⚠️ 若未達禁食標準 → 通知手術室 + 麻醉科

17. **確認術前用藥**
    - 核對麻醉評估表的用藥指示
    - 該吃的藥準備好 + 小杯水
    - 該停的藥確認已停
    - 胰島素劑量調整依指示
    - 記錄給藥時間

18. **術前預防性抗生素（如 protocol 在病房給）**
    - 確認醫囑
    - 確認過敏史（Penicillin / Cephalosporin）
    - 給藥（目標：切刀前 60 分鐘內）
    - 記錄給藥時間
    - ⚠️ 有些醫院 protocol 是到 OR 才給

### B2. 病人準備

19. **病人更衣**
    - 換穿手術衣（開口朝後）
    - 內衣褲脫除（依手術部位）
    - 提供保暖被單

20. **移除個人物品**
    - 假牙移除 → 放入標示容器交家屬或護理站保管
    - 眼鏡 / 隱形眼鏡移除
    - 助聽器移除（或保留至 OR，依溝通需要）
    - 首飾移除（戒指 / 項鍊 / 耳環 / 手錶）
      - ⚠️ 無法取下的戒指 → 膠帶包覆 + 記錄
    - 髮夾 / 髮飾移除
    - 活動式假牙 / 牙套移除
    - 指甲油 / 光療移除（影響 SpO2 讀數）
    - 身上金屬物品移除（如使用電燒）

21. **確認手術部位標記**
    - 有側別的手術 → 確認外科醫師已標記（YES 字樣）
    - 確認標記位置與排程一致
    - ⚠️ 標記缺失 → 聯繫外科醫師補標

22. **建立靜脈通路（IV line）— 如病房端需建立**
    - 選擇穿刺部位
      - 避免手術側上肢
      - 避免 AV fistula 側
      - 避免淋巴結清除側
      - 避免已有傷口 / 感染的區域
    - 選擇管針口徑
      - 一般手術：20G 或 22G
      - 預期大出血 / 輸血需求：18G（或更粗）
      - 兒科 / 困難血管：24G
    - 穿刺
      - 消毒 → 止血帶 → 穿刺 → 確認回血 → 固定
      - ⚠️ 失敗 → 換部位重試（最多 2-3 次，之後上報或改 OR 內處理）
    - 連接點滴（LR / NS）
    - 調整流速
    - 記錄管路位置 + 口徑 + 建立時間

23. **辨識手環確認**
    - 核對手環資訊完整（姓名 / 病歷號 / 生日 / 過敏標示）
    - 有過敏 → 紅色過敏手環
    - 跌倒高風險 → 黃色手環（依院規）

24. **備血確認（如需要）**
    - 確認已完成血型(ABO/Rh) + 交叉配血
    - 確認備血單位數（依手術需求）
    - 確認血庫已備妥 / 或需通知血庫
    - ⚠️ 未備血但手術有出血風險 → 緊急通知

### B3. 出發前

25. **病歷資料夾整理**
    - 麻醉同意書 ✓
    - 手術同意書 ✓
    - 自費同意書 ✓（如有）
    - 麻醉術前評估表 ✓
    - 護理交接紀錄 ✓
    - 最新檢驗報告 ✓
    - 影像報告（如適用）✓
    - 備血記錄（如適用）✓

26. **通知開刀房**
    - 電話 / 系統通知：「XX 床病人 ready」
    - 確認傳送人員已排定

27. **搬運前最後確認**
    - 病人姓名 vs 排程
    - 手術部位標記 in place
    - IV 通暢
    - 禁食確認
    - 所有文件已備齊
    - 個人物品已處理

28. **等待傳送人員**
    - 傳送人員抵達
    - 護理師 + 傳送人員共同確認病人身份
    - 交接病歷資料夾

---

## Phase C：前往開刀房 & 報到

### C1. 轉送至開刀房

29. **從病房出發**
    - 推床 / 輪椅（依病人行動能力）
    - 確認點滴架固定
    - 確認引流管/導尿管固定（如有）
    - 被單覆蓋保暖 + 維護隱私

30. **移動路線**
    - 搭乘專用電梯至手術樓層
    - 行經走廊到開刀房管制區入口
    - ⚠️ 轉送中觀察病人狀態（意識、呼吸、IV 通暢）

### C2. 開刀房前台報到

31. **抵達前台（Reception）**
    - 傳送人員將推床停靠前台窗口
    - 告知前台人員：「XX 病人報到」

32. **前台核對身份**
    - 前台人員掃描手環條碼 或 人工查閱
    - 核對排程系統：姓名 + 病歷號 + 預定手術名稱 + 刀房號
    - 口頭詢問病人：「請問您的名字？生日？」

33. **核對生理參數**
    - 查看病房端最後一套生命徵象（BP / HR / RR / SpO2 / Temp）+ 現場再次測量
    - 現場再次確認NPO時間
    - 現場再次確認有沒有抽菸喝酒嚼檳榔
    - 確認有無使用氧氣>>檢查氧氣儲量是否需要盡快進入開刀房
    - 記錄於開刀房報到表
    - ⚠️ 異常值（例如 SBP > 180, HR > 120, SpO2 < 92, 發燒 > 38°C）
      - → 通知麻醉醫師評估
      - → 麻醉醫師決定：可繼續 / 需先處理 / 需延後手術

34. **核對病歷表單 — 逐一清點**
    - 麻醉照會單 / 術前評估表 → ✓ 已填寫完整
    - 麻醉同意書 → ✓ 已簽署（病人 + 醫師）
    - 手術同意書 → ✓ 已簽署
    - 自費同意書 → ✓ 已簽署（如有自費品項）
    - 護理交接紀錄 → ✓ 已填寫
    - 術前檢查報告 → ✓ 已附上
    - 備血記錄 → ✓（如需要）
    - ⚠️ 文件缺漏 → 聯繫病房補件 → 暫不進入刀房

35. **前台系統登錄**
    - 系統登記病人「已報到」
    - 記錄報到時間
    - 更新刀房狀態看板

36. **判斷去向**
    - 🅰️ **到等候區（Holding Area）** —— 若：
      - 該刀房前一台手術尚未結束
      - 麻醉 / 外科團隊尚未就位
      - 需先在等候區做進一步評估
    - 🅱️ **直接進入指定刀房** —— 若：
      - 刀房已清潔 / 備妥
      - 團隊已就位
      - 是該刀房第一台

---

## Phase D：等候區 / 進入手術室

### D1. 等候區流程（如走 🅰️ 路線）

37. **推入等候區**
    - 移至指定等候位
    - 煞車固定推床
    - 確認病人舒適

38. **等候區護理師接手**
    - 傳送人員交接 → 等候區護理師
    - 交接：病歷資料 + 口頭交班（病人姓名、手術名稱、特殊注意）

39. **等候區再確認**
    - 身份核對（手環 + 口頭）
    - 禁食狀態再確認
    - 過敏狀態再確認
    - 手術部位標記再確認

40. **等候區麻醉訪視（如術前門診未做 / 住院急排）**
    - 麻醉醫師到等候區看診
    - 重複 Phase A 的評估流程（簡化版）
    - 確認 / 修訂麻醉計畫
    - 補簽同意書（如尚未簽）

41. **等候區 IV 建立（如病房端未建）**
    - 同 Step 22 流程

42. **等候區前置用藥（如需要）**
    - Midazolam IV（焦慮嚴重的病人）
    - 制酸劑（Citric acid / Ranitidine）—— 全胃風險病人
    - 止吐藥（Granisetron / Dexamethasone）—— 高 PONV 風險
    - Glycopyrrolate（減少口腔分泌物）—— 兒科 / 纖維支氣管鏡

43. **等待 OR 通知**
    - 等候區護理師接到通知：「XX 號刀房 ready」
    - 確認病人狀態允許轉入

### D2. 進入手術室

44. **推病人至指定刀房門口**
    - 核對刀房號碼 vs 排程
    - ⚠️ 推錯刀房 → 嚴重安全事件

45. **刀房門口再確認**
    - 流動護理師 + 推床人員 + 病人三方核對
    - 姓名 + 手術名稱 + 手術部位
    - 確認無誤 → 推入刀房

---

## Phase E：手術室內 — 病人安頓 & 監測建立

### E1. 病人安頓

46. **推床進入刀房**
    - 推床推至手術台旁
    - 煞車固定推床

47. **移位決策**
    - 🅰️ **立即移到手術台** —— 一般情況
    - 🅱️ **暫留推床上** —— 若需先建立 RA（如 spinal）再移位
    - 決定取決於麻醉方式 + 外科醫師偏好

48. **移到手術台（如走 🅰️）**
    - 手術台高度調整 → 與推床同高
    - 手術台煞車確認鎖定
    - 使用滑板（transfer board）或直接搬移
    - 指導清醒病人配合：「請慢慢移過來」
    - 或由團隊搬移（麻醉 + 護理 + 助手）
    - ⚠️ 注意事項
      - 管路不被拉扯（IV / Foley / drain）
      - 防止病人跌落
      - 頸椎損傷病人：固定頸圈 + 對齊搬移

49. **手術台上固定**
    - 安全帶跨膝上方固定（不過緊）
    - 確認手臂位置
      - 手臂外展板固定（angle < 90°，避免 brachial plexus 損傷）
      - 或手臂收靠身體（tucked）
    - ⚠️ 有 AV fistula / 淋巴結清除側 → 不放 BP cuff、不放 IV

50. **確認病人舒適**
    - 詢問病人是否有不適
    - 頭枕位置調整
    - 被單保暖 + 隱私

### E2. 標準監測建立

51. **貼心電圖電極（ECG leads）**
    - 3-lead ECG：RA（右鎖骨下）、LA（左鎖骨下）、LL（左下腹/左髖）
    - 或 5-lead ECG：加 V₁（第四肋間胸骨右緣）+ RL（右下腹）
    - 確認貼片位置正確
    - 確認皮膚乾燥（汗多 → 擦乾 → 用酒精擦拭 → 再貼）
    - 確認男性胸毛 → 必要時剃除避免貼不住
    - 接上 ECG 導線（顏色/位置對應）
    - 開啟 monitor 確認 ECG 波形正常
      - ⚠️ 雜訊太多 → 重新貼 / 調整位置
      - ⚠️ 波形異常 → 確認是否真的心律不整 → 通報麻醉醫師

52. **裝血壓帶（NIBP cuff）**
    - **選擇合適 size**
      - 目測或量測上臂周徑
      - 小號 (S)：周徑 17–22 cm
      - 中號 (M)：周徑 22–32 cm
      - 大號 (L)：周徑 32–42 cm
      - 大腿用 (Thigh)：特殊需求
    - **如果 size 不合**
      - 先找本間開刀房的備品架/抽屜
      - → 沒有 → 去隔壁開刀房借
      - → 還是沒有 → 去庫房（supply room）拿
      - → 庫房也沒有 → 通知護理長調貨
    - **裝設位置**
      - 一般：非手術側上臂
      - ⚠️ 禁忌同側：AV fistula / 淋巴結清除 / IV 同側
      - 替代位置：前臂 / 小腿（特殊情況記錄 + 可能有誤差）
    - 對齊動脈標記（cuff 上的「ARTERY」指示線對準肱動脈）
    - 接上 NIBP 管線到 monitor
    - **測試一次**
      - 按 NIBP 按鈕 → 充氣 → 讀取數值
      - ⚠️ 錯誤/無法量測 → 確認 cuff 鬆緊 / size / 管線連接

53. **夾 SpO2 探頭（Pulse Oximeter）**
    - 選擇部位
      - 首選：非手術側手指（食指 / 中指）
      - 替代：腳趾 / 耳垂 / 前額反射式（新生兒/小兒/末梢循環差）
    - 指甲油/光療已移除（Step 20 確認）
    - ⚠️ 波形不好
      - 末梢冰冷 → 搓揉手指 / 暖手 / 換耳垂
      - 周邊循環差 → 改用前額反射式 sensor
      - 電燒干擾 → 距電燒遠的肢體
    - 確認 SpO2 波形 + 數值顯示正常

54. **拆封自費品項**
    - 查閱自費同意書 → 確認品項清單
    - 逐一拆封
      - BIS sensor（腦電圖監測）
      - 自費保溫毯（Bair Hugger 等品牌）
      - 自費溫度探頭
      - 特殊 IV catheter / 特殊 ETT
      - 其他自費耗材
    - **記錄**
      - 品項名稱
      - 批號 / 序號 / 有效期限
      - 記錄於自費品項使用紀錄表
    - 核對：拆封品項 vs 同意書品項 → 一致
    - ⚠️ 品項不足 / 備品有誤 → 通知護理師調貨

55. **貼 BIS sensor（如使用）**
    - 擦拭前額皮膚（酒精棉片去油脂）
    - 依包裝指示貼合位置（前額 + 太陽穴）
    - 接上 BIS module cable
    - 開啟 → 確認 SQI（Signal Quality Index）> 80
    - ⚠️ SQI 低 → 重新貼 / 確認接觸 / 皮膚再清潔

56. **裝保溫毯**
    - 選擇保溫毯類型
      - 上半身型（上肢 + 胸部覆蓋）
      - 下半身型（下肢覆蓋）
      - 全身型
      - 選擇取決於手術部位暴露範圍
    - 連接保溫毯機器（Forced Air Warmer）
      - 插電 → 開機
      - 接上保溫毯管線
      - 設定目標溫度（通常 38°C / High setting）
      - 確認送風正常（手感暖風從毯子出來）
    - ⚠️ 機器故障 → 換一台 / 從隔壁刀房借 / 通知工程

57. **裝溫度探頭（Temp probe）**
    - **GA 病人**（誘導後放置）
      - 鼻咽溫度探頭（最常用，GA 插管後置入）
      - 食道溫度探頭（食道聽診器含溫度探頭）
      - 直腸溫度探頭（某些情境）
    - **RA / MAC 病人**
      - 腋窩溫度探頭
      - 皮膚溫度貼片
      - 紅外線耳溫
    - 接上 monitor → 確認讀數合理

58. **裝 NMT sensor（肌鬆監測，如計畫使用）**
    - TOF-Watch / TOF-Cuff
    - 貼電極於 ulnar nerve 路徑
    - 校正基線（誘導前做 calibration）
    - 或規劃誘導後才校正

### E3. 進階監測建立（如需要）

59. **建立 Arterial line（A-line）— 如計畫侵入性血壓監測**
    - 選擇部位
      - 首選：非慣用手橈動脈（radial artery）
      - 替代：尺動脈、肱動脈、股動脈、足背動脈
    - Allen's test（如穿刺橈動脈）確認尺動脈灌流
    - 消毒 + 鋪巾
    - 局部麻醉（清醒病人）
    - 穿刺
      - 直接穿刺法 或 超音波引導
      - 確認動脈血回流
      - 導入 catheter
    - 連接 transducer + 沖洗管路（heparinized saline）
    - Zeroing（歸零校正）—— transducer 對齊 phlebostatic axis
    - 確認動脈波形正常
    - 固定 + 記錄

60. **建立 CVC（Central Venous Catheter）— 如需要**
    - 選擇部位
      - 首選：右頸內靜脈（R-IJV）
      - 替代：鎖骨下靜脈、股靜脈、左 IJV
    - 超音波確認血管位置 + 大小 + 通暢
    - 消毒 + 鋪巾（最大無菌屏障）
    - 局部麻醉（清醒病人）
    - 超音波引導穿刺（Seldinger technique）
    - 導入 guide wire → 確認位置（超音波看到 wire 在血管內）
    - 擴張 → 導入 catheter
    - 固定 + 縫合
    - 沖洗各 port
    - 確認回血
    - 接上 CVP transducer（如需要）+ zeroing
    - ⚠️ 術後需 CXR 確認位置 + 排除氣胸

---

## Phase F：麻醉準備 — 機器 / 藥物 / 氣道設備

### F1. 麻醉機檢查

61. **麻醉機開機自檢**
    - 開啟電源
    - 等待自檢程序完成（各品牌不同：Dräger / GE / Mindray）
    - 確認自檢通過（綠燈 / OK 顯示）
    - ⚠️ 自檢失敗 → 不可使用 → 通知生物醫學工程 → 換機器

62. **氣體供應確認**
    - 中央氣體供應連接確認
      - O2 管線（綠色）接頭密合
      - N2O 管線（藍色）接頭密合
      - Air 管線（黃色）接頭密合
    - 備用 O2 鋼瓶
      - 確認有裝
      - 確認壓力足夠（> 1000 psi / > 70 bar）
      - ⚠️ 低壓 → 更換鋼瓶

63. **呼吸迴路連接 & 漏氣測試**
    - 組裝呼吸迴路（吸氣管 + 呼氣管 + Y-piece）
    - 接上 CO2 absorbent canister
      - 確認鈉石灰顏色（未變色 = 堪用）
      - ⚠️ 已變色（紫色/灰色）→ 更換
    - 封閉 Y-piece → 執行 leak test
      - 系統自動加壓 → 確認漏氣率在允許範圍
    - 接上 HME filter（Heat Moisture Exchanger）
    - 確認 APL valve 功能正常

64. **揮發器（Vaporizer）確認**
    - 確認揮發器安裝正確
    - 檢查液面（Sevoflurane / Desflurane / Isoflurane）
      - ⚠️ 液面低 → 補充
    - 確認揮發器 lock 正確
    - Desflurane 加熱型揮發器：確認已加熱完成

65. **抽吸系統確認**
    - 牆壁抽吸連接（或可攜式抽吸機）
    - 接上抽吸管（Yankauer）
    - 測試抽吸力（手封住管口 → 壓力顯示正常 / 聽到抽吸音）
    - 確認收集瓶安裝正確

66. **備用甦醒球（Self-inflating bag / Ambu bag）**
    - 確認在手邊可及處
    - 確認功能良好（擠壓 → 感覺到 valve 出氣）
    - 接上 O2 管線（可接中央或鋼瓶）

### F2. 藥物準備

67. **抽取誘導藥物**
    - **Propofol**
      - 20ml 注射器
      - 記錄濃度（10 mg/ml）
      - 標籤：藥名 + 濃度 + 日期 + 時間 + 抽藥者姓名
    - **Fentanyl**
      - 注射器（通常 3–5 ml）
      - 記錄濃度（50 μg/ml）
      - 標籤
    - **Rocuronium**（或 Cisatracurium / Succinylcholine）
      - 注射器
      - 記錄濃度
      - 標籤
    - **Lidocaine**（optional，降低 Propofol 注射痛 / 降低插管反應）
      - 注射器
      - 記錄濃度（20 mg/ml）
      - 標籤
    - ⚠️ 所有注射器必須貼標籤（顏色依 ISMP/ASA 顏色規範）
    - ⚠️ 管制藥物（Fentanyl 等）需從管制藥櫃領取 + 簽名 + 記錄

68. **準備急救藥物**
    - **Atropine** 0.5 mg/ml — 注射器抽好或安瓶備妥
    - **Ephedrine** — 稀釋至 5 mg/ml（通常 1ml Ephedrine 50mg + 9ml NS）
    - **Phenylephrine** — 稀釋至 100 μg/ml（通常 1ml PE 10mg + 99ml NS 配成 bag）
    - **Epinephrine** — 1:10,000 稀釋（1mg/10ml）安瓶或預充式備
    - ⚠️ 急救藥物放置位置統一 + 隨手可取

69. **準備持續輸注藥物（如計畫使用）**
    - Remifentanil infusion（稀釋 + 輸注幫浦設定）
    - Propofol infusion（TIVA 情境）
    - Dexmedetomidine infusion
    - Ketamine infusion（低劑量止痛）
    - Insulin infusion（DM 病人）
    - ⚠️ 所有 infusion line 標籤 + 輸注幫浦程式確認

70. **準備止吐藥（如高 PONV 風險）**
    - Ondansetron / Granisetron
    - Dexamethasone（誘導時給）
    - Droperidol（低劑量）

71. **準備特殊藥物（如需要）**
    - Dantrolene 位置確認（MH cart 位置）
    - Sugammadex（肌鬆逆轉）
    - Intralipid 20%（LAST 急救）
    - Nitroglycerin / Esmolol / Labetalol（心血管手術）
    - TXA（Tranexamic acid，大出血風險）

72. **輸液準備**
    - 選擇晶體液（LR / NS / Plasmalyte）
    - 掛上點滴 + 排氣（確認無氣泡）
    - 接上 IV extension + 3-way stopcock（三通閥）
    - 輸液加溫器設定（Level 1 / Ranger 等，如預期大量輸液/輸血）
    - 加壓袋準備（如需要快速輸液）

### F3. 氣道設備準備

73. **喉鏡準備**
    - 直視喉鏡
      - 選擇 blade（Macintosh #3 或 #4 / Miller #2）
      - 確認燈泡亮（或 LED 光源正常）
    - Video 喉鏡（如 GlideScope / McGrath / C-MAC）
      - 開機 → 確認螢幕顯示
      - 選擇 blade size
      - 備用直視喉鏡在旁

74. **氣管內管（ETT）準備**
    - 選擇 size
      - 成人女性：6.5–7.0 mm ID
      - 成人男性：7.0–8.0 mm ID
      - 兒科：(Age/4) + 4（uncuffed）或 (Age/4) + 3.5（cuffed）
    - 備用小一號 ETT
    - Stylet 潤滑 → 插入 ETT → 彎曲成 hockey stick 形狀
    - Cuff 充氣測試 → 確認無漏 → 放氣
    - 潤滑 ETT 前端（水溶性潤滑劑）

75. **備用氣道設備**
    - Oral airway（Guedel）— 選擇 size
    - Nasal airway — 選擇 size（如需要）
    - LMA（Laryngeal Mask Airway）/ i-gel — 選 size + cuff 測試
    - Bougie（Introducer）— 備在手邊
    - 困難氣道車位置確認（如高風險病人）
      - Fiberoptic bronchoscope
      - Video stylet
      - Retrograde intubation kit
      - 外科氣道工具（Cricothyrotomy kit）

76. **抽吸管接上**
    - Yankauer suction tip
    - 接上抽吸管線
    - 測試抽吸功能
    - 放置於麻醉醫師右手可及處

77. **面罩（Face Mask）準備**
    - 選擇合適 size（蓋住口鼻無漏氣）
    - 成人：size 4 或 5
    - 小兒：size 1–3
    - 連接呼吸迴路 Y-piece

---

## Phase G：麻醉誘導

### G1. WHO Sign-In（手術安全查核 — 第一部分）

78. **Sign-In 啟動**
    - 麻醉醫師主導
    - 在場人員：麻醉醫師 + 護理師（至少）
    - 確認以下項目（口頭逐一確認）：

79. **病人確認**
    - 姓名（口頭 + 手環）
    - 病歷號
    - 手術名稱 + 部位 + 側別

80. **同意書確認**
    - 麻醉同意書 → 已簽署 ✓
    - 手術同意書 → 已簽署 ✓

81. **手術部位標記確認**
    - 有側別 → 標記存在 ✓
    - 無側別 → N/A

82. **麻醉安全確認**
    - 麻醉機 + 監測設備已查檢 ✓
    - 困難氣道風險？→ YES / NO
      - YES → 確認設備準備（Plan A/B/C）
    - 吸入風險（Full stomach）？→ YES / NO
      - YES → RSI 準備確認
    - 大量失血風險（> 500ml）？→ YES / NO
      - YES → 備血確認（已 crossmatch + 血庫備妥）
    - 過敏？→ 列出過敏藥物

83. **脈搏血氧儀確認運作中 ✓**

### G2. 預氧合（Pre-oxygenation）

84. **面罩密合放置**
    - 左手 C-E grip 固定面罩
    - 確認密合（無漏氣）
    - ⚠️ 有鬍鬚 → 面罩邊緣塗凡士林 / 用濕紗布填充
    - ⚠️ 無牙 → 義齒暫時留置幫助密合（誘導後再取出）/ 塞紗布填充臉頰

85. **設定 O2 流量**
    - Fresh Gas Flow 開至 100% O2
    - 流量 8–10 L/min（或 flush）

86. **執行預氧合**
    - 標準：3–5 分鐘正常呼吸 或 8 次 vital capacity breaths
    - 監測 EtO2（end-tidal O2）
      - 目標：EtO2 > 90%（理想 > 0.87）
    - ⚠️ 特殊族群
      - 小兒：預氧合時間較短（FRC/BW 比小，desaturation 快）
      - 肥胖：頭高位（25–30° head-up / beach chair）
      - 孕婦：FRC ↓ → 快速 desaturation → 充分預氧合更重要
      - 急診 RSI：可能時間不足 → HFNC 15 L/min 同時預氧合

87. **預氧合完成確認**
    - EtO2 > 90% ✓
    - SpO2 100% ✓
    - 通知團隊：「預氧合完成，準備 induction」

### G3. 全身麻醉誘導（GA Induction）

88. **點滴確認通暢**
    - 快速 flush 確認 IV 通暢
    - 無外滲 / 腫脹

89. **給予 Fentanyl（或其他 opioid）**
    - 劑量：1–2 μg/kg IV
    - 緩慢推注（30–60 秒）
    - 觀察：呼吸頻率可能下降 → 正常反應

90. **等待 Fentanyl 作用（1–2 分鐘）**
    - 持續監測 SpO2 / HR / BP
    - 持續面罩 O2

91. **給予 Lidocaine（optional）**
    - 劑量：1–1.5 mg/kg IV
    - 用途：降低 Propofol 注射痛 / 抑制插管心血管反應

92. **給予 Propofol（或其他誘導劑）**
    - 劑量：1.5–2.5 mg/kg IV
    - 調整劑量依病人狀況：
      - 老人 / ASA III-IV：減量（1–1.5 mg/kg）
      - 肥胖：用 LBW 或 adjusted BW 計算
      - 小兒：可能需較高劑量（2.5–3.5 mg/kg）
      - 血行動力學不穩：改用 Etomidate（0.2–0.3 mg/kg）或 Ketamine（1–2 mg/kg）
    - 推注速度：依 BP 反應調整
    - ⚠️ 注射痛 → 先走 Lidocaine / 混合 Lidocaine / 大靜脈注射

93. **確認意識喪失**
    - 呼喚病人姓名 → 無反應
    - 睫毛反射消失
    - 下顎鬆弛

94. **開始面罩通氣**
    - 一手 C-E grip 面罩
    - 另一手擠壓呼吸袋 / 開 APV
    - 評估面罩通氣品質
      - 看胸廓起伏 ✓
      - 聽呼吸音 ✓
      - 看 ETCO2 波形出現 ✓
      - 看呼吸袋順從性
    - ⚠️ **面罩通氣困難**
      - 雙手固定面罩（需助手擠袋）
      - 插入 oral airway
      - 插入 nasal airway
      - 調整頭位（chin lift / jaw thrust）
      - ⚠️ 完全無法通氣 → 進入困難氣道流程

95. **給予肌鬆劑**
    - **Rocuronium**：0.6 mg/kg（標準）或 1.2 mg/kg（RSI）
    - 或 **Succinylcholine**：1–1.5 mg/kg（RSI / 極短手術 / 需快速肌鬆）
      - ⚠️ Succinylcholine 禁忌：高血鉀風險（燒傷/脊髓損傷/MH/肌病變）
    - 或 **Cisatracurium**：0.1–0.2 mg/kg（肝腎不佳選擇）
    - 記錄給藥時間

96. **等待肌鬆作用**
    - Rocuronium：60–90 秒
    - Succinylcholine：45–60 秒
    - 持續面罩通氣
    - TOF 監測（如已建立）→ TOF = 0 確認完全肌鬆
    - ⚥ 此時持續注意 BP / HR 變化 → 低血壓嚴重 → 給 Ephedrine / Phenylephrine

### G4. 氣道處理 — 氣管插管

97. **停止面罩通氣**
    - 移開面罩

98. **喉鏡插入**
    - 左手持喉鏡
    - 右手打開病人口腔（scissor technique）
    - Blade 從右嘴角進入
    - 沿舌面推進至 vallecula（Macintosh）或 epiglottis 後方（Miller）
    - 向前上方提起（lifting，非撬動）

99. **聲門暴露**
    - 評估 Cormack-Lehane grade（I / II / III / IV）
    - Grade III/IV → 採取輔助措施
      - BURP maneuver（由助手執行）
      - 換 Video 喉鏡
      - 換 Blade size
      - Bougie 輔助

100. **插入 ETT**
     - 右手持 ETT
     - 看到聲帶 → ETT 通過聲帶
     - 插入深度
       - 成人女性：門齒深度 21 cm
       - 成人男性：門齒深度 23 cm
       - 兒科：(Age/2) + 12（口腔）
     - 拔出 stylet
     - Cuff 充氣
       - 聽到漏氣聲消失即可（或 cuff 壓力計 < 25 cmH2O）

101. **確認管位 — 5 步驟**
     - ① ETCO2 波形出現（最重要的確認方法）
       - 連續 5–6 個正常 CO2 波形 ✓
     - ② 雙側胸廓對稱起伏 ✓
     - ③ 雙側肺尖聽診呼吸音 ✓
     - ④ 雙側肺底聽診呼吸音 ✓
     - ⑤ 上腹部聽診無氣過水聲 ✓（排除食道插管）
     - SpO2 維持 ✓

102. **固定 ETT**
     - 使用膠帶 / 固定器固定於臉頰
     - 記錄門齒深度
     - 確認固定後管子不會移動

103. **接上呼吸器**
     - 呼吸迴路 Y-piece 接到 ETT
     - 切換至機械通氣模式

### G5. 呼吸器初始設定

104. **設定通氣模式**
     - Volume Control（最常用）或 Pressure Control
     - 設定參數：
       - Tidal Volume (Vt)：6–8 ml/kg（用 IBW 計算）
         - IBW 男：50 + 0.91 × (身高cm - 152.4)
         - IBW 女：45.5 + 0.91 × (身高cm - 152.4)
       - Respiratory Rate (RR)：10–14 /min（維持 ETCO2 35–45 mmHg）
       - PEEP：5 cmH2O（標準起始）
       - FiO2：調整（先 50%–100%，穩定後依 SpO2 下調）
       - I:E ratio：1:2（標準）
     - ⚠️ 特殊設定
       - COPD：延長呼氣比（1:3 或 1:4）
       - 肥胖：較高 PEEP（8–10）+ 可能需較高 Vt
       - 單肺通氣：見 Phase I 特殊情境

105. **確認呼吸力學**
     - Peak Inspiratory Pressure (PIP)：< 30 cmH2O 可接受
     - Plateau Pressure (Pplat)：< 30 cmH2O（肺保護）
     - Compliance 計算可接受
     - ⚠️ PIP 過高 → 確認管路無扭折 / 支氣管痙攣 / 單側插管

106. **開始吸入麻醉藥（如選擇 inhalation maintenance）**
     - Sevoflurane / Desflurane / Isoflurane
     - 設定濃度（通常 1–1.5 MAC，依年齡調整）
     - 確認 FiO2 + N2O 比例（如使用 N2O）
     - 確認揮發器輸出 + 回路濃度顯示

107. **或 TIVA 設定（如選擇全靜脈麻醉）**
     - Propofol TCI（Target-Controlled Infusion）
       - 設定 Marsh 或 Schnider model
       - 目標濃度（Ce 3–5 μg/ml）
     - Remifentanil TCI
       - 設定 Minto model
       - 目標濃度（Ce 2–5 ng/ml）
     - 或手動 infusion rate 設定
     - BIS 目標 40–60

### G6. 區域麻醉（如選擇 RA 而非 GA）

108. **Spinal Anesthesia（脊椎麻醉）**
     - 病人擺位
       - 側臥位（affected side down 或 up，依 baricity）
       - 或坐姿（背部弓起「蝦米姿勢」）
     - 確認監測設備運作中
     - 消毒背部
       - Chlorhexidine 或 Betadine，由中心向外擴大
     - 鋪無菌巾
     - 觸摸定位
       - Iliac crest（相當於 L4 棘突或 L3-4 間隙）
       - 穿刺點：L3-4 或 L4-5
     - 局部麻醉皮膚（Lidocaine 1% 皮下注射）
     - 插入 Spinal needle（25G Whitacre pencil-point）
       - 正中或旁正中進路
       - 感覺突破韌帶層次
       - 回抽見 CSF（清澈液體）
     - 慢速注入藥物
       - Heavy Bupivacaine 0.5%（hyperbaric）10–15 mg
       - ± Fentanyl 10–25 μg intrathecal
     - 拔出 needle
     - 病人回復仰臥位
     - 紀錄穿刺時間 + 藥物 + 劑量
     - 測試阻滯高度 — 每 2–3 分鐘
       - Pin-prick test 或 cold sensation（酒精棉）
       - 目標高度取決於手術類型（例如 C-section → T4 / 下肢手術 → T10）
     - 等待阻滯穩定（約 10–15 分鐘）
     - 持續監測 BP（spinal → 交感阻斷 → 低血壓）
       - ⚠️ 低血壓 → Ephedrine / Phenylephrine / 加速輸液

109. **Epidural Anesthesia（硬膜外麻醉）**
     - 擺位（同 spinal）
     - 消毒 + 鋪巾
     - 局部麻醉
     - Touhy needle（17G / 18G）進針
       - Loss of Resistance（LOR）technique
       - LOR to saline 或 air
       - 突破黃韌帶 → 進入硬膜外腔
     - 穿入 epidural catheter
       - 留置 catheter 進入硬膜外腔 3–5 cm
       - 回抽確認無血 / 無 CSF
     - **Test dose**
       - Lidocaine 1.5% + Epinephrine 1:200,000（3 ml）
       - 觀察 3 min
         - ⚠️ HR 上升 > 20% → 懷疑 IV catheter
         - ⚠️ 快速運動阻滯 → 懷疑 intrathecal catheter
     - 分次給藥（loading dose）
       - Bupivacaine 0.25–0.5% 或 Ropivacaine 0.5–0.75%
       - 每次 3–5 ml，間隔 3–5 min
       - ± Fentanyl epidural（1–2 μg/ml）
     - 固定 catheter（膠帶固定於背部）
     - 記錄 catheter depth（皮膚處刻度）
     - 測試阻滯高度

110. **Peripheral Nerve Block（周邊神經阻斷）**
     - 選擇阻斷類型（依手術部位）
       - 上肢：Interscalene / Supraclavicular / Infraclavicular / Axillary
       - 下肢：Femoral / Adductor canal / Sciatic / Popliteal / Ankle
       - 軀幹：TAP / PVB / ESP / Rectus sheath
     - 擺位 + 消毒 + 無菌技術
     - 超音波引導
       - 線性探頭（高頻 6–15 MHz）
       - 找到目標神經 + 周圍結構
       - In-plane 或 Out-of-plane approach
     - 局部皮膚麻醉
     - 穿刺
       - 在超音波引導下進針
       - 確認針尖位置
       - 回抽（確認無血液）
       - 注入少量 LA → 看到擴散（hydrodissection）
       - 分次注入藥物
         - Ropivacaine 0.25–0.5% 或 Bupivacaine 0.25–0.5%
         - 總量依 block 類型 + 體重計算最大安全劑量
     - ⚠️ 局麻藥物中毒（LAST）徵兆監測
       - 耳鳴 / 金屬味 / 頭暈 / 抽搐 / 心律不整
       - → Intralipid 20% rescue protocol

### G7. MAC（Monitored Anesthesia Care）

111. **MAC 設定**
     - 標準監測建立（同 E2）
     - 鼻導管 O2 供應
       - 2–4 L/min nasal cannula
       - 或高流量面罩
     - 鎮靜藥物
       - Midazolam 1–2 mg IV titrate
       - ± Fentanyl 25–50 μg IV
       - ± Propofol infusion 25–75 μg/kg/min
       - 或 Dexmedetomidine infusion 0.2–1 μg/kg/hr
     - 局部麻醉（外科醫師執行 or 麻醉醫師注射）
     - 持續監測呼吸（ETCO2 via nasal cannula，SpO2）
     - ⚠️ 隨時準備轉換為 GA（conversion to GA）

---

## Phase H：手術擺位 & 手術開始

### H1. 手術擺位

112. **誘導後擺位（如需要改變位置）**
     - 仰臥位（Supine）— 大部分手術預設
     - 截石位（Lithotomy）— 婦科/泌尿科
       - 腿架安裝 + 調整
       - ⚠️ 腓總神經壓迫風險（腿架 vs 膝部墊）
       - ⚠️ 下肢區室症候群風險（手術時間 > 4 hr）
     - 側臥位（Lateral decubitus）— 胸腔/腎臟手術
       - 腋下墊卷（保護腋窩血管神經）
       - 耳朵保護墊
       - 下側手臂保護
     - 俯臥位（Prone）— 脊椎手術
       - ⚠️ 拔管後翻身 or 帶管翻身 → 依計畫
       - Jackson table / Wilson frame 安裝
       - 胸墊 / 骻墊位置
       - 頭部固定（Mayfield / 面朝下 + 額墊）
       - ⚠️ 眼睛保護（無壓迫 → 失明風險）
       - ⚠️ 管路不被壓迫（ETT / IV / A-line / CVC）
       - ⚠️ 腹部懸空（避免腹壓升高 → 出血增加）
     - 坐姿（Sitting / Beach chair）— 肩關節/後顱窩
       - ⚠️ 空氣栓塞風險 → precordial Doppler / TEE
       - ⚠️ 腦灌注壓力降低 → BP 修正
     - Trendelenburg / Reverse Trendelenburg
     - 頭轉一側（ENT / Carotid 手術）

113. **擺位後確認**
     - 所有壓力點有墊保護
     - 手臂外展 < 90°（避免 brachial plexus）
     - 手指不在桌縫處（鉸鏈壓傷）
     - 眼睛保護
       - 閉眼 + 眼貼
       - 俯臥位 → 確認眼球無壓迫
       - 塗防護眼藥膏（Lacrilube）
     - 頭頸位置中立 or 依手術需要
     - 生殖器 / 乳房無壓迫
     - ⚠️ 特殊裝備
       - Sequential Compression Device (SCD) → DVT 預防
       - 開啟 SCD 機器

114. **擺位後重新確認監測**
     - ECG 波形仍正常
     - NIBP 重新量測（位置改變可能影響）
     - SpO2 仍有訊號
     - A-line 波形 + zeroing（如侵入性 BP）
     - ETT 深度重新確認（尤其翻身後）
       - 重新聽診雙側呼吸音
       - ⚠️ 翻身後 ETT 可能位移 → 單側插管
     - ETCO2 波形正常

### H2. Time-Out（WHO 第二部分）

115. **Time-Out 啟動**
     - 所有團隊成員暫停手上動作
     - 主持：流動護理師或麻醉醫師（依院規）
     - 全程口頭確認 + 所有人參與

116. **Time-Out 內容**
     - □ 團隊成員自我介紹（姓名 + 角色）
     - □ 病人姓名 + 病歷號
     - □ 手術名稱 + 部位 + 側別
     - □ 預期手術時間
     - □ 預期失血量
     - □ 抗生素已給予（或確認已開始計時）
       - ⚠️ 切刀前 60 min 內需完成
       - ⚠️ Vancomycin 需 1–2 hr 輸注 → 更早開始
     - □ 病人過敏
     - □ 影像是否已 display
     - □ 麻醉特殊注意事項（困難氣道/血行動力學/大量輸血準備）
     - □ 外科特殊注意事項
     - □ 護理特殊注意事項（特殊器械/植入物）
     - □ VTE 預防措施確認

117. **Time-Out 完成確認**
     - 所有人員確認 → 「Proceed」
     - ⚠️ 任何人有疑慮 → 暫停 → 釐清後再繼續

118. **手術開始 — Incision**
     - 外科醫師劃刀
     - 麻醉醫師記錄 Incision time
     - 啟動計時器（抗生素追加倒計時）

---

## Phase I：術中維持

### I1. 持續監測 & 記錄

119. **生命徵象持續監測**
     - ECG：持續，注意 ST 變化 / arrhythmia
     - BP（NIBP 或 A-line）：每 3–5 分鐘
     - SpO2：持續
     - ETCO2：持續（波形 + 數值）
     - 體溫：每 15–30 分鐘
     - BIS（如有）：持續，目標 40–60
     - Urine output（如有 Foley）：每 30–60 分鐘記錄

120. **麻醉紀錄填寫**
     - 每 5 分鐘記錄 VS（電子 AIMS 自動或手動）
     - 藥物給予記錄（時間 + 藥物 + 劑量 + 路徑）
     - 輸液記錄（晶體/膠體/輸血）
     - Event 記錄（特殊事件、體位變化、外科溝通）
     - I/O 累計（input = 輸液 + 輸血；output = 出血 + 尿量）

### I2. 麻醉藥物管理

121. **吸入麻醉藥調控**
     - 監測 MAC 值（age-adjusted MAC）
     - 依手術刺激調整濃度
       - 強刺激（切皮/骨鋸）→ 增加
       - 弱刺激（縫合）→ 減少
     - 併用 N2O 考量（降低 volatile MAC）
     - ⚠️ end-tidal concentration vs dial setting 差異

122. **靜脈麻醉藥調控（TIVA）**
     - Propofol infusion rate 調整（依 BIS）
     - Remifentanil infusion rate 調整（依 BP/HR/疼痛刺激）
     - ⚠️ TIVA 中斷 → awareness 風險

123. **Opioid 追加**
     - 依手術刺激 + 生命徵象判斷
     - Fentanyl bolus 或 infusion
     - ⚠️ 手術快結束 → 減少長效 opioid（避免術後呼吸抑制）

124. **肌鬆劑追加**
     - 依 TOF 監測（TOF count 1–2 → 追加）
     - 或臨床判斷（外科要求更好 relaxation / 出現 bucking）
     - 記錄追加劑量 + 時間

125. **血管活性藥物使用**
     - 低血壓
       - Ephedrine bolus（5–10 mg）
       - Phenylephrine bolus（50–100 μg）或 infusion
       - ⚠️ 持續性 → 確認原因（出血/麻醉過深/過敏/心臟問題）
     - 高血壓
       - 確認麻醉深度足夠
       - Esmolol / Labetalol / Nicardipine
     - 心搏過慢
       - Atropine 0.5 mg（可重複）
       - Glycopyrrolate 0.2 mg
     - 心搏過快
       - 確認疼痛/淺麻醉/低血容
       - Esmolol / Metoprolol

### I3. 輸液 & 輸血管理

126. **晶體液持續輸注**
     - 維持速率：1–3 ml/kg/hr（基本需求）
     - 補充禁食缺失
     - 第三空間喪失（依手術類型）
     - ⚠️ 過度輸液 → 組織水腫 / 肺水腫

127. **膠體液使用（如需要）**
     - Hydroxyethyl Starch (HES) — ⚠️ 部分指引已限制
     - Albumin
     - Gelatin
     - 用於大量出血補充 intravascular volume

128. **輸血決策 & 執行**
     - Trigger：Hb < 7 g/dL（一般），< 8 g/dL（心臟病人）
     - 下備血單 → 通知血庫
     - 血品到達 → 核對（兩人核對）
       - 血型 / Rh / 病人姓名 / 病歷號 / 血品編號 / 有效期
     - 開始輸血
       - 輸血速率（一般 15–30 min/unit）
       - 觀察輸血反應（前 15 分鐘尤其注意）
         - ⚠️ 發燒 / 寒顫 / 蕁麻疹 / 低血壓 / 血紅尿
         - → 停止輸血 → 通知血庫 → 留管路 → NS keep
     - 其他血品
       - FFP（凝血功能異常 / massive transfusion）
       - Platelet（PLT < 50,000 且持續出血）
       - Cryoprecipitate（Fibrinogen < 100）
     - Massive Transfusion Protocol (MTP) — 如觸發
       - 固定比例 PRBC : FFP : PLT
       - Cell salvage（自體血回收）
       - TXA 給予

129. **輸液加溫**
     - 大量輸液 / 輸血 → 必須加溫（37–42°C）
     - 確認加溫器設定正確
     - ⚠️ 低溫輸液 → 加重低體溫 → 凝血功能障礙

### I4. 通氣管理

130. **持續呼吸器監測**
     - ETCO2 維持 35–45 mmHg
     - SpO2 > 95%（一般）
     - Peak pressure / Compliance 變化
     - ⚠️ ETCO2 突然下降 → 可能 PE / 心輸出量下降 / 管路脫離
     - ⚠️ ETCO2 突然上升 → 可能 MH / CO2 吸收不良 / 通氣不足

131. **通氣參數調整**
     - RR 調整以維持 ETCO2 目標
     - PEEP 調整（肺塌陷 → 增 PEEP / 通氣壓過高 → 減 PEEP）
     - FiO2 下調（穩定後 → 0.3–0.5，避免 hyperoxia）
     - Recruitment maneuver（如需要）

132. **抽痰**
     - 指徵：聽到 rhonchi / PIP 上升 / SpO2 下降
     - 關閉麻醉迴路 → 斷開 → 抽吸管進入 ETT → 抽痰 → 重新接上
     - ⚠️ 過程中 SpO2 可能下降 → 快速操作

133. **ETT 位置持續注意**
     - 尤其在手術中翻身 / 頭部移動後
     - ⚠️ ETCO2 消失 / 單側呼吸音 → 立即確認管位

### I5. 特殊情境管理

134. **大出血處理**
     - 確認大口徑 IV 通暢（≥ 18G × 2）
     - 加壓輸液 + 加溫
     - 通知血庫啟動 MTP
     - 動脈血氣（ABG）+ POCT 凝血（如有 ROTEM/TEG）
     - 升壓藥物持續輸注
     - 報告主治外科醫師出血量
     - ⚠️ DIC → 積極補充凝血因子

135. **低體溫預防 & 處理**
     - 保溫毯持續運作
     - 輸液加溫
     - 刀房溫度維持（≥ 21°C）
     - 體溫 < 36°C → 加強保溫措施
     - ⚠️ 體溫 < 35°C → 凝血異常/藥物代謝↓/傷口感染↑

136. **心律不整處理**
     - 辨識類型（12-lead ECG 如需要）
     - Sinus tachycardia → 找原因（疼痛/出血/淺麻醉）
     - Sinus bradycardia → Atropine / Glycopyrrolate
     - AF / AFL → Rate control or cardioversion
     - VT / VF → ACLS protocol
     - 術中 ST elevation → 通知心臟科 + 考量術中處理

137. **支氣管痙攣（Bronchospasm）**
     - 深化麻醉（Sevoflurane 有支氣管擴張效果）
     - Salbutamol MDI via ETT
     - Epinephrine（嚴重）
     - 確認 ETT 位置（排除 carina 刺激）

138. **過敏反應（Anaphylaxis）**
     - 停止可疑藥物
     - Epinephrine 10–100 μg IV bolus（依嚴重度）
     - 大量輸液
     - 下調麻醉深度
     - 通知團隊
     - Diphenhydramine / Hydrocortisone / Salbutamol（二線）
     - 術後：Tryptase 抽血

139. **惡性高熱（MH）**
     - ⚠️ 徵兆：ETCO2 急速上升 + Tachycardia + Rigidity + 體溫上升
     - 立即停止所有 trigger agents（volatile + Succinylcholine）
     - 過度通氣 100% O2
     - **Dantrolene 2.5 mg/kg IV bolus**（重複至症狀控制）
     - 冷卻措施（冰 NS / 冰敷）
     - ABG + 電解質（hyperkalemia！）
     - MH cart 位置 → 立即取用
     - 通知 MH hotline（如有）

140. **術中抗生素追加**
     - 手術時間 > 2 個半衰期 → 追加
     - 常見：Cefazolin 每 3–4 小時追加
     - 大量出血（> 1500 ml）→ 追加
     - 計時器 / alarm 提醒

### I6. 與手術團隊溝通

141. **手術進度溝通**
     - 外科通報：目前進度（主要步驟/關鍵時點）
     - 外科需求對應
       - 「需要更好的 relaxation」→ 追加肌鬆
       - 「出血比較厲害」→ 加速輸液 + 備血
       - 「即將關刀」→ 準備 emergence
       - 「bone cement」→ 準備處理 bone cement implantation syndrome

142. **護理溝通**
     - 紗布計數異常 → 暫停 → X-ray
     - 需要追加供應（紗布/器械/藥物）
     - 體位調整需求

---

## Phase J：手術結束 & 甦醒

### J1. 手術結束準備

143. **接獲外科通知「即將關刀」**
     - 預估剩餘時間

144. **調整麻醉深度**
     - 逐步降低吸入麻醉藥濃度
     - 停止 Remifentanil infusion（或減速）
     - 停止 Propofol infusion（TIVA 情境）
     - 計畫長效止痛（如尚未給）
       - Morphine IV（如計畫 PCA）
       - Ketorolac / Acetaminophen IV
       - 確認 epidural / nerve block 仍有效
     - 止吐藥給予
       - Ondansetron 4 mg IV（結束前 30 min）

145. **準備逆轉藥物（肌鬆逆轉）**
     - 選擇
       - **Sugammadex**：Rocuronium/Vecuronium 專用
         - TOF count ≥ 2：2 mg/kg
         - TOF count = 0（deep block）：4 mg/kg
         - 無法等待：16 mg/kg（immediate reversal）
       - **Neostigmine + Glycopyrrolate**：非去極化肌鬆劑通用
         - TOF count ≥ 2 且有衰減才能用
         - 0.04–0.07 mg/kg + Glycopyrrolate 0.2 mg per 1 mg Neostigmine
     - 確認 TOF ≥ 0.9 才可拔管

### J2. 甦醒（Emergence）

146. **停止吸入麻醉藥**
     - 揮發器歸零
     - 增加 Fresh Gas Flow（高流量 wash-out）
     - 100% O2

147. **等待甦醒跡象**
     - 自主呼吸恢復
       - 先出現不規則呼吸 → 逐漸規律
       - Tidal volume 足夠
       - RR 合理（10–20）
     - 意識恢復徵象
       - 吞嚥反射恢復
       - 眼睛睜開
       - 皺眉 / 抓手 / 移動肢體
     - 呼喚病人姓名 → 反應
     - 指令遵從：「睜開眼睛」「握我的手」「抬頭 5 秒」
     - ⚠️ delayed emergence 鑑別
       - 殘餘麻醉藥
       - 殘餘肌鬆（確認 TOF）
       - 低體溫
       - 代謝異常（血糖/電解質）
       - 腦部事件（罕見）

148. **肌鬆逆轉給予（如尚未給）**
     - 確認 TOF
     - 給予 Sugammadex 或 Neostigmine + Glycopyrrolate
     - 等待 TOF ≥ 0.9

### J3. 拔管（Extubation）

149. **拔管條件確認**
     - □ 自主呼吸規律且足夠
     - □ Tidal volume > 5 ml/kg
     - □ RR 10–25
     - □ SpO2 > 95% on 100% O2
     - □ ETCO2 正常
     - □ TOF ≥ 0.9
     - □ 病人能遵從指令（或有目的性肢體活動）
     - □ 上氣道反射恢復（吞嚥 / 咳嗽）
     - □ 血行動力學穩定

150. **抽痰**
     - 口腔抽吸（Yankauer）
     - 氣管內抽吸（suction catheter via ETT）
     - 確認分泌物清除

151. **拔管執行**
     - 解開 ETT 固定
     - cuff 放氣
     - 深吸氣後（或正壓吸氣時）拔出 ETT
     - 立即給 O2
       - 面罩 / T-piece
     - 觀察呼吸
       - 胸廓起伏 ✓
       - 呼吸音正常 ✓
       - SpO2 維持 ✓
       - 無 stridor ✓
     - ⚠️ **拔管後喉痙攣（Laryngospasm）**
       - 100% O2 正壓通氣
       - Jaw thrust
       - 深化（Propofol 0.5 mg/kg）
       - ⚠️ 持續 → Succinylcholine 0.5–1 mg/kg
     - ⚠️ **拔管後氣道水腫 / Stridor**
       - Racemic epinephrine nebulizer
       - Dexamethasone IV
       - 嚴重 → 重新插管

152. **深拔管（Deep extubation）— 特殊情境**
     - 適應症：避免咳嗽（如眼科/神經外科/某些 ENT）
     - 條件：自主呼吸已恢復但仍在麻醉深度
     - 風險：喉痙攣/吸入 → 僅有經驗者執行

### J4. WHO Sign-Out（第三部分）

153. **Sign-Out 執行**
     - 外科醫師 + 麻醉 + 護理
     - □ 確認手術名稱（實際執行的）
     - □ 紗布 / 器械 / 針計數正確
     - □ 檢體標示正確
     - □ 設備問題記錄
     - □ 術後照護重點
       - 術後去向（PACU / ICU / 一般病房）
       - 關鍵術後醫囑
       - 術後注意事項

---

## Phase K：PACU 轉送 & 恢復

### K1. 轉送至 PACU

154. **離開手術室準備**
     - 面罩 O2 或鼻導管 O2
     - 清醒程度確認
     - BP / HR / SpO2 最後一組數據
     - 移至推床（若在手術台上）
       - 管路固定（IV / drain / Foley / epidural catheter）
       - 防跌 → 側欄拉起

155. **轉送中監測**
     - SpO2 隨行監測（portable pulse oximeter）
     - 持續觀察呼吸型態
     - 持續升壓藥 infusion（如有）→ 不中斷
     - ⚠️ 轉送中 SpO2 下降 → 停推床 → jaw thrust / 面罩通氣 / 求助

156. **推至 PACU**
     - 抵達 PACU 指定床位
     - 煞車固定推床

### K2. PACU 交班

157. **SBAR 交班**
     - **S（Situation）**
       - 病人姓名、年齡、體重
       - 手術名稱
     - **B（Background）**
       - 重要共病
       - 過敏
       - ASA 分級
       - 術前用藥
     - **A（Assessment）**
       - 麻醉方式（GA / Spinal / Epidural / Block / MAC）
       - 術中事件（if any）
         - 出血量
         - 輸液量（晶體/膠體）
         - 輸血量
         - Urine output
         - 血行動力學事件（低血壓/高血壓/心律不整）
       - 使用藥物（重點）
         - 肌鬆 + 逆轉（什麼藥 + 劑量 + 時間 + TOF）
         - 長效 opioid（Morphine → 劑量 + 時間）
         - 止吐藥
         - 抗生素
       - ETT size + 門齒深度（如仍帶管）
       - 區域麻醉（block level / catheter depth / infusion）
     - **R（Recommendation）**
       - 術後止痛計畫
         - PCA 設定（藥物/bolus/lockout/basal）
         - Epidural infusion 設定
         - Multimodal 止痛方案
       - 術後輸液醫囑
       - 需注意事項
         - 出血風險
         - 呼吸風險（OSA / opioid sensitivity）
         - 特殊監測（如每30min 神經 check、drain 量）
       - 術後去向（PACU → 病房 / PACU → ICU）
       - 出室條件

158. **接上 PACU 監測**
     - ECG 連接
     - NIBP 第一次量測
     - SpO2
     - O2 supply（nasal cannula / mask）
     - 溫度量測

159. **Aldrete Score 初次評分**
     - 活動力（Activity）：0–2
     - 呼吸（Respiration）：0–2
     - 循環（Circulation）：0–2
     - 意識（Consciousness）：0–2
     - SpO2：0–2
     - 總分 ≥ 9 → 可考慮出室

### K3. PACU 恢復監測

160. **持續監測**
     - VS 每 5–15 分鐘記錄（依院規）
     - 疼痛評估（NRS 數字評分 0–10）
       - NRS ≥ 4 → 給予止痛藥
       - PCA 教導病人使用
     - PONV 監測 + 處理
       - 噁心嘔吐 → Ondansetron / Metoclopramide
     - 出血監測
       - 手術傷口 / 引流管量 / 顏色
     - 尿量監測（如有 Foley）
     - 意識程度持續評估
     - ⚠️ 寒顫 → 保溫毯 + Meperidine 25 mg IV

161. **區域麻醉監測（如有）**
     - 阻滯高度變化追蹤
     - 下肢運動恢復追蹤
     - Epidural infusion 運作確認
     - ⚠️ 持續運動阻滯超過預期 → 評估 epidural hematoma / catheter migration

162. **特殊監測**
     - 甲狀腺手術後 → 頸部腫脹 / 聲音沙啞 / 呼吸困難
     - 頸椎手術後 → 四肢活動確認
     - Craniotomy 後 → GCS 評分 / 瞳孔反射
     - 扁桃腺手術後 → 吞嚥正常 / 出血確認

### K4. PACU 出室

163. **出室評估**
     - Aldrete Score ≥ 9（或院規標準）
     - 疼痛控制良好（NRS < 4）
     - 無持續噁心嘔吐
     - 血行動力學穩定（BP ± 20% 基線）
     - 呼吸穩定（RR 10–20, SpO2 > 94% on room air or low-flow O2）
     - 意識清楚
     - 無持續出血
     - 體溫 > 36°C
     - 區域麻醉阻滯已消退至安全範圍（如適用）

164. **醫師同意出室**
     - 麻醉醫師 / PACU 負責醫師評估
     - 簽署出室同意

165. **出室交班**
     - PACU 護理師 → 病房護理師
     - 用 SBAR 格式
     - 含：術後醫囑、止痛方案、注意事項、下次用藥時間

166. **轉送回病房 / ICU**
     - 推床轉送（同 Phase C 轉送注意事項）
     - SpO2 隨行監測
     - 交接完成

---

## Phase L：術後照護 & 紀錄結案

### L1. 術後照護

167. **急性疼痛服務 (APS)**
     - APS 團隊巡房
     - 評估 PCA 使用狀況
     - 調整 PCA 設定（如需要）
     - Epidural 巡查
       - 阻滯高度
       - 感覺/運動功能
       - Catheter site 感染/脫位
     - Multimodal 止痛調整
     - ⚠️ PCA 過度使用 → 評估呼吸抑制風險
     - ⚠️ 止痛不足 → rescue dose + 調整方案

168. **術後訪視**
     - 麻醉醫師術後巡房（24–48 hr 內）
     - 評估內容
       - 術後疼痛狀況
       - PONV 狀況
       - 麻醉相關併發症篩檢
         - 喉嚨痛 / 聲音沙啞
         - 牙齒損傷
         - 嘴唇 / 舌頭損傷
         - 周邊神經損傷（ulnar / brachial plexus / peroneal）
         - 術後認知功能變化（高齡）
         - 脊椎麻醉後頭痛（PDPH）
       - 病人滿意度
     - 記錄於術後訪視紀錄

169. **併發症追蹤（如發生）**
     - PDPH → epidural blood patch 諮詢
     - 神經損傷 → 神經科會診 + 追蹤
     - 術後譫妄 → 非藥物介入 + 藥物（Haloperidol / Dexmedetomidine）
     - 呼吸事件 → 加強監測 / ICU 轉入

### L2. 紀錄完成

170. **麻醉紀錄完成**
     - 電子 AIMS 或紙本
     - 確認所有時間點/藥物/事件已記錄完整
     - 確認 I/O 計算正確
     - 麻醉醫師簽名

171. **管制藥品結案**
     - 未使用的管制藥品歸還
     - 兩人核對銷毀（殘餘 Fentanyl 等）
     - 管制藥品紀錄簿簽名
     - ⚠️ 數量不合 → 報告管制藥品管理人

172. **自費品項結案**
     - 確認使用品項 vs 同意書一致
     - 未使用品項退還
     - 費用核算

173. **不良事件通報（如有）**
     - 院內通報系統填報
     - 困難氣道 → 記錄 + 通知病人 + 建議戴 MedicAlert
     - 過敏 → 記錄 + 更新過敏清單
     - 設備故障 → 通報生物醫學工程
     - MH → 通報 + 轉介遺傳諮詢

174. **品質紀錄**
     - 術中低血壓事件
     - 非計畫性 ICU 轉入
     - 困難氣道紀錄
     - 輸血事件
     - 計入品質指標追蹤

---

## 📊 統計

> 完成建檔後將於此更新各 Phase 顆粒數統計

| Phase | 名稱 | 步驟數 |
|:-----:|------|:------:|
| A | 術前門診/照會 | 14 |
| B | 手術日病房準備 | 14 |
| C | 前往開刀房 & 報到 | 8 |
| D | 等候區/進入手術室 | 9 |
| E | 手術室安頓 & 監測建立 | 12 |
| F | 麻醉準備（機器/藥物/氣道） | 17 |
| G | 麻醉誘導 | 34 |
| H | 手術擺位 & 手術開始 | 7 |
| I | 術中維持 | 24 |
| J | 手術結束 & 甦醒 | 11 |
| K | PACU 轉送 & 恢復 | 13 |
| L | 術後照護 & 紀錄結案 | 8 |
| **合計** | | **171** |

---

> ⏭️ **下一步**：逐一 audit 每個顆粒的 AI 介入機會  
> 📎 **高階 AI 分析**：參見 `anesthesia-ai-workflow-analysis.md`

*Built with CGU (Creativity Generation Unit)*
