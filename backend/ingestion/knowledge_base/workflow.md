---
title: Complete Workflow
category: Workflow
audience: public
source: LensPilot Knowledge Base v1
version: 2026-07-03
public: true
---
# Complete Workflow

This is the full end-to-end flow of how LensPilot is used, from setup to
a customer's try-on session.

## The full flow
1. Admin creates the lens catalogue.
2. Shopkeeper registers an account.
3. Subscription is activated for the shopkeeper.
4. QR code is generated for the shopkeeper.
5. Customer scans the shopkeeper's QR code (no account needed).
6. Virtual try-on opens in the customer's browser.
7. Camera permission is requested from the customer.
8. AI detects the iris in the camera feed (iris segmentation).
9. Lens overlay is rendered on the customer's eyes in real time.
10. Customer changes lens colors to compare different options.
11. Session ends when the customer is done.

## Notes on the flow
Each shopkeeper gets exactly one QR code, and the lens catalogue is
centrally managed by admins -- shopkeepers do not add their own lenses.
