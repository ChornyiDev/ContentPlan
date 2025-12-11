# Component State для форми Content Plan (Create/Edit)

## Службові стейти (для управління компонентом)

1. **isEditMode** (Boolean)
   - `true` – режим редагування існуючого Content Plan
   - `false` – режим створення нового
   - Початкове значення: `false`

2. **contentPlanDocument** (Document - content_plans, nullable)
   - Повний документ Content Plan, який редагується
   - Використовується `contentPlanDocument.reference` для Update
   - Початкове значення: `null`

---

## Basic Metadata стейти

3. **planName** (String)
   - Назва Content Plan (e.g., "Client X Master Plan")
   - Обов'язкове поле
   - Початкове значення: ""

4. **status** (String)
   - Статус Content Plan
   - Значення: "Active" | "Archived" | "On Hold"
   - Початкове значення: "Active"

5. **clientRef** (Document Reference - users, nullable)
   - Посилання на клієнта (користувача)
   - Обов'язкове поле
   - Початкове значення: `null`

---

## Enabled Statuses (динамічний список)

6. **enabledStatuses** (List<String>)
   - Список доступних статусів для ads в цьому плані
   - Приклад: `["Draft", "In Review", "Approved", "Live"]`
   - Початкове значення: `["In_Progress", "Approved_by_lf", "Live", "Paused", "Ended"]`

7. **newStatusInput** (String)
   - Тимчасове поле для додавання нового статусу
   - Початкове значення: ""

8. **editingStatusIndex** (Integer, nullable)
   - Індекс статусу, який редагується (null = не редагуємо)
   - Для inline editing у списку
   - Початкове значення: `null`

9. **editingStatusValue** (String)
   - Значення статусу під час редагування
   - Початкове значення: ""

---

## Enabled Platforms (динамічний список)

10. **enabledPlatforms** (List<String>)
    - Список ID платформ, доступних для цього плану
    - Приклад: `["meta", "tiktok"]`
    - Якщо порожній `[]` – доступні всі платформи
    - Початкове значення: `[]`

11. **availablePlatformsOptions** (List<String>)
    - Список всіх можливих платформ для вибору
    - Статичне значення: `["meta", "snapchat", "tiktok", "youtube", "pinterest"]`
    - Можна отримати з `platforms` collection якщо потрібно динамічно

---

## Enabled Tags (динамічний список TagStruct)

12. **enabledTags** (List<TagStruct>)
    - Конфігурація категорій тегів для цього плану
    - Структура: 
      ```json
      [
        {
          "category": "Funnel step",
          "options": ["Awareness", "Conversion"],
          "type": "single"
        },
        {
          "category": "Audience",
          "options": ["B2B", "B2C"],
          "type": "multi"
        }
      ]
      ```
    - Початкове значення: `[]`

### Допоміжні стейти для роботи з тегами:

13. **newTagCategory** (String)
    - Назва нової категорії тегу
    - Початкове значення: ""

14. **newTagType** (String)
    - Тип нової категорії: "single" | "multi"
    - Початкове значення: "single"

15. **newTagOptions** (List<String>)
    - Список опцій для нової категорії
    - Початкове значення: `[]`

16. **newTagOptionInput** (String)
    - Тимчасове поле для додавання нової опції до тегу
    - Початкове значення: ""

17. **editingTagIndex** (Integer, nullable)
    - Індекс тегу, який редагується
    - Початкове значення: `null`

18. **editingTagCategory** (String)
    - Категорія тегу під час редагування
    - Початкове значення: ""

19. **editingTagType** (String)
    - Тип тегу під час редагування
    - Початкове значення: "single"

20. **editingTagOptions** (List<String>)
    - Опції тегу під час редагування
    - Початкове значення: `[]`

21. **editingTagOptionInput** (String)
    - Тимчасове поле для додавання опції під час редагування
    - Початкове значення: ""

---

## UI Control стейти

22. **isSaving** (Boolean)
    - `true` під час збереження (показувати Loading)
    - Початкове значення: `false`

23. **validationErrors** (List<String>)
    - Список помилок валідації
    - Початкове значення: `[]`

24. **showAddStatusDialog** (Boolean)
    - Показувати діалог додавання статусу
    - Початкове значення: `false`

25. **showAddTagDialog** (Boolean)
    - Показувати діалог додавання категорії тегу
    - Початкове значення: `false`

26. **showEditTagDialog** (Boolean)
    - Показувати діалог редагування тегу
    - Початкове значення: `false`

---

## Підсумок: **26 Component State змінних**

**Обов'язкові для заповнення (валідація):**
- planName
- clientRef

**Опціональні але важливі:**
- enabledStatuses (має бути хоча б один статус)
- enabledTags (може бути порожній, але краще мати хоча б 1 категорію)
- enabledPlatforms (порожній = всі доступні)

---

## Логіка ініціалізації (On Component Load)

```
IF contentPlanDocument parameter != null (Edit режим):
  → isEditMode = true
  → planName = contentPlanDocument.name
  → status = contentPlanDocument.status
  → clientRef = contentPlanDocument.client_ref
  → enabledStatuses = contentPlanDocument.enabled_statuses
  → enabledPlatforms = contentPlanDocument.enabled_platforms
  → enabledTags = contentPlanDocument.enabled_tags
ELSE (Create режим):
  → isEditMode = false
  → planName = ""
  → status = "Active"
  → clientRef = null
  → enabledStatuses = ["In_Progress", "Approved_by_lf", "Live", "Paused", "Ended"]
  → enabledPlatforms = []
  → enabledTags = []
```

---

## Логіка роботи з динамічними списками

### Enabled Statuses

**Додати новий статус:**
```
On Tap "Add Status" button:
  1. IF newStatusInput is not empty
  2. IF newStatusInput not in enabledStatuses
  3. → Add newStatusInput to enabledStatuses list
  4. → Clear newStatusInput
  5. → Close dialog
```

**Видалити статус:**
```
On Tap "Delete" icon on status item:
  → Remove item from enabledStatuses at index
```

**Редагувати статус:**
```
On Tap "Edit" icon:
  1. → Set editingStatusIndex = current index
  2. → Set editingStatusValue = current status value
  3. → Show inline TextField

On Save inline edit:
  1. → Update enabledStatuses[editingStatusIndex] = editingStatusValue
  2. → Set editingStatusIndex = null
```

---

### Enabled Platforms

**Додати/видалити платформу:**
```
Use ChoiceChips or MultiSelect Dropdown:
  → Update enabledPlatforms list
  → Options from availablePlatformsOptions
```

---

### Enabled Tags

**Додати нову категорію тегу:**
```
On Tap "Add Tag Category" button:
  1. → Show dialog (showAddTagDialog = true)
  2. User enters:
     - newTagCategory (text field)
     - newTagType (dropdown: single/multi)
     - newTagOptions (dynamic list with add/remove)
  
  3. On "Save":
     - Validate: category not empty, options not empty
     - Create TagStruct: {
         category: newTagCategory,
         type: newTagType,
         options: newTagOptions
       }
     - Add to enabledTags list
     - Clear inputs (newTagCategory, newTagType, newTagOptions)
     - Close dialog
```

**Додати опцію до нової категорії (в діалозі):**
```
TextField + "Add" button:
  1. User enters option in newTagOptionInput
  2. On Tap "Add":
     - IF newTagOptionInput not empty
     - Add to newTagOptions list
     - Clear newTagOptionInput
```

**Видалити опцію з нової категорії:**
```
On Tap "X" icon on option chip:
  → Remove from newTagOptions at index
```

**Редагувати категорію тегу:**
```
On Tap "Edit" icon on tag card:
  1. → Set editingTagIndex = current index
  2. → Load data into editing states:
     - editingTagCategory = enabledTags[index].category
     - editingTagType = enabledTags[index].type
     - editingTagOptions = enabledTags[index].options
  3. → Show dialog (showEditTagDialog = true)
  
  4. User can:
     - Edit category name
     - Change type (single/multi)
     - Add/remove options (same logic as newTag)
  
  5. On Save:
     - Update enabledTags[editingTagIndex] = {
         category: editingTagCategory,
         type: editingTagType,
         options: editingTagOptions
       }
     - Clear editing states
     - Close dialog
```

**Видалити категорію тегу:**
```
On Tap "Delete" icon on tag card:
  → Show confirmation dialog
  → Remove from enabledTags at index
```

---

## Логіка валідації

```
On Tap "Save" button:
  1. Clear validationErrors list
  
  2. Validate:
     - IF planName is empty → Add "Plan name is required"
     - IF clientRef is null → Add "Client is required"
     - IF enabledStatuses is empty → Add "At least one status is required"
     - FOR EACH tag in enabledTags:
       - IF tag.category is empty → Add "Tag category cannot be empty"
       - IF tag.options is empty → Add "Tag must have at least one option"
  
  3. IF validationErrors is not empty:
     - Show error message
     - Stop execution
  
  4. Continue to Save logic...
```

---

## Логіка Save

```
On Tap "Save" button (after validation):
  1. Set isSaving = true
  
  2. IF isEditMode == true:
     → Backend Call: Update Document (contentPlanDocument.reference)
     → Set Fields: {
         name: planName,
         status: status,
         client_ref: clientRef,
         enabled_statuses: enabledStatuses,
         enabled_platforms: enabledPlatforms,
         enabled_tags: enabledTags,
         updated_at: ServerTimestamp
       }
  
  3. ELSE (Create):
     → Backend Call: Create Document (in content_plans/)
     → Set Fields: {
         name: planName,
         status: status,
         client_ref: clientRef,
         enabled_statuses: enabledStatuses,
         enabled_platforms: enabledPlatforms,
         enabled_tags: enabledTags,
         created_at: ServerTimestamp,
         updated_at: ServerTimestamp
       }
  
  4. On Success:
     → Set isSaving = false
     → Show "Content Plan Saved Successfully"
     → Navigate Back / Close Component
  
  5. On Error:
     → Set isSaving = false
     → Show error message
```

---

## UI Components структура

```
Form Container
├─ Basic Info Section
│  ├─ TextField: Plan Name (→ planName)
│  ├─ Dropdown: Status (→ status)
│  └─ Dropdown: Client (→ clientRef)
│
├─ Enabled Statuses Section
│  ├─ Header: "Ad Statuses" + "Add" button
│  ├─ ListView of status chips
│  │  └─ Each chip: [Status Name] [Edit] [Delete]
│  └─ Dialog: Add/Edit Status
│
├─ Enabled Platforms Section
│  ├─ Header: "Platforms"
│  └─ ChoiceChips (Multi-select) → enabledPlatforms
│
├─ Enabled Tags Section
│  ├─ Header: "Tag Categories" + "Add Category" button
│  ├─ ListView of tag cards
│  │  └─ Each card:
│  │     ├─ Category Name
│  │     ├─ Type badge (Single/Multi)
│  │     ├─ Options chips
│  │     └─ Actions: [Edit] [Delete]
│  └─ Dialog: Add/Edit Tag Category
│     ├─ TextField: Category Name
│     ├─ Dropdown: Type (Single/Multi)
│     └─ Dynamic Options List:
│        ├─ TextField + "Add" button
│        └─ ListView of option chips [Option] [X]
│
└─ Action Buttons
   ├─ Cancel button
   └─ Save button (with loading state)
```

---

## Додаткові considerations

### 1. **Validation для тегів**
   - Не дозволяти дублікати категорій
   - Не дозволяти дублікати опцій в одній категорії
   - Категорія повинна мати хоча б 1 опцію

### 2. **Default values при Create**
   - Можна додати кнопку "Load Default Statuses" що додасть стандартний набір
   - Можна додати кнопку "Load Default Tags" з типовими категоріями

### 3. **Reordering**
   - Додати можливість перетягування (drag & drop) для зміни порядку:
     - Статусів
     - Опцій тегів
   - Додати стейти: `statusesOrder`, `tagsOrder`

### 4. **Bulk operations**
   - "Clear All Statuses" button
   - "Clear All Tags" button
   - З підтвердженням

### 5. **Import/Export**
   - Export конфігурації тегів як JSON
   - Import з іншого Content Plan
   - Стейт: `importedConfig` (JSON String)