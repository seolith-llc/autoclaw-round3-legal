# Citation Verification Log

Every legal proposition in the review memo is traced below to the source actually read on November 6, 2026. Quotes are copied from the source text; paraphrases are labeled as such.

## 1. Tooling and jurisdiction

| Tool | Purpose | Result |
| --- | --- | --- |
| `legal_statute` (yuandian) | Statute text | Unavailable. The backend returned "service currently unavailable" on every call. It also only covers PRC law, so it could not support a US-law review even when working. |
| `legal_case` (yuandian) | Case law | Unavailable, same error, same jurisdiction limit. |
| `fetch_content` | Primary-source retrieval | Used for all authorities below. |

Because no case-law database was reachable, this review cites **statutes and regulations only** and does not assert holdings from cases. Where a case would normally be cited (unconscionability, arbitration), the memo states the statutory standard instead.

## 2. Verified authorities

### 2.1 Cal. Bus. & Prof. Code section 17602 - automatic renewal

- **Status:** current. Amended by Stats. 2024, ch. 515 (AB 2863), effective January 1, 2025. Subdivision (j) applies the amendments to contracts entered into, amended, or extended on or after July 1, 2025.
- **Verified requirements:**
  - section 17602(a)(1): renewal terms must be presented "in a clear and conspicuous manner" before the agreement is fulfilled, in visual proximity to the consent request.
  - section 17602(a)(8): before confirming billing information, notice must state that the service renews automatically, the renewal length, the amount or range of costs, at least one cancellation method, and - for electronic notice - a link to the cancellation process.
  - section 17602(b)(2): for an offer with an initial term of one year or longer that renews automatically, notice must be given **at least 15 days and not more than 45 days** before renewal.
  - section 17602(d)(1)(A): an online cancellation method, being a "prominently located direct link or button."
  - section 17602(g)(2): fee changes require 7 to 30 days' notice plus cancellation information.
- **Scope caveat recorded:** the article applies to offers made "to a consumer in this state." A 250-seat B2B subscription is likely outside its scope; the memo says so rather than overclaiming.
- **Source:** [leginfo.legislature.ca.gov, BPC 17602](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602)

### 2.2 15 U.S.C. section 8403 - ROSCA

- **Status:** current.
- **Verified text (paraphrased in memo, quoted here):** it is unlawful to charge a consumer for goods or services sold over the Internet through a negative option feature unless the seller (1) "provides text that clearly and conspicuously discloses all material terms of the transaction before obtaining the consumer's billing information," (2) "obtains a consumer's express informed consent before charging" the payment method, and (3) "provides simple mechanisms for a consumer to stop recurring charges."
- **Source:** [15 U.S.C. 8403](https://www.law.cornell.edu/uscode/text/15/8403)

### 2.3 16 CFR Part 425 - deliberately **not** cited as a click-to-cancel mandate

- **Finding:** the current eCFR text of Part 425 is titled "Use of Prenotification Negative Option Plans" and contains the prenotification-plan requirements in section 425.1 (disclosure of material terms, announcement and form timing, cancellation handling). It does **not** contain the general "click-to-cancel" requirements that are often attributed to it.
- **Action taken:** the memo cites ROSCA and the California statute for cancellation mechanics, and does not cite Part 425. Recording the negative finding prevents a future drafter from "fixing" the memo by adding a citation that the current text does not support.
- **Source:** [eCFR Title 16, Part 425](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-425)

### 2.4 Cal. Civ. Code section 1798.100 - CCPA business duties

- **Status:** current. Amended by Proposition 24, operative January 1, 2023.
- **Verified text:** subdivision (d) requires a business that discloses personal information to a service provider or contractor for a business purpose to enter into an agreement that:
  1. "Specifies that the personal information is sold or disclosed by the business only for limited and specified purposes";
  2. obligates the recipient to comply with the title and provide the same level of privacy protection;
  3. grants the business rights to take reasonable and appropriate steps to ensure compliant use;
  4. requires the recipient to notify the business if it can no longer meet its obligations;
  5. grants the business the right, on notice, to stop and remediate unauthorized use.
- **Correction recorded:** the service-provider contract requirement is subdivision **(d)**, not (e). Subdivision (e) is the reasonable-security obligation. An earlier draft of the memo cited (e); corrected before delivery.
- **Source:** [leginfo.legislature.ca.gov, CIV 1798.100](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)

### 2.5 Cal. Civ. Code section 1798.150 - private right of action

- **Status:** current. Amended by Stats. 2024, ch. 121 (AB 3286), effective January 1, 2025.
- **Verified text:** a consumer whose nonencrypted, nonredacted personal information is subject to unauthorized access and exfiltration, theft, or disclosure as a result of the business's failure to maintain reasonable security may recover "damages in an amount not less than one hundred dollars ($100) and not greater than seven hundred and fifty ($750) per consumer per incident or actual damages, whichever is greater," plus injunctive or declaratory relief.
- **Why it matters here:** statutory damages accrue per consumer per incident, so a 12-month fee cap does not cap the Customer's exposure - it only shifts who bears it.
- **Source:** [leginfo.legislature.ca.gov, CIV 1798.150](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.150)

### 2.6 UCC section 2-316 - exclusion of warranties

- **Status:** uniform text, adopted with variations by the states.
- **Verified text:** subsection (2) requires that a disclaimer of merchantability "mention merchantability" and, in a writing, be "conspicuous"; a disclaimer of fitness must be in a writing and conspicuous. Subsection (3)(a) provides that, unless circumstances indicate otherwise, implied warranties are excluded by expressions like "as is" or "with all faults" that call the buyer's attention to the exclusion. Subsection (1) provides that language negating a warranty is inoperative to the extent it cannot reasonably be construed as consistent with the express warranty.
- **Application note:** SaaS is a service, so Article 2 applies by analogy rather than directly in most states. The memo states this limitation instead of citing the section as binding.
- **Source:** [UCC 2-316](https://www.law.cornell.edu/ucc/2/2-316)

### 2.7 UCC section 2-302 - unconscionable contract or clause

- **Status:** uniform text.
- **Verified text:** if the court finds the contract or any clause unconscionable at the time it was made, it may refuse to enforce the contract, enforce the remainder without the clause, or limit the clause's application to avoid an unconscionable result. The parties are entitled to present evidence of "commercial setting, purpose and effect."
- **Source:** [UCC 2-302](https://www.law.cornell.edu/ucc/2/2-302)

### 2.8 UCC section 2-719 - limitation of remedies

- **Status:** uniform text.
- **Verified text:** subsection (2) - where an exclusive or limited remedy "fail[s] of its essential purpose," remedy may be had as provided in the Act. Subsection (3) - consequential damages may be limited or excluded "unless the limitation or exclusion is unconscionable," and limitation for commercial loss "is not" prima facie unconscionable.
- **Source:** [UCC 2-719](https://www.law.cornell.edu/ucc/2/2-719)

## 3. Claims deliberately not made

| Tempting claim | Why it is absent |
| --- | --- |
| "The liability cap is void." | Caps for commercial loss are generally enforceable. The memo argues enforceability risk, not nullity. |
| "Arbitration is unenforceable." | The Federal Arbitration Act generally favors enforcement. The memo targets forum, cost, and drafting inconsistency instead. |
| "The click-to-cancel rule requires X." | Current 16 CFR Part 425 does not contain those requirements. |
| "Courts have held this clause unconscionable." | No case database was reachable, and no case was read. Only statutory standards are cited. |

## 4. Currency statement

Authorities were read on November 6, 2026. Statutes change; re-verify before relying on this memo in a live matter.
