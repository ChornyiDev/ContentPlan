# Component State для форми Ad (Create/Edit)

## Службові стейти (для управління компонентом)

1. **isEditMode** (Boolean)
   - `true` – режим редагування існуючого документу
   - `false` – режим створення нового
   - Початкове значення: `false`

2. **adDocument** (Document - ads, nullable)
   - Повний документ, який редагується (якщо Edit)
   - Містить всі дані, так що не потрібен додатковий запит
   - Використовується `adDocument.reference` для Update
   - Початкове значення: `null`

---

## Metadata стейти

3. **campaignRef** (Document Reference - campaigns, nullable)
   - Посилання на кампанію
   - Обов'язкове поле

4. **status** (String)
   - Статус реклами
   - Значення: "In_Progress" | "Approved_by_lf" | "Live" | "Paused" | "Ended"
   - Початкове значення: "In_Progress"

---

## Core Data стейти

5. **adName** (String)
   - Внутрішня назва реклами
   - Обов'язкове поле
   - Початкове значення: ""

6. **imgUrl** (String)
   - URL картинки реклами
   - Початкове значення: ""

7. **uploadedImage** (Uploaded File Path, nullable)
   - Для завантаження нової картинки
   - Якщо користувач обере нову картинку, вона збережеться тут
   - Після Upload → оновити imgUrl
   - Початкове значення: `null`

8. **platform** (String)
   - Платформа для реклами
   - Значення: "meta" | "snapchat" | "tiktok" | "youtube" | "pinterest"
   - Обов'язкове поле
   - Початкове значення: ""

9. **mediaType** (String)
   - Тип медіа
   - Значення: "image" | "video" | "carousel"
   - Початкове значення: "image"

10. **landingPage** (String)
    - URL лендінгу
    - Початкове значення: ""

11. **assetsLink** (String)
    - Посилання на Google Drive/Dropbox
    - Початкове значення: ""

12. **comments** (String)
    - Внутрішні нотатки
    - Початкове значення: ""

---

## Tags стейти

13. **tags** (List<TagStruct>)
    - Список вибраних тегів
    - Структура: `[{category: "Audience", options: ["B2B"], type: "single"}]`
    - Початкове значення: `[]`

---

## Platform-Specific Content стейти

### Meta (Arrays)

14. **metaHeadlines** (List<String>)
    - До 5 заголовків для Meta
    - Початкове значення: `[]`

15. **metaPreviewTexts** (List<String>)
    - До 5 preview текстів для Meta
    - Початкове значення: `[]`

### Single Text Fields

16. **headline** (String)
    - Заголовок для Snapchat, YouTube, Pinterest
    - Початкове значення: ""

17. **tiktokAdText** (String)
    - Текст для TikTok
    - Початкове значення: ""

18. **pinterestDescription** (String)
    - Опис для Pinterest
    - Початкове значення: ""

19. **youtubeShortHeadline** (String)
    - Короткий заголовок для YouTube
    - Початкове значення: ""

20. **youtubeLongHeadline** (String)
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
- adName
- campaignRef
- platform

**Опціональні:**
- Решта полів (залежать від платформи та специфіки реклами)

---

## Логіка ініціалізації (On Component Load)

```
IF adDocument parameter != null (Edit режим):
  → isEditMode = true
  → adName = adDocument.ad_name
  → campaignRef = adDocument.campaign_ref
  → status = adDocument.status
  → imgUrl = adDocument.img
  → platform = adDocument.platform
  → mediaType = adDocument.media_type
  → landingPage = adDocument.landing_page
  → assetsLink = adDocument.assets_link
  → comments = adDocument.comments
  → tags = adDocument.tags
  → metaHeadlines = adDocument.meta_headlines
  → metaPreviewTexts = adDocument.meta_preview_texts
  → headline = adDocument.headline
  → tiktokAdText = adDocument.tiktok_ad_text
  → pinterestDescription = adDocument.pinterest_description
  → youtubeShortHeadline = adDocument.youtube_short_headline
  → youtubeLongHeadline = adDocument.youtube_long_headline
ELSE (Create режим):
  → isEditMode = false
  → Всі значення залишаються пустими/default
```

---

## Логіка Save

```
On Tap Save Button:
  1. Валідація:
     - IF adName is empty → Show error
     - IF campaignRef is null → Show error
     - IF platform is empty → Show error
  
  2. IF isEditMode == true:
       → Backend Call: Update Document (adDocument.reference)
       → Set Fields: {
           ad_name: adName,
           campaign_ref: campaignRef,
           status: status,
           img: imgUrl,
           platform: platform,
           media_type: mediaType,
           landing_page: landingPage,
           assets_link: assetsLink,
           comments: comments,
           tags: tags,
           meta_headlines: metaHeadlines,
           meta_preview_texts: metaPreviewTexts,
           headline: headline,
           tiktok_ad_text: tiktokAdText,
           pinterest_description: pinterestDescription,
           youtube_short_headline: youtubeShortHeadline,
           youtube_long_headline: youtubeLongHeadline,
           updated_at: ServerTimestamp
         }
  
  3. ELSE (Create):
       → Backend Call: Create Document (in content_plans/{planId}/ads/)
       → Set Fields: (same as above + created_at: ServerTimestamp)
  
  4. On Success:
       → Close Component / Navigate Back
       → Show "Ad Saved Successfully"
```


