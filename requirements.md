## Product Requirements

1. **Focus area**
   Process patents in the field of **synthetic biology** only.

2. **Time window**
   Handle **one week of newly filed US patents** per run.

3. **Data source**
   Use **USPTO bulk full-text datasets** without images.

4. **Ingestion method**
   Perform **manual downloads**; no scheduler or automation needed.

5. **Data fields to extract**

   * Patent title
   * Abstract
   * CPC classification codes
   * Inventors
   * Applicant or assignee
   * Application or publication ID
   * Filing or publication date
   * URL if available

6. **Relevance filtering**
   Apply a **rule-based filter** using synthetic biology keywords and CPC codes.

7. **Technology focus**
   Include patents where synthetic biology is the **principal technology area**; exclude tangentially related fields.

8. **Patent types**
   Include both **inventive** and **additional** patents.

9. **Search and exploration**
   Provide **lightweight search and exploration** features for non-technical users.

10. **Engineer outputs**
    Produce **weekly JSON files** with clear naming patterns (e.g. `patents_YYYY-MM-DD.json`) for easy integration by engineers.

11. **User interface**
    Offer a **simple local dashboard** for non-technical users to browse, search, and download data.

12. **Access control**
    Run **locally with no authentication** required.

13. **Ease of use**
    The tool should be **install-and-run ready**, completing a full run in minutes with minimal setup.

---
