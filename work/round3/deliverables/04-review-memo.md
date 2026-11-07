# Contract Review Memorandum

| | |
| --- | --- |
| Matter | Master Subscription Agreement - Skyline Device Cloud platform |
| Client | Northwind Precision Manufacturing, Inc. (fictional sample) |
| Counterparty | Skyline Device Cloud, Inc. (fictional sample) |
| Review date | November 6, 2026 |
| Governing law (proposed) | Ohio, with federal law where applicable |
| Reviewer | AutoClaw Legal Review |
| Status | Fictional training sample. No real customer, contract, or personal data. Not legal advice. |

## 1. Bottom line

**Do not sign the Provider draft as written.** Fifteen clauses, twenty-four discrete problems, and three of them cannot be priced around:

1. **Section 5.2 takes the Customer's data for model training.** A perpetual, irrevocable, worldwide license to "train, fine-tune, and improve machine-learning models" is not a hosting license. If any Customer Data contains personal information, the clause also collides with the service-provider limits in Cal. Civ. Code section 1798.100(d), which requires processing only for "limited and specified purposes."
2. **Section 9.2 tries to make the liability cap non-reviewable.** A cap of 12 months' fees plus a bar on any court or arbitrator modifying it reads as an attempt to contract out of judicial review. Caps are generally enforceable for commercial loss, but the carve-outs are missing: gross negligence, willful misconduct, Section 6 breaches, and indemnity.
3. **Section 15.1 lets Provider rewrite the deal by posting.** Continued use as acceptance is the weakest form of assent, and every other protection in the contract can be undone through it.

**Five must-fix items before signature:** 5.2 (data license), 9.1-9.2 (cap and carve-outs), 15.1 (unilateral amendment), 11.1 (suspension without notice), 13.1-13.2 (forum and arbitration).

**Deliverables:** redline in Word tracked changes, clean revised draft, risk matrix, citation verification log, reusable checklist.

## 2. Scope and method

### 2.1 Task

Northwind (Ohio manufacturer, roughly 400 employees) is buying a three-year subscription to Skyline's device-telemetry platform for 250 named users at US$180,000 per year. Skyline sent its standard form. Northwind's procurement team needs a signature-ready redline and a defensible record of why each change was requested.

### 2.2 Method

1. Read the form once for structure, then again clause by clause to decide, for each issue, whether it is **void or unenforceable**, **unenforceable as applied**, or **a commercial term to trade**.
2. Test every clause against the statute that actually governs it, not against the general feeling that it is "one-sided."
3. Verify each authority in the primary source before citing it. Where a rule is commonly mis-cited, say so in the memo rather than repeating the folklore.
4. Redline as paired edits - delete the old sentence, insert the new one - so no clause carries both rules at once.

### 2.3 Two jurisdiction notes that shape the analysis

- **UCC Article 2 covers goods, not SaaS.** Ohio and most states apply Article 2 by analogy to software and services contracts. The warranty and remedy provisions below are therefore persuasive rather than directly binding, which is exactly why the drafting has to be explicit.
- **The consumer statutes may not apply to Northwind.** California's automatic-renewal law and the federal ROSCA both key off "consumer" transactions. A 250-seat B2B subscription is likely outside both. They are still cited because (a) self-service seat purchases by employees blur the line, and (b) the operational failure they target - renewal windows nobody tracks - is a real commercial risk regardless.

## 3. Clause-by-clause analysis

### 3.1 Section 1 - Services and Scope

**Draft:** features are whatever Provider's website says, and Provider may modify, suspend, or discontinue anything without notice.

**Problem.** The deliverable is defined by a document the Provider controls and can change. That is not just unfair, it is indefinite: there is no ascertainable standard to breach, so the warranty in Section 12 has nothing to attach to.

**Fix.** Exhibit A fixes the feature set, seat count, retention period, and support response times; core-feature changes need consent and trigger a refund right.

### 3.2 Section 2 - Term, Renewal, and Termination

**Draft:** automatic 12-month renewal, 60-day non-renewal notice, renewal at then-current list price; no termination for convenience; early termination accelerates all remaining fees.

**Problem.** Two layers. First, the 60-day window is shorter than most procurement cycles - miss it and the Customer buys another year at whatever price Provider posts. Second, acceleration of all remaining fees is a penalty, not a forecast of loss, and a court asked to enforce it will look for actual damages.

**Consumer-law overlay.** For consumer transactions, [Cal. Bus. & Prof. Code section 17602(b)(2)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602) requires a renewal reminder **at least 15 and not more than 45 days** before renewal of a term of one year or longer, and section 17602(d) requires an online cancellation path. ROSCA, 15 U.S.C. section 8403, requires clear disclosure of material terms before billing information is collected, express informed consent, and simple cancellation. If Northwind's employees can buy seats individually, assume these apply and design the flow accordingly.

**Fix.** Renewal only on an affirmative accepted quote, quote delivered 60 days out, increase capped at 5%, termination for convenience with pro rata refund, and a 90-day notice obligation on Provider.

### 3.3 Section 3 - Fees, Payment, and Price Changes

**Draft:** annual prepayment, non-refundable, plus a right to raise fees at any time on 30 days' notice, including mid-term.

**Problem.** A price term that one party can change unilaterally during the term is not a price term. The consideration becomes illusory at the point of change, and the Customer has already prepaid.

**Fix.** Milestone payment (50% signature, 50% production acceptance), fee lock during the Initial Term, 5% cap at renewal, late interest reduced from 1.5% to 1.0% per month.

### 3.4 Section 4 - Service Levels and Support

**Draft:** 99.5% availability, sole remedy a credit capped at 5% of the monthly fee, and upstream hosting failures excluded.

**Problem.** A remedy capped at 5% of one month's fee, declared exclusive, is a limitation of remedy. Under UCC section 2-719(2), where a limited remedy fails of its essential purpose, the buyer gets the ordinary remedies back. The more aggressive the cap, the easier that argument becomes. Excluding the Provider's own hosting failures simply moves its infrastructure risk onto the Customer.

**Fix.** 10% credit per percentage point below target, termination right if availability drops below 95% twice in six months, subcontractor failures counted as Provider downtime, credits not exclusive for material breach.

### 3.5 Section 5 - Customer Data and License to Provider

**Draft:** 5.2 grants a perpetual, irrevocable, worldwide license to use Customer Data to train models and "for any other business purpose"; 5.3 gives Provider all derived data, models, and outputs.

**Problem.** This is the clause that should stop the deal. Device telemetry from a factory floor contains operator names and badge numbers, shift patterns, throughput, and process parameters - personal information and trade secrets in the same feed. Training on it converts the Customer's data into the Provider's product.

**Statutory anchor.** Where Northwind is a "business" and Skyline a "service provider," [Cal. Civ. Code section 1798.100(d)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100) requires a written agreement that (1) specifies the limited and specified purposes, (2) obligates the service provider to comply with the statute and provide the same level of privacy protection, (3) gives the business the right to take reasonable steps to ensure compliant use, (4) requires notice if the provider can no longer meet its obligations, and (5) gives the business the right to stop and remediate unauthorized use. A model-training license is the opposite of a limited and specified purpose.

**Fix.** License limited to hosting, copying, transmitting, and displaying solely to provide the Platform; no model training; no third-party disclosure beyond bound subcontractors; de-identification standard with a no-re-identification covenant; outputs owned by Customer.

### 3.6 Section 6 - Privacy, Security, and Breach Notification

**Draft:** "commercially reasonable" measures, no responsibility absent gross negligence, notice within a "commercially reasonable time."

**Problem.** "Commercially reasonable" without a described program is unverifiable. Notice on an undefined timeline defeats the Customer's own statutory deadlines. And the liability position is worse than it looks: [Cal. Civ. Code section 1798.150](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.150) creates a private right of action for breaches caused by a failure to maintain reasonable security, with statutory damages of **$100 to $750 per consumer per incident** or actual damages, whichever is greater. A 12-month fee cap does not make that exposure disappear; it just decides who pays it.

**Fix.** Written security program and annual SOC 2 Type II; 72-hour incident notice; cooperation and cost-bearing for notification, credit monitoring, and forensics; executed DPA satisfying section 1798.100(d) before any personal information is processed.

### 3.7 Section 7 - Intellectual Property and Feedback

**Draft:** all feedback and usage data are Provider's property; Customer assigns all rights.

**Problem.** An assignment of "all right, title, and interest" in feedback captures ideas the Customer may already be developing, and "usage data" can swallow the telemetry that Section 5.1 says the Customer owns.

**Fix.** Customer keeps its feedback; Provider gets a non-exclusive license to use it, with no attribution obligation and no access to Confidential Information.

### 3.8 Section 8 - Confidentiality

**Draft:** one-way, Customer only, perpetual.

**Problem.** Provider holds the Customer's data, security architecture, and pricing - the more sensitive side of the exchange. A perpetual obligation on one party only is not a confidentiality regime, it is a gag.

**Fix.** Mutual, Term plus three years, trade secrets for as long as they remain trade secrets.

### 3.9 Section 9 - Limitation of Liability

**Draft:** cap at fees paid in the prior 12 months; no consequential, incidental, special, or indirect damages; limitations apply "regardless of the theory of liability and may not be modified by any court or arbitrator."

**Problem.** Three separate issues. The cap is measured on fees **paid**, which in year one is half a year if the payment schedule changes. The consequential-damages exclusion has no carve-outs, so it would cover a data breach the Provider caused. And the "may not be modified" sentence is an attempt to strip judicial review; no drafter can bind a court that way, and including it invites the other side to argue the whole clause is overreaching.

**Legal frame.** [UCC section 2-719(3)](https://www.law.cornell.edu/ucc/2/2-719) permits excluding consequential damages "unless the limitation or exclusion is unconscionable," and expressly notes that limitation for commercial loss is not prima facie unconscionable. [UCC section 2-302](https://www.law.cornell.edu/ucc/2/2-302) gives the court power to refuse enforcement of an unconscionable clause. The realistic risk is not that the cap is void, it is that a court reads the combination - tiny cap, no carve-outs, no review - as evidence of unconscionability and unwinds more than intended.

**Fix.** Cap = greater of 12 months' fees or 2x annual fee; carve-outs for gross negligence, willful misconduct, Section 6, and indemnity; delete the non-modification sentence and replace with a standard unenforceable-provision carve-out.

### 3.10 Section 10 - Indemnification

**Draft:** Customer indemnifies Provider for any claim arising from Customer Data or use of the Platform, **including claims caused by Provider's own negligence**; no IP indemnity from Provider.

**Problem.** The Customer is indemnifying the Provider for the Provider's negligence. That is not an allocation of risk, it is a transfer of the Provider's own tort exposure. Meanwhile the Customer gets no protection if the Platform itself infringes.

**Fix.** Customer indemnity limited to third-party claims that Customer Data, used as permitted, infringes; add a reciprocal Provider IP indemnity with the usual procure/modify option.

### 3.11 Section 11 - Suspension and Acceptable Use

**Draft:** immediate suspension on suspicion, with or without notice; AUP changeable at will.

**Problem.** Suspension is the practical equivalent of termination for a production system, but it bypasses every termination protection in Section 2. "Suspicion" is not a standard.

**Fix.** Notice plus 48-hour cure for breaches posing imminent risk, immediate suspension only where legally required, suspension limited to affected users or features, prompt restoration; AUP frozen at signing with 30-day notice for changes.

### 3.12 Section 12 - Warranties and Disclaimers

**Draft:** "AS IS," all implied warranties disclaimed including merchantability, fitness, and non-infringement.

**Problem.** Two drafting defects. First, there is no express warranty at all, so the disclaimer is doing all the work and the Customer has nothing to enforce. Second, a blanket disclaimer sitting alongside a service description creates the conflict [UCC section 2-316(1)](https://www.law.cornell.edu/ucc/2/2-316) addresses: language negating a warranty is inoperative to the extent it cannot be read consistently with the express warranty. Conspicuous "as is" language does work under section 2-316(3)(a), which is why the fix is to add an express performance warranty, not to delete the disclaimer.

**Fix.** Express warranty of material conformance to Exhibit A and workmanlike performance; disclaimer limited to implied warranties and to the extent permitted by law, expressly not applying to the express warranty.

### 3.13 Section 13 - Governing Law and Dispute Resolution

**Draft:** Texas law, Travis County courts, but mandatory AAA arbitration in Austin with a class-action waiver.

**Problem.** The forum clause and the arbitration clause are internally inconsistent, which is a preview of the fight the Customer would have at the courthouse door. Beyond that, a home-forum arbitration with a fee-shifting risk is a cost barrier, and the class waiver is written without a severability fallback.

**Fix.** Ohio law and Cuyahoga County courts; no mandatory arbitration; litigation route preserved; class waiver only to the extent enforceable.

### 3.14 Section 14 - Assignment and Subcontracting

**Draft:** Provider may assign to any affiliate or successor without consent; Customer may not assign at all; no responsibility stated for subcontractors.

**Problem.** An assignment to a competitor or to a distressed acquirer changes the counterparty without the Customer's consent, on a three-year prepaid contract.

**Fix.** Mutual consent, successor exception with assumption, competitor carve-out, Provider responsible for subcontractors.

### 3.15 Section 15 - General

**Draft:** Provider may amend by posting; continued use is acceptance.

**Problem.** This is the clause that nullifies the other fourteen. Posting plus continued use is weak assent for material terms, and it makes every negotiated protection revocable.

**Fix.** Amendments only by signed writing; exhibits updatable only through the specific mechanisms in Sections 1.2 and 11.2.

## 4. Negotiation priorities

| Priority | Clauses | Approach |
| --- | --- | --- |
| Walk-away | 5.2, 6.2-6.3, 9.2 | Offer price movement in exchange; frame as data-governance requirement, not leverage |
| Must fix | 2.2-2.3, 9.1, 11.1, 13.1-13.2, 15.1 | Redline as drafted; do not accept "market standard" without a citation |
| Trade | 3.3 (interest), 4.2 (credit size), 8.1 (survival period), 10.1 (indemnity scope) | Concede one to hold the walk-away items |
| Paper the file | 12.1 | Keep the express warranty even if the disclaimer stays |

## 5. Open items for the business team

1. Confirm whether any seat is purchased by an individual on a personal card - that determines whether the consumer renewal statutes apply.
2. Confirm whether Customer Data includes biometric or badge-scan data; if so, additional consent and retention limits apply before go-live.
3. Confirm data residency requirements and whether any processing occurs outside the United States.
4. Confirm the SOC 2 report has been received and reviewed by security, not just promised in the contract.
5. Decide whether Northwind will accept arbitration if Skyline insists; if yes, negotiate seat location and cost allocation.

## 6. Multi-state overlay: Virginia, DC, Maryland, Delaware, California, Texas

Northwind operates in four jurisdictions and has remote staff in two more. That does not require six contracts, and it does not require six reviews. The Ohio choice-of-law clause selects one body of contract law. What changes state to state is the regulatory overlay, because those statutes attach by where the person lives, not by what the contract says.

**The finding that shapes the DPA.** Five of the six comprehensive statutes exclude commercial and employment data from the definition of "consumer": Virginia ([59.1-575](https://law.lis.virginia.gov/vacode/title59.1/chapter53/section59.1-575/)), Maryland (14-4601(H)), Delaware (12D-102(8)), and Texas ([541.001(7)](https://capitol.texas.gov/tlodocs/88R/billtext/html/HB00004F.htm)) all carve out individuals acting in an employment context. California does not - CCPA covers employees and job applicants. Since the platform's personal data is badge numbers, operator names, and shift records, **California is the only jurisdiction where the workforce data in scope is protected data.** The DPA is therefore California-shaped, and the other states inherit it.

| Jurisdiction | Regime | Applies to this deal? | Consequence |
| --- | --- | --- | --- |
| California | CCPA/CPRA | Yes - employees covered | 1798.100(d) terms required; 1798.150 creates statutory damages of $100-$750 per consumer per incident |
| Virginia | VCDPA | Only if consumer data enters the platform | Processor duties in 59.1-579(B) set the template for the DPA |
| Maryland | MODPA (eff. Oct 1, 2025) | Only if consumer data enters the platform | Employment carve-out; violation is a Consumer Protection Act violation |
| Delaware | DPDPA | Below threshold today (35,000 consumers, or 10,000 plus 20% of revenue from sales) | Monitor if consumer-facing features ship |
| Texas | TDPSA | Small-business exemption likely applies | Loses the exemption if sensitive data is sold |
| District of Columbia | No comprehensive statute | n/a | Obligations come from the contract, the CPPA, and breach-notification law |

**What this changes in the paper.** Three clauses, not fifty. Section 6.3 makes the DPA a condition precedent and writes the CCPA's five terms into it. Section 14.1 imposes the Virginia-style flow-down onto subcontractors, which is what 59.1-579(B)(5) requires. Deletion and return at termination is the one requirement still open; it belongs in Exhibit B rather than the main body, and is flagged in Section 5. Everything else is the same contract in every state.

**What it does not change.** The liability, warranty, and forum analysis. Those run through Ohio law and do not vary by where an employee sits.

## 7. Sources

- [Cal. Bus. & Prof. Code section 17602 (automatic renewal)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602)
- [15 U.S.C. section 8403 (ROSCA)](https://www.law.cornell.edu/uscode/text/15/8403)
- [Cal. Civ. Code section 1798.100 (CCPA business duties)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100)
- [Cal. Civ. Code section 1798.150 (private right of action)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.150)
- [UCC section 2-316 (exclusion of warranties)](https://www.law.cornell.edu/ucc/2/2-316)
- [UCC section 2-302 (unconscionable contract or clause)](https://www.law.cornell.edu/ucc/2/2-302)
- [UCC section 2-719 (limitation of remedies)](https://www.law.cornell.edu/ucc/2/2-719)
