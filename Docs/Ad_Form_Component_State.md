# Component State для форми Ad (Create/Edit)

## Службові стейти (для управління компонентом)

1. **isEditMode** (Boolean)
   - `true` – режим редагування існуючого документу
   - `false` – режим створення нового
   - Початкове значення: `false`

2. **adDocumentRef** (Document Reference, nullable)
   - Посилання на документ, який редагується (якщо Edit)
   - Використовується для Update
   - Початкове значення: `null`

---

## Metadata стейти

3. **tempCampaignRef** (Document Reference - campaigns, nullable)
   - Посилання на кампанію
   - Обов'язкове поле

4. **tempStatus** (String)
   - Статус реклами
   - Значення: "In_Progress" | "Approved_by_lf" | "Live" | "Paused" | "Ended"
   - Початкове значення: "In_Progress"

---

## Core Data стейти

5. **tempAdName** (String)
   - Внутрішня назва реклами
   - Обов'язкове поле
   - Початкове значення: ""

6. **tempImgUrl** (String)
   - URL картинки реклами
   - Початкове значення: ""

7. **tempUploadedImage** (Uploaded File Path, nullable)
   - Для завантаження нової картинки
   - Якщо користувач обере нову картинку, вона збережеться тут
   - Після Upload → оновити tempImgUrl
   - Початкове значення: `null`

8. **tempPlatform** (String)
   - Платформа для реклами
   - Значення: "meta" | "snapchat" | "tiktok" | "youtube" | "pinterest"
   - Обов'язкове поле
   - Початкове значення: ""

9. **tempMediaType** (String)
   - Тип медіа
   - Значення: "image" | "video" | "carousel"
   - Початкове значення: "image"

10. **tempLandingPage** (String)
    - URL лендінгу
    - Початкове значення: ""

11. **tempAssetsLink** (String)
    - Посилання на Google Drive/Dropbox
    - Початкове значення: ""

12. **tempComments** (String)
    - Внутрішні нотатки
    - Початкове значення: ""

---

## Tags стейти

13. **tempTags** (List<TagStruct>)
    - Список вибраних тегів
    - Структура: `[{category: "Audience", options: ["B2B"], type: "single"}]`
    - Початкове значення: `[]`

---

## Platform-Specific Content стейти

### Meta (Arrays)

14. **tempMetaHeadlines** (List<String>)
    - До 5 заголовків для Meta
    - Початкове значення: `[]`

15. **tempMetaPreviewTexts** (List<String>)
    - До 5 preview текстів для Meta
    - Початкове значення: `[]`

### Single Text Fields

16. **tempHeadline** (String)
    - Заголовок для Snapchat, YouTube, Pinterest
    - Початкове значення: ""

17. **tempTiktokAdText** (String)
    - Текст для TikTok
    - Початкове значення: ""

18. **tempPinterestDescription** (String)
    - Опис для Pinterest
    - Початкове значення: ""

19. **tempYoutubeShortHeadline** (String)
    - Короткий заголовок для YouTube
    - Початкове значення: ""

20. **tempYoutubeLongHeadline** (String)
    - Довгий заголовок для YouTube
    - Початкове значення: ""

---

## Додаткові допоміжні стейти (опціонально)

21. **isSaving** (Boolean)
    - `true` під час збереження (показувати Loading)
    - `false` в звичайному стані
    - Початкове значення: `false`

22. **validationErrors** (List<String>, опціонально)
    - Список помилок валідації для показу користувачу
    - Початкове значення: `[]`

---

## Підсумок: **22 Component State змінні**

**Обов'язкові для заповнення (валідація):**
- tempAdName
- tempCampaignRef
- tempPlatform

**Опціональні:**
- Решта полів (залежать від платформи та специфіки реклами)

---

## Логіка ініціалізації (On Component Load)

```
IF adDocument parameter != null (Edit режим):
  → isEditMode = true
  → adDocumentRef = adDocument.reference
  → tempAdName = adDocument.ad_name
  → tempCampaignRef = adDocument.campaign_ref
  → tempStatus = adDocument.status
  → tempImgUrl = adDocument.img
  → tempPlatform = adDocument.platform
  → tempMediaType = adDocument.media_type
  → tempLandingPage = adDocument.landing_page
  → tempAssetsLink = adDocument.assets_link
  → tempComments = adDocument.comments
  → tempTags = adDocument.tags
  → tempMetaHeadlines = adDocument.meta_headlines
  → tempMetaPreviewTexts = adDocument.meta_preview_texts
  → tempHeadline = adDocument.headline
  → tempTiktokAdText = adDocument.tiktok_ad_text
  → tempPinterestDescription = adDocument.pinterest_description
  → tempYoutubeShortHeadline = adDocument.youtube_short_headline
  → tempYoutubeLongHeadline = adDocument.youtube_long_headline
ELSE (Create режим):
  → isEditMode = false
  → Всі temp* значення залишаються пустими/default
```

---

## Логіка Save

```
On Tap Save Button:
  1. Валідація:
     - IF tempAdName is empty → Show error
     - IF tempCampaignRef is null → Show error
     - IF tempPlatform is empty → Show error
  
  2. IF isEditMode == true:
       → Backend Call: Update Document (adDocumentRef)
       → Set Fields: {
           ad_name: tempAdName,
           campaign_ref: tempCampaignRef,
           status: tempStatus,
           img: tempImgUrl,
           platform: tempPlatform,
           media_type: tempMediaType,
           landing_page: tempLandingPage,
           assets_link: tempAssetsLink,
           comments: tempComments,
           tags: tempTags,
           meta_headlines: tempMetaHeadlines,
           meta_preview_texts: tempMetaPreviewTexts,
           headline: tempHeadline,
           tiktok_ad_text: tempTiktokAdText,
           pinterest_description: tempPinterestDescription,
           youtube_short_headline: tempYoutubeShortHeadline,
           youtube_long_headline: tempYoutubeLongHeadline,
           updated_at:ServerTimestamp
         }
  
  3. ELSE (Create):
       → Backend Call: Create Document (in content_plans/{planId}/ads/)
       → Set Fields: (same as above + created_at: ServerTimestamp)
  
  4. On Success:
       → Close Component / Navigate Back
       → Show "Ad Saved Successfully"
```
