# CONTRACT｜prospera-engine-ontology
Ring: R4 Engines（R4a Internal Intelligence 子環；程式碼標 R4a，見 ontology_classifier）
Version: v1.0
Date: 2026-05-31

## Input
| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| concept | string | ✅ | 需要語義理解的概念 |
| domain | string | ✅ | 業務領域 |

## Output
| 欄位 | 型別 | 說明 |
|------|------|------|
| ontology_map | object | 語義關係圖 |
| related_concepts | array | 相關概念清單 |

## Boundary
- 不負責內容生成（由 prospera-engine-generation 處理）
- 只負責語義理解和知識圖譜
