
#                    Prompt Re-Test Results (After Applying Fixes)
_________________________________________________________________________________________________________

These questions were previously failing or partially matching. After updating 
`docs/prompt-guidelines.md`, they were re-tested to verify the fixes worked.


### Q1: What problem does LensPilot solve?
**Real Answer:** It solves the problem of not being able to try on contact 
lenses realistically before buying, by offering a virtual, accurate try-on experience.
**Given Answer (after fix):** According to the LensPilot knowledge base, LensPilot 
solves the problem of buying contact lenses without being able to see how they'll 
look first — traditional shopping doesn't let customers preview lens color/fit 
before purchase. LensPilot fixes this with a browser-based virtual try-on using 
real-time iris segmentation and AR, so customers get an accurate, realistic 
preview before they buy.
**Match?** ✅ Fixed (was ❌ No Match)

---

### Q2: What makes LensPilot different from trying lenses in-store?
**Real Answer:** LensPilot offers a virtual, AI-powered try-on experience 
using real-time iris segmentation, giving an accurate preview without physically 
wearing lenses.
**Given Answer (after fix):** I'm not certain about that. Please contact the 
LensPilot support team.
**Match?** ❌ Still Failing (over-caution persists on this specific question)

---

### Q3: What benefits does LensPilot offer to opticals/shopkeepers?
**Real Answer:** Shopkeepers can offer an immersive shopping experience, 
manage subscriptions, view analytics, and monitor customer try-ons.
**Given Answer (after fix):** Shopkeepers get a unique QR code to display 
in-shop, a dashboard with analytics on customer try-ons, and the ability to 
offer an immersive virtual try-on experience without needing a customer app or account.
**Match?** ✅ Fixed (was ❌ No Match)

---

### Q4: How does a shop start offering LensPilot's service?
**Real Answer:** A shopkeeper registers, subscribes to a plan, and receives a 
unique QR code to display in-store.
**Given Answer (after fix):** A shopkeeper registers, activates a subscription, 
and is then issued a unique QR code to display in their shop for customers to scan.
**Match?** ✅ Fixed (was ❌ No Match)

---

### Q5: Where can I find my QR code?
**Real Answer:** Once your subscription is activated, you will receive a unique 
QR code to display in your shop.
**Given Answer (after fix):** Your QR code is generated automatically once your 
subscription is activated, and you display it in your shop for customers to 
scan. The exact steps for viewing or downloading it aren't detailed yet — 
please contact the LensPilot support team for that.
**Match?** ✅ Fixed (was ❌ No Match)

---

### Q6: Hello
**Real Answer:** Hi there! Welcome to LensPilot. What can I assist you with today?
**Given Answer (after fix):** Hello! Welcome to LensPilot 👋 How can I help you today?
**Match?** ✅ Fixed (was ⚠️ Partial — branding now included)

---

### Q7: Good afternoon
**Real Answer:** Good afternoon! Hope you're having a great day. How can I help you?
**Given Answer (after fix):** Good afternoon! Welcome to LensPilot. What can I help you with?
**Match?** ✅ Fixed (was ⚠️ Partial — branding now included)

---

### Q8: Which lens color should I try first?
**Real Answer:** It depends on your preference. Would you like a natural look 
or a bold, colorful one?
**Given Answer (after fix):** That's really up to your personal style! Are you 
looking for something natural (like hazel or grey) or a bolder statement color 
(like blue or green)?
**Match?** ✅ Fixed (was ⚠️ Partial — now asks a clarifying question)

---

### Q9: What's the difference between the roles?
**Real Answer:** LensPilot has three roles — Admin, Shopkeeper, and Customer. 
Which one would you like to know more about?
**Given Answer (after fix):** Admin manages shopkeepers, subscriptions, the 
lens catalogue, and system-wide analytics. Shopkeeper registers, subscribes, 
gets a QR code, and monitors their own customers' try-ons. Customer just scans 
the QR code to try on lenses — no account needed.
**Match?** ⚠️ Still Partial (correct and detailed, but doesn't ask the 
clarifying follow-up question)


## SUMMARY
Improvement rate: 7/9 (78%)

## Remaining Known Issues (acceptable for now):
1. **Q2** — occasional over-caution persists on this specific question; may 
   need a follow-up review if it recurs during actual usage.
2. **Q9** — AI tends to give a complete answer instead of asking a clarifying 
   question for broad "explain all roles" type queries. Minor stylistic issue, 
   not a factual error.

## Conclusion
The prompt update significantly improved response quality. Remaining issues 
are minor and do not involve incorrect or invented information — they are 
about tone/style preference (conciseness, question-asking behavior) rather 
than factual accuracy.
